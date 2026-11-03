
x11服务器负责渲染，x客户端（虚拟桌面）发送画图指令。
x11vnc会把x11服务器放在虚拟桌面位置并渲染，vnc客户端（远程连接App）则是显示图片，
否则，客户端是使用x11服务器进行渲染，接收x客户端请求。
简单来说，就是x11vnc是服务端渲染，x11服务器是客户端渲染。

虚拟桌面->x11服务器->vnc直接在宿主机渲染->vnc客户端（用户远程控制）。

创建虚拟桌面：xvfb
启动x服务器宿主机绘图：x11vnc
Xvnc（TigerVNC） = xvfb + x11vnc
连接vnc服务器：tigervnc-viewer



- 端口转发：`ssh -L [localaddr:]port:remoteadd:port target` 
  - 注意，这个ssh终端会照常打开，可以不用管


## 第 0 层：物理 / 虚拟显示设备

**名称**：显示输出（Display Output）
**实现**：
- Linux：`Xvfb`（内存帧缓冲）、`Weston --backend=headless`（Wayland 无头合成器）
- Windows：**IDD（Indirect Display Driver）** —— UMDF v2 用户态驱动，经 `IddCx` 向系统注册虚拟显示器
- macOS：Apple Silicon 自动创建虚拟显示；Intel Mac 需 **HDMI Dummy Plug** 欺骗 GPU


## 第 1 层：显示服务 / 图形协议

**名称**：窗口系统（Window System）
**实现**：
- X11 路线：`Xvfb` 作为 X Server 的内存实现，客户端经 `DISPLAY=:99` 接入
- Wayland 路线：`Weston` headless、`labwc`、`wayvnc` 等
- 关键区别：X11 显示服务与窗口管理分离；Wayland 合成器将两者合一


## 第 2 层：窗口管理 / 桌面环境

**名称**：窗口管理器（Window Manager, WM）
**实现**：
- **堆叠式**：`Openbox`、`Fluxbox`（窗口可重叠，轻量）
- **平铺式**：`i3`、`Awesome WM`、`bspwm`（自动网格排列，适合自动化）
- **完整桌面环境**：`XFCE`、`LXDE`、`LXQt`（带面板、文件管理器，较重）
- Xvfb 本身**不管理窗口**，WM 是让对话框焦点、堆叠行为正常的**事实必需品**


## 第 3 层：远程传输协议

**名称**：远程显示协议（Remote Display Protocol）
**实现**：
- **VNC / RFB**：像素级帧缓冲差异传输。代表：`x11vnc`、`TigerVNC`、`KasmVNC`（WebP 压缩）
- **RDP**：指令级渲染传输，带宽通常低于 VNC。代表：`xrdp`、`FreeRDP`
- **WebRTC**：编码视频流（H.264/VP8/VP9），自适应带宽，原生音频。代表：`Selkies-GStreamer`、`Neko`
- **WebSocket**: [voxl](https://github.com/tembo/voxl) - fps相对高、相对省流

## 第 4 层：客户端 / 接入方式

**名称**：客户端（Client）
**实现**：
- VNC 客户端：`RealVNC Viewer`、`TigerVNC Viewer`、`noVNC`（浏览器，经 WebSocket）
- RDP 客户端：Windows 自带“远程桌面连接”、`FreeRDP`
- WebRTC：**原生浏览器**，无需插件


## 跨平台速查

| 层 | Linux | Windows | macOS |
|---|---|---|---|
| **显示设备** | Xvfb / Weston headless | IDD 虚拟显示驱动 | Apple Silicon 自动 / Intel 需 Dummy Plug |
| **窗口管理** | Openbox / i3 / XFCE | DWM（系统内置） | WindowServer（系统内置） |
| **传输** | VNC / WebRTC | **RDP**（带宽效率最高） | VNC（屏幕共享） |
| **核心差异** | 显示服务与 WM 分离，可选组合多 | IDD 在内核/驱动层“造”显示器 | 无头支持依赖硬件代际，灵活性最低 |