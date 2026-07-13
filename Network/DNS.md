
# Linux

四种设置方式
- NetworkManager nmcli
- systemd-resolved resolvectl status
	- global是systemd-resolved配置（fallback）
		- `/etc/systemd/resolved.conf`   `sudo systemctl restart systemd-resolved`
	- 网卡如enp3s0，Current是用过的（那个好用用哪个）
	- 如果要确认来源的时候，最好不要设置global，只用nmcli设置
- /etc/resolv.conf
	- nameserver 127.0.0.53  就是用stemd-resolved
- 应用程序(getaddrinfo、curl、浏览器...)


| 提供商               | IPv4                           |
| ----------------- | ------------------------------ |
| Google Public DNS | 8.8.8.8 / 8.8.4.4              |
| Cloudflare        | 1.1.1.1 / 1.0.0.1              |
| Quad9             | 9.9.9.9 / 149.112.112.112      |
| 阿里云 Public DNS    | 223.5.5.5 / 223.6.6.6          |
| 腾讯 DNSPod         | 119.29.29.29 / 182.254.116.116 |
| 百度 DNS            | 180.76.76.76                   |
114.114.114.114  用不了，不要用

## 查看&修改
- 重启
`sudo nmcli connection up netplan-enp3s0`

```bash

# 查看  enp3s0 是网卡名
nmcli connection show netplan-enp3s0
nmcli -g ipv4.dns connection show netplan-enp3s0


# 自动用路由器的
sudo nmcli connection modify netplan-enp3s0 ipv4.ignore-auto-dns no ipv4.dns ""

# 自定义DNS
sudo nmcli connection modify netplan-enp3s0 ipv4.dns "192.168.123.1 223.5.5.5 119.29.29.29"
```

## DNS测试
- 清空缓存：`sudo resolvectl flush-caches`

### 用系统DNS测试 dig google.com
- 最后会显示 `;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)`
	- systemd-resolved需要看其日志才知道究竟哪个

- `sudo resolvectl log-level debug`
- `journalctl -fu systemd-resolved`
	- `Using DNS server xxx for transaction ...`

### 指定DNS测试 dig @8.8.8.8 google.com

### curl
- `curl -v --resolve dns.google:443:8.8.8.8 https://dns.google/resolve?name=www.baidu.com`
	- --resolve添加dns缓存
`curl -v --doh-url https://1.1.1.1/dns-query https://www.google.com`
`curl -v --doh-url https://1.1.1.1/dns-query https://www.google.com`
## 一个小测试

- https://browserleaks.com/dns
- 路由器代理：规则代理+UDP拦截
	- 注意，因此会泄露DNS查询给国内运营商
- 主机代理：
	- 注意，如果clash要开启全局代理，会因为访问国内ip就走国内ip导致dns泄露
	- windows：
		- 关闭clash DNS拦截，无法上网，打开则可以
- 感觉不能这样，在linux里完全不知道到底是怎么生效的，claude说我写的webkit linux 没有实现doh，但是测试结果总是表明实现了
	- DNS拦截+规则：有国内的 ISP
	- DNS拦截+全局：全是AWS ISP
	- 无DNS拦截+规则：全是AWS ISP
	- 无DNS拦截+全局：全是AWS ISP
	- 最重要的是我配置的dns是Google的，却老是出现AWS
# 浏览器的DNS
- chrome： 设置、安全、安全DNS
- firefox: 设置、安全、安全DNS
- safari： 无