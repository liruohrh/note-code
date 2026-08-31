
# 命令
```bash
# 生成2个密钥对
wg genkey | tee wg0.pri | wg pubkey > wg0.pub


# linux命令
sudo wg-quick up wg0
# 开机自启
sudo systemctl enable wg-quick@wg0
# 查看状态
sudo wg show
```


# 配置
- Interface 表示本机创建的虚拟网卡（注意用的是24，是一个网络）
- Peer表示连接的主机（注意用的是32，是一个ip），一个配置文件可以有多个

```conf
[Interface]
PrivateKey = 6J8pzGAfTCxpxYgrnGAtCLlE7B4rUhR5WODkIJbli2c=
ListenPort = 51820
Address = 10.0.0.1/24

[Peer]
PublicKey = HgjexlF6mwSTcj+thDm+PWrzBecwDoGqd7XbAvqIEBQ=
AllowedIPs = 10.0.0.2/32
Endpoint = 192.168.0.100:51820
PersistentKeepalive = 25
```
