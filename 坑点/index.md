

# Windows快速启动导致的Windows服务恢复时错误地读取到0点

1. Windows 快速启动，把服务进程内存快照保存，包括 cron 的 goroutine 和 timer
2. 开机恢复快照，进程继续运行
3. **恢复的瞬间系统时钟是 `00:00:00`**（硬件时钟还没同步）
4. Go runtime 恢复 timer，发现 `time.Since(deadline)` 已超时，立即触发
5. `timer.C` 吐出的时间戳就是触发瞬间的系统时间：`00:00:00`
6. cron 用这个值更新 `now`，日志打印出 `now=00:00:00`
7. **但日志框架用的是 `time.Now()`**，此时系统时钟已经跳回正常时间，所以日志时间戳显示 `08:59:36`

- timer是错误的在此时，time.Now

# Windows文件路径长度
- Computer Configuration  → Administrative Templates  → System  → Filesystem  → Enable Win32 long paths = Enabled
- git需要主动开启才行：`git config --global core.longpaths true`
- 删除长路径文件：`Remove-Item -Path "\\?\D:\ws\lib\webkit-ws\webkit_5e02fd1\WebKitBuild" -Recurse -Forces`
- 