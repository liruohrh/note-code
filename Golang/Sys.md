# Signal

- 优雅关闭，监听SIGINT（ctrl+c，键盘中断）、SIGTERM（`kill -15 pid`默认，优雅终止）、SIGKILL（`kill -9 pid`默认，强制杀死）

- GoLand、Jetbrains产品的测试好像都是SIGKILL，导致程序无法接收信号，只能自己找到pid进行SIGTERM
	- main则是发生SIGINT
	- unix 则都是SIGINT

```go
signalChan := make(chan os.Signal, 1)  
signal.Notify(signalChan,  
    syscall.SIGINT,  
    syscall.SIGKILL,  
    syscall.SIGTERM, 
)  
fmt.Printf("exit with %v", <-signalChan)
```


- windows上 `taskkill /pid xxx`无法被signal监听
	- `taskkill /pid`发送 `WM_CLOSE` 给窗口 无窗口，收不到
	- `taskkill /f /pid`调用 `TerminateProcess()` 强杀，无法处理
- 用库`github.com/containers/winquit`兼容
	- 监听windows版的SIGTERM：  NotifyOnQuit（返回bool）、SimulateSigTermOnQuit（返回Signal.SIGTERM）
	- 发送windows版的SIGTERM：
		- `RequestQuit(pid)`发送 `WM_CLOSE` 消息，发完就返回，不等待`QuitProcess(pid, duration)`发送 `WM_CLOSE`，等待进程退出，超时则强杀
- `os.Process#Kill`
	- windows：exit status 1
	- unix：发送SIGKILL
	- 如果是cmd.Process，则command.Run会返回exec.ExitError（可以获取进程信息，错误信息）
	- 当然可以选择自己发送信号，如`process.Signal(syscall.SIGTERM)`
		- 还可以`process.Wait`
		- 但如果发送SIGKILL会立刻杀死进程，且不等待