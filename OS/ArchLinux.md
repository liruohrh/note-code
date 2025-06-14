# 网络
- 输出网卡：`ip link`
- 扫描wifi
	- 安装`iwd` 会重命名网卡名为wlan0
	- 查看无线网卡：`iwctl station list`
	- 扫描wifi：`iwctl station wlan0 get-networks`
	- 连接wifi：`iwctl station wlan0 connect get-networks`
- wpa
	- `wpa_passphrase SSID PASSWD > xxx.conf`
	- `wpa_supplicant -c xxx.conf -i interfaceName &`
	- `dhcpcd`
- 无论是否在DE,在安装后都推荐用NetworkManager.service管理
	- 在DE中，会有菜单栏、系统设置的wifi管理
	- `sudo systemctl enable  NetworkManager`
	- `sudo systemctl start  NetworkManager`
# 多媒体
- https://wiki.archlinuxcn.org/wiki/建议阅读#多媒体
- 

## 声音
- 如果没有，检查有无`/lib/firmware/intel/sof`，没有仅安装 `sudo pacman -S sof-firmware`

# AUR(Arch User Repository 社区软件仓库)
- yay：基于pacman的AURpackage管理工具
- 自行安装
```
git clone https://aur.archlinux.org/yay.git
cd yay
export GOPROXY=https://goproxy.cn,direct
makepkg -si
```
- 不要以root执行，避免破坏系统
- 推荐package
	- appimagelauncher：让appimage集成到DE中，而不是仅仅只是一个可执行文件
	- google-chrome



