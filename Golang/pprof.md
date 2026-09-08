# 例子

```go

import (
	_ "net/http/pprof"
)

func main() {  
    go func() {  
	   //如果没有启动默认的http server，则启动一下
       if err := http.ListenAndServe(":6060", nil); err != nil && errors.Is(err, http.ErrServerClosed) {  
          log.Printf("pprof server error: %s", err)  
       }  
    }()  
}
```


# 一次分析

## 上 pprof 之前：先判断这是「什么类型」的 CPU


```bash
ps -L -p 576302 -o tid,pcpu,stat,comm --sort=-pcpu     # 每线程 CPU
for t in /proc/576302/task/*; do awk '{print $14,$15}' $t/stat; done  # utime/stime
```
三个信号：

| 观察                                       | 排除了什么                     |
| ---------------------------------------- | ------------------------- |
| utime 累计 3200 万 tick，stime 只有 ~1200 tick | 纯用户态计算，不是系统调用/futex 抖动/IO |
| RES 只有 46MB                              | 不是 GC 抖动（堆太小）             |
| 日志 15:55 后无业务活动，CPU 仍 380%               | 与业务负载无关，是常驻空转             |


还算了一下：324000s CPU / 84600s 墙钟 ≈ 3.83 核，所以大概是 4~5 个 goroutine 在死转，而不是「整体偏慢」。这个数字后面用来交叉验证。

顺带试过 perf（perf_event_paranoid=4）和 dlv/gdb attach（yama/ptrace_scope=1），都没权限，所以必须走进程自己暴露的 pprof。

## pprof：抓 CPU profile

 
```bash
curl -o cpu.pprof "xxxx/debug/pprof/profile?seconds=20"
go tool pprof -top -nodecount=25 /opt/xxx cpu.pprof
```
注意要带上二进制路径，否则符号解析不出来。输出：

```bash
Duration: 20.18s, Total samples = 97.96s (485.38%)
   19.36s 19.76%  xxxx.func1.1
   15.66s 15.99%  sync/atomic.(*Value).Load
   11.45s 11.69%  context.(*cancelCtx).Done       (cum 57.93%)
    3.68s  3.76%  runtime.selectnbrecv
```
485.38% 和前面 /proc 算出的 3.83 核对得上（采样时略高），说明抓到的就是元凶而不是采样偏差。

关键不是 top，是 -traces：
`go tool pprof -traces cpu.pprof`
xxxx.func1.1
  → context.(*cancelCtx).Done

栈只有这两层。这一点信息量最大：一个每轮都要调 playwright 的循环，栈里居然没有任何 websocket/playwright 帧 —— 说明那条 default 分支一次都没执行到。到这里已经能反推出「select 一直命中某个恒就绪的 case」了。

selectnbrecv 是 select 带 default 的专用运行时函数，进一步坐实了是非阻塞 select；cancelCtx.Done() 内部就是 atomic.Value.Load，解释了第二热的那一行。

## 回到源码验证机制

func1.1 这个符号名的含义是：xxxx 里第 1 个闭包（返回值）里的第 1 个闭包 —— 也就是那个 go func(){}。

但 $GOMODCACHE 里的 project 源码对不上（没有内层闭包）。查构建信息：

```bash
go version -m /opt/xxxx
#   dep  xxxx  (devel)     ← go.work 指向本地checkout
#   build -gcflags="all=-N -l"                   ← 顺带发现的调试构建
```

(devel) 说明走的是 go.work 本地目录，找到 xxxx，源码就对上了：case <-waitCtx.Done(): 是个空分支。

最后一步是确认语义：select 的 default 只在所有 case 都未就绪时才走。ctx.Done() 一旦关闭就永久就绪，于是循环退化成 for { <-waitCtx.Done() } —— 和 profile 里看到的栈完全一致。

可复用的点

- 先看 utime vs stime 再决定用什么工具，能省掉大量试错方向。
- -traces 比 -top 有用：top 告诉你哪个函数热，traces 告诉你它没在调用什么，缺失的帧往往才是证据。
- 用数量级交叉验证：/proc 算出 3.83 核 vs profile 的 485%，两个独立来源对上了才敢下结论。
- go version -m 确认二进制的真实来源，尤其是有 go.work / replace 的时候，别对着 module cache 的源码看。
