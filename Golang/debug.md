# dlv
## attach
```powershell
dlv attach (get-process "processname without .exe").Id --continue --accept-multiclient --headless --listen=localhost:2345 --api-version=2
```
- `--continue`：连接后不会让程序停止在main，而是继续运行
	- `--accept-multiclient` `--continue`必须要这个
- `--headless --listen=localhost:2345`：开启api模式，允许远程监听
	- 直接执行不会在后台运行
## connect
- `dlv connect localhost:2345`
	- 进入交互debug模式，exit会停止connect
		- exit后会询问关闭dlv，若是关闭问关闭进程（即运行的程序进程）
		- Goland会在关闭dlv时强制杀死进程
		- 因此如果想关闭dlv，就手动connect再exit