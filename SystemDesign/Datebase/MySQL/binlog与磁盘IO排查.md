# binlog 与磁盘 IO 排查

## binlog 的用途

binlog 只服务三件事：

| 用途 | 说明 |
|---|---|
| 主从复制 | 从库读主库 binlog 回放 |
| 时间点恢复 PITR | 全量备份 + binlog 回放到任意时刻 |
| CDC 订阅 | Debezium / canal / maxwell 等订阅 binlog 做数据管道 |

三者都不需要时（本机开发库、单实例、无 PITR 流程），binlog 是纯开销，可以整个关掉。

### 关闭与清理

```ini
# my.cnf
skip-log-bin
```

容器场景直接作为服务端参数追加：

```bash
podman run -d --name mysql -e MYSQL_ROOT_PASSWORD=xxx -p 3306:3306 \
  -v /path/to/data:/var/lib/mysql \
  docker.io/library/mysql:latest \
  --skip-log-bin \
  --innodb-flush-log-at-trx-commit=2 \
  --innodb-flush-neighbors=0
```

数据在 bind mount 上时，删除重建容器不会丢数据。

**清理顺序很重要**：先在 binlog 仍启用的状态下清空，再关闭。关闭后 `PURGE` 语句不可用。

```sql
-- MySQL 8.4+
RESET BINARY LOGS AND GTIDS;
-- MySQL 8.0
RESET MASTER;
-- 或只保留最近 1 天（保留 binlog 但限制体积）
SET GLOBAL binlog_expire_logs_seconds = 86400;
```

不要手动 `rm binlog.0*`：`binlog.index` 会与实际文件不一致，mysqld 可能启动失败。

### 按库过滤

```ini
binlog-ignore-db = some_hot_db    # 黑名单：排除指定库
binlog-do-db     = only_this_db   # 白名单：只记录指定库
```

**坑**：

- `binlog_format=STATEMENT` 时，过滤依据是「当前默认库」（`USE` 选中的那个），而非表实际所属的库。跨库语句 `INSERT INTO other_db.t ...` 会判错。
- `binlog_format=ROW`（MySQL 8 默认）按受影响表的实际库判断，相对可靠。
- 白名单模式下未列出的库是**静默**不记录的，日后想做 PITR 才发现没有日志。

完全不需要复制和 PITR 时，`skip-log-bin` 比配过滤规则更简单也更可靠。

---

## 核心经验：binlog 体积 ≠ binlog 是写入源

这是最容易误判的一点。两组概念必须分开：

### 存量 vs 速率

binlog 目录占几十 GB，说明的是**历史累积未清理**，不等于它当前在高速写入。

实测参考（某开发库，数据库本体 95 MB，binlog 72 GB）：

```
数据目录总计           72 G
  其中 binlog          72 G    ← 99.9% 的空间
  实际数据库           ~95 MB
```

同一环境下测 60 秒窗口的写入速率：

```
分区总写入              576.18 MB   (9.60 MB/s)
  binlog 增长             6.24 MB   ← 仅占 1.08%
  其他追加型文件合计      0.15 MB
  无法归因（原地覆写）  569.79 MB   ← 98.9%
```

**空间占了 99.9%，写入速率只占 1.08%。** 看 `du` 得出的结论会完全反过来。

### 字节 vs fsync

binlog 的字节量小，但 `sync_binlog=1` 时每个事务提交都要 fsync 一次。这贡献的是 **IOPS 和延迟**，不是 MB/s。

判据：写入速率除以 IOPS，得到平均请求大小。

```
11 MB/s ÷ 748 iops ≈ 15 KB/次
```

十几 KB 的平均请求 = 大量小同步写，典型的高频小事务 + fsync 风暴特征。这种负载对廉价无 DRAM 缓存的 SATA SSD 最致命：顺序吞吐看着够用，但随机小写的延迟会劣化一到两个数量级。

---

## MySQL 真正的写入来源：InnoDB 写放大

