# 某些应用可能出无法同时使用wayland应用
- https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland#Chromium_.2F_Electron
- 解决方法
- electron/浏览器：`xxx --enable-features=UseOzonePlatform --ozone-platform=wayland --enable-wayland-ime`  
	- 不知道为什么，必须在启动器里加这个参数
	- 在打包前，脚本里的命令后面加却不行，但是又不知道为什么在appimagelauncher的applications目录下生存时自动生成的2个启动应用菜单又可以，如果不在这里就又不可以