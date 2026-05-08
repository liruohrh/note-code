
```powershell
# 尝试优雅关闭
# -WindowStyle必须不是Hidden, 比如Minimized
$proc.CloseMainWindow() | Out-Null

# 事件（轻量，如果不用数据，可以用这个）
$eventName = "shutdown_pid_$($proc.Id)"
$event = [System.Threading.EventWaitHandle]::OpenExisting($eventName)
$event.Set()
$event.Close()

# named pipe
$pipe = New-Object System.IO.Pipes.NamedPipeClientStream(".", $eventName, [System.IO.Pipes.PipeDirection]::Out)
$pipe.Connect(1000)
$pipe.Close()
```


```go
func waitShutdownPipe(pid int) {
	// github.com/Microsoft/go-winio
	ln, _ := winio.ListenPipe(fmt.Sprintf("\\\\.\\pipe\\shutdown_pid_%d", pid), nil)
	defer ln.Close()
	conn, _ := ln.Accept()
	defer conn.Close()
	fmt.Printf("shutdown pipe received\n")
}

func waitShutdownEvent(pid int) {
	// golang.org/x/sys/windows
	name, _ := windows.UTF16PtrFromString(fmt.Sprintf("shutdown_pid_%d", pid))
	event, _ := windows.CreateEvent(nil, 0, 0, name)
	defer windows.CloseHandle(event)

	windows.WaitForSingleObject(event, windows.INFINITE)
	//sc <- syscall.SIGTERM
	fmt.Printf("shutdown event received\n")
}
```