一次事务提交会触发多处写入：

| 文件 | 性质 | 说明 |
|---|---|---|
| `#innodb_redo/` | 原地覆写 | redo log，每次提交都写 |
| `undo_001` / `undo_002` | 原地覆写 | undo 表空间，长事务会让它膨胀 |
| `#ib_16384_*.dblwr` | 原地覆写 | doublewrite 缓冲，**每个页刷盘都写两遍** |
| `mysql.ibd` | 原地覆写 | 数据字典，DDL 和临时表会频繁改动 |
| `*.ibd` | 原地覆写 | 实际表数据，按检查点惰性刷盘 |
| `binlog.NNNNNN` | 追加 | 可关闭 |
| `ibdata1` | 原地覆写 | 系统表空间 |

**数据库很小也可能写很多。** 数据库完全装进 buffer pool 时，数据页刷盘很少，但 redo / undo / doublewrite / binlog 的写入与**事务笔数**成正比，与数据量无关。

观察到的信号：数据目录里 `*.ibd` 几乎不变，而 `undo_*`、`dblwr`、redo 持续被改动 → 事务笔数极高，单笔很小。

---

## 开发机参数

```ini
innodb_flush_log_at_trx_commit = 2   # 每秒 fsync，而非每次提交
sync_binlog                    = 0   # 交给 OS 决定（或直接 skip-log-bin）
innodb_flush_neighbors         = 0   # SSD 不需要邻页合并刷写
```

### `innodb_flush_log_at_trx_commit` 取值

| 值 | 行为 | 崩溃损失 | 场景 |
|---|---|---|---|
| 1 | 每次提交写 redo + fsync | 不丢 | 生产，默认 |
| 2 | 每次提交写 redo，每秒 fsync | **mysqld 进程崩溃不丢**；OS/主机崩溃丢最后 1 秒 | 开发机 |
| 0 | 每秒写 redo + fsync | mysqld 崩溃也丢最后 1 秒 | 可重建的临时数据 |

`2` 是开发机的合理档位：mysqld 自身崩溃（最常见的情况）不丢数据，只有整机掉电才丢 1 秒。

### 不要动的

- `innodb_doublewrite = 0` 能省一半页写入，但页断裂（torn page）时无法恢复，有数据损坏风险。不要为了性能关它。

---

## 根治：减少事务笔数

参数调优只能降低每笔事务的开销，笔数本身是应用决定的。单行 `INSERT` 连续轰炸改成下面任一种，redo / undo / binlog 的写入量可降一到两个数量级：

```sql
-- 多行批量
INSERT INTO t (a,b) VALUES (1,2),(3,4),(5,6), ... ;

-- 或显式事务包住一批
START TRANSACTION;
  INSERT ...;  -- N 条
COMMIT;
```

自动提交下每条 `INSERT` 都是一个完整事务，各自付一轮 redo 写 + fsync + binlog 写 + fsync。

---

## 排查方法论

### 第一步：分清 CPU / 内存 / IO

```bash
cat /proc/pressure/cpu /proc/pressure/memory /proc/pressure/io
```

`some` = 至少一个任务被阻塞；`full` = 所有任务都被阻塞（对应整机卡顿）。`cpu full` 为 0 而 `io full` 很高，就不必再看 CPU 占用。

### 第二步：定位到分区，不要停在整盘

整盘数字会掩盖是哪个挂载点的问题。

```bash
cp /proc/diskstats /tmp/d1; sleep 10; cp /proc/diskstats /tmp/d2
awk 'NR==FNR{a[$3]=$0;next}
     ($3 in a)&&($3~/^(sd[a-z]+[0-9]*|nvme[0-9]+n[0-9]+(p[0-9]+)?)$/){
       split(a[$3],b," ");
       rio=$4-b[4]; wio=$8-b[8]; rd=($6-b[6])*512; wr=($10-b[10])*512;
       tms=($7-b[7])+($11-b[11]); ios=rio+wio;
       aw=(ios>0)?tms/ios:0; util=($13-b[13])/100;
       if(ios>0) printf "%-10s read=%7.2f MB/s write=%7.2f MB/s w_iops=%5d avio=%6.2f ms util=%6.1f%%\n",
         $3, rd/10/1048576, wr/10/1048576, wio/10, aw, util }' /tmp/d1 /tmp/d2
```

