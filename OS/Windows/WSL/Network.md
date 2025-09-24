- [Windows 访问WSL网络](https://learn.microsoft.com/zh-cn/windows/wsl/networking#accessing-linux-networking-apps-from-windows-localhost)：直接用localhost、127.0.01

- [WSL 访问Windows网络](https://learn.microsoft.com/zh-cn/windows/wsl/networking#accessing-windows-networking-apps-from-linux-host-ip)： 通过命令`ip route show | grep -i default | awk '{ print $3}'` 获取Windows的IP地址，然后使用该IP进行访问Windows网络。
	- [Windows 11 22H2开始可以启用镜像网络，WSL就也可以直接访问windows服务](https://learn.microsoft.com/zh-cn/windows/wsl/networking#mirrored-mode-networking)



# Proxy
- [WSL 配置](https://learn.microsoft.com/zh-cn/windows/wsl/wsl-config#main-wsl-settings)
	- 自动使用系统代理[wsl].autoProxy=true(但是好像不太行)
```bash
PROXY_PORT=7890
WIN_HOST=$(ip route show | grep -i default | awk '{ print $3}')
export WIN_HOST=$WIN_HOST
export http_proxy=http://$WIN_HOST:$PROXY_PORT
export https_proxy=http://$WIN_HOST:$PROXY_PORT
export all_proxy=socks5h://$WIN_HOST:$PROXY_PORT
```