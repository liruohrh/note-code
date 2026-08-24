# 名词
## 显示服务器协议DSP（Display Server Protocol）(Graphics Platform)
- **X11（Xorg）**：传统的显示服务器协议，历史悠久，但设计复杂。
- **Wayland**：（compositor+DS）现代的显示服务器协议，逐渐取代 X11。


- **窗口管理器（Window Manager）**：负责窗口的移动、缩放、装饰边框、工作区切换（比如 X11 下的 mutter、kwin、i3、xmonad，本质上也是一个特殊的 X client）。
- **合成器（Compositor）**：负责窗口内容的最终合成、特效（阴影、透明、动画）。在 X11 下这是独立于 X server 的一个进程（同样是 client 身份，通过 XComposite/XDamage 扩展跟 server 打交道）；在 Wayland 下则直接就是 server 本身。
- **面板、任务栏、文件管理器、设置中心**等等——这些都是普通的 X11/Wayland **client**，只是被打包成一整套统一体验，叫做"某某桌面环境"。

- 当前DS`$DISPLAY=:0`   `hostname:displaynumber.screennumber`
### xauth认证
- xauth list

### 远程Client连接本地Server

- `ssh -Y xxx` ssh转发

- 本地Server
	- /etc/ssh/sshd_config   X11Forwarding=yes
- 远程Client
	- /etc/ssh/sshd_config   X11UseLocalhost=yes

- 执行如 `firefox &`
	- 如果不行，可能是snap等封装环境不支持


或者用TigerVNC

### X11 Virtual Framebuffer：虚拟DS
```bash
Xvfb :99 -screen 0 1280x800x24 & DISPLAY=:99 GDK_BACKEND=x11 xxx &
```


## 窗口管理器 WM（Windows Manager）

- **堆叠式窗口管理器**（stack）：窗口可以重叠，如 Openbox、Fluxbox。
    
- **平铺式窗口管理器**（tiled）：窗口自动排列，不重叠，如 i3wm、Sway。
- 但注意，VM往往2种都有实现
- [i3wm: Jump Start (1/3)](https://www.youtube.com/watch?v=j1I63wGcvU4)
- [Sway on Arch Linux: 2023 Edition (From Scratch)](https://www.youtube.com/watch?v=QAmTUkzpIiM)
    

## 桌面环境DE（Desktop Environment）
- 通常都会集成现有的显示服务器协议、窗口管理器 

- **完整桌面环境**：包含窗口管理器、面板、应用程序等，如 GNOME、KDE Plasma。
    
- **轻量级桌面环境**：仅包含基本组件，如 LXDE、XFCE。

