
# windows netsh
这是 Windows 系统内置的命令，最轻量且无需额外安装软件
- **以管理员身份运行 CMD，执行：**
```cmd
netsh interface portproxy add v4tov4 listenaddress=192.168.123.88 listenport=80 connectaddress=127.0.0.1 connectport=8080

netsh interface portproxy add v4tov4 listenport=80 listenaddress=0.0.0.0 connectport=8080 connectaddress=(wsl hostname -I)
```
**常用命令：**
- 查看所有规则：`netsh interface portproxy show all`
- 删除规则：`netsh interface portproxy delete v4tov4 listenaddress=192.168.123.88 listenport=80`
- 清空所有规则：`netsh interface portproxy reset`

**⚠️ 注意事项：**
- 仅支持 **TCP** 协议，不支持 UDP
- 需要确保 `IP Helper` 服务正在运行
- 规则是永久性的，重启后仍然有效
- 如果 `192.168.123.88` 不是本机实际 IP，可能需要先添加虚拟网卡或确保该 IP 可用