`/proc/diskstats` 字段：`$4` 读完成数、`$6` 读扇区数、`$7` 读耗时 ms、`$8` 写完成数、`$10` 写扇区数、`$11` 写耗时 ms、`$13` 设备忙碌 ms。扇区恒为 512 字节。

然后用 `findmnt -no TARGET,SOURCE` 对照分区与挂载点。

### 第三步：归因到文件

关键是区分两类写入：

- **追加型**（binlog、各种 log、WAL、jsonl）：文件大小会涨，用 `stat -c %s` 前后对比即可精确归因。
- **原地覆写**（InnoDB redo/undo/dblwr/ibd、数据库数据文件）：大小不变，**只能靠 mtime 发现，无法用大小归因**。

```bash
# 追加型：精确字节数
stat -c '%s %n' /path/to/*.log > /tmp/s1; sleep 60; stat -c '%s %n' /path/to/*.log > /tmp/s2

# 原地覆写：找出窗口内被改动的全部文件
find /data -xdev -type f -mmin -1
```

把「分区总写入」减去「可归因的文件增长」，差额就是原地覆写 + 文件系统日志提交 + 元数据。差额占比很高时，不要再去找「哪个日志文件在涨」。

### 第四步：交叉验证（最重要）

单一指标会骗人。至少用两个独立来源互相印证：

```
PSI io full  ←→  diskstats util
进程 CPU     ←→  进程累计 IO (/proc/PID/io)
文件大小增长 ←→  分区总写入量
```

数字互相矛盾时，优先相信 `diskstats`（直接来自块层）。

### 常用命令

```bash
# 长期平均写入速率（累计量 ÷ 开机时长），用来判断某次测量是否是突发峰值
awk '$3=="sdb8"{w=$10*512} END{print w/1e9" GB"}' /proc/diskstats
awk '{print $1}' /proc/uptime

# 不可中断 IO 等待的进程 + 内核等待点
ps -eo stat=,pid=,user=,wchan:22=,comm= | awk '$1~/D/'

# 直接内存回收（判断是否内存压力导致的停顿，比 free 有用）
grep -E 'pgsteal_direct|pgscan_direct|pswpin|pswpout|pgmajfault' /proc/vmstat

# MySQL 自己统计的每文件写入量（最权威）
SELECT FILE_NAME, COUNT_WRITE, SUM_NUMBER_OF_BYTES_WRITE/1024/1024 AS MB
FROM performance_schema.file_summary_by_instance
ORDER BY SUM_NUMBER_OF_BYTES_WRITE DESC LIMIT 15;
```

### `wchan` 对照

| wchan | 含义 |
|---|---|
| `folio_wait_bit_common` | 等页面从磁盘读回（常见于 swap 换入） |
| `wait_on_buffer` | 等文件系统元数据块 |
| `submit_bio_wait` | 等块设备 IO 完成 |
| `jbd2/sdXN-8` 本身是 D 状态 | 该分区 ext4 日志线程阻塞 → 密集小写入 + fsync |

### `avio` 参考值

单次 IO 平均耗时，判断磁盘是否真的是瓶颈：

| avio | 判断 |
|---|---|
| < 0.5 ms | 正常 NVMe / SSD |
| 1–5 ms | 偏慢，或 SATA SSD 接近满载 |
| > 10 ms | 已在产生可感知卡顿 |
| > 20 ms | 机械盘水平 |
| > 100 ms | 队列彻底积压，整机冻结 |

---

## 陷阱：PSI io 压力可能完全不反映磁盘负载

`/proc/pressure/io` 和 `iowait` 都可能被「持续计入 `nr_iowait` 但不产生块设备 IO」的任务顶高，此时它们作为磁盘瓶颈指标是无效的。

实测可以出现这种组合：

```
io full 停顿          = 88%
所有分区 util         ≈ 1%
自开机 iowait 占比    = 41.9%
procs_blocked         = 8~9（长期稳定）
采样瞬间的 D 状态任务 = 0
```

### 判定方法

做一次**可验证的对照实验**：确凿地移除一部分磁盘负载，再看指标是否跟着变。

某环境移除了约 9 MB/s、750 iops 的写入（分区 util 从 77% 降到 0.5%）后，`io full` 的日均值变化：

```
移除前   72.9%
移除后   70.4%    ← 基本未变
```

负载被证实移除而指标不动 → 该指标与磁盘负载无关，不能用它定位。

另一个佐证信号：`procs_blocked` 长期稳定在某个非零值（如 6~9），且 `blocked` 归零的秒数与 `io full` 接近 0 的秒数完全吻合 —— 说明压力值由一组常驻的「阻塞」任务撑着，而非真实 IO 竞争。这类任务每次只阻塞极短时间，瞬时采样抓不到 D 状态，但会连续累加 PSI。

### 应对

- **不要用 PSI io 或 iowait 判断磁盘瓶颈**，改用 `diskstats` 的 `util` 和 `avio`，它们直接来自块层。
- PSI io 仍可用于**相对比较**（同一台机器上尖峰相对基线的高度），但其绝对值无意义。
- 失效的 FUSE 挂载（守护进程已死、挂载点残留、`stat` 返回 ENOTCONN）是会造成伪 IO 等待的已知诱因之一，值得顺手排除，但**清掉它不一定能让读数恢复正常**：

```bash
mount | grep -i fuse
stat /tmp/fuse                      # 报「传输端点尚未连接」即为死挂载
cat /sys/fs/fuse/connections/*/waiting
fusermount -u /tmp/fuse || sudo umount -l /tmp/fuse
```

- 排查 D 状态任务时注意两个坑：
  - `awk '{print $3}' /proc/PID/stat` 取状态位是**错的** —— 进程名含空格时（如 Firefox 的 `Isolated Web Co`）字段会错位。应取「最后一个 `)` 之后」的字符，或直接用 `ps -eLo stat=`。
  - 要扫**线程**（`/proc/*/task/*`）而非只扫进程，很多阻塞发生在非主线程。

### 反之

`diskstats` 显示某分区 `util` 70%+ 且 `avio` 超过 10 ms 时，磁盘瓶颈是真实的，与 PSI 是否虚高无关。两者判断冲突时以 `diskstats` 为准。

---

## 速查

| 现象 | 结论 |
|---|---|
| binlog 目录很大 | 空间问题。清理 + 关闭或设过期时间；**不代表它在高速写入** |
| 写入速率高但平均请求只有十几 KB | 高频小事务 + fsync 风暴。调 `innodb_flush_log_at_trx_commit`，根治靠批量提交 |
| 数据库很小但写入量很大 | 写放大（redo/undo/doublewrite）。与事务笔数相关，与数据量无关 |
| `*.ibd` 不变而 `undo_*`/`dblwr` 持续改动 | 同上，事务笔数极高 |
| 分区总写入远大于文件大小增长之和 | 原地覆写为主，别再找「哪个日志在涨」 |
| `jbd2/sdXN-8` 常处于 D 状态 | 该分区密集小写入 + fsync |
| `io full` 高但所有分区 `util` 都低 | PSI 不可信。改用 `diskstats` 的 `util`/`avio`；用「移除已知负载看指标是否变化」验证 |
| 同机有空闲的更快磁盘 | 把高 IOPS 服务的数据目录迁过去，不改任何服务配置即可缓解 |
