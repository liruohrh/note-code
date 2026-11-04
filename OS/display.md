
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

Linux 上造一块"假屏"，**本质只有两类**，区别是你在哪个世界：

| | X11 世界 | Wayland 世界 |
|---|---|---|
| 谁提供这块屏 | **Xvfb** —— 一个 X 服务器，屏幕就是内存里一块缓冲 | **合成器 + headless 后端** —— 输出不接任何真实显示器，同样画到内存里 |
| 窗口管理 | 分开的，要另配 WM（openbox…） | 合成器自己兼任，不需要额外的 WM |
| 应用怎么接进来 | `DISPLAY=:99`，说 X11 协议 | `WAYLAND_DISPLAY=wayland-1`，说 Wayland 协议 |
| 能不能用 GPU | ❌ Xvfb 不实现 DRI3，客户端拿不到设备 fd，只能退 llvmpipe | ✅ 合成器自己开 render node |

"headless 后端"就是 Xvfb 那个"内存帧缓冲"的 Wayland 版说法 —— 合成器平时要把画面输出到
显示器（DRM）、X 窗口或另一个 Wayland 窗口，headless 就是哪儿都不输出，只留在内存里。

Wayland 合成器这边又分两家，**挑哪家决定了能配什么远程方案**：

- **weston**：官方参考实现，后端最全（`x11` / `drm` / `headless` / `vnc` / `rdp`），
  但只实现官方协议 —— `wayvnc` 要的 `wlr-screencopy` 它没有。
- **wlroots 系**（`cage` 单应用 kiosk、`sway` 平铺、`labwc`）：基于 wlroots 库，
  自带 `wlr-screencopy`、虚拟键鼠等扩展协议，`wayvnc` 只能配它们。

实测同一台机器、同一个满屏动画页（100% = 一个核）：

| 虚拟屏 | 同页面 CPU | 备注 |
|---|---|---|
| `Xvfb`（软件渲染） | ≈380% | 页面被 CPU 画一遍、合成器再画一遍 |
| `weston --backend=headless --renderer=gl` | ≈10% | 用上 GPU，但只能截图，配不了 wayvnc |
| `cage` headless + `WLR_RENDERER=gles2` | ≈14.5% | 用上 GPU，且能配 wayvnc 看和接管 |

**其他平台**：
- Windows：**IDD（Indirect Display Driver）** —— UMDF v2 用户态驱动，经 `IddCx` 向系统注册虚拟显示器
- macOS：Apple Silicon 自动创建虚拟显示；Intel Mac 需 **HDMI Dummy Plug** 欺骗 GPU

**帧的两种形态**（下面反复出现）：GPU 画的帧是 **dmabuf**（显存缓冲用一个 fd 跨进程传，不拷像素；
EGLImage 是 EGL 层对它的句柄），CPU 画的帧是 **SHM**（共享内存里的像素数组）。
能不能产出 dmabuf，取决于进程能否打开 **render node**（`/dev/dri/renderD128`）——
拿不到 ≠ 没显卡，X 客户端靠 X 服务器的 DRI3 要、Wayland 客户端靠合成器通告，链路不给就只能软件渲染。

### 无头模式的应用：如浏览器

**与 Xvfb 的一句话区别**：Xvfb 是完整的虚拟 X 显示服务器，让“有头应用”以为有屏幕；WPE/Chromium Headless 是浏览器内部的无窗口渲染，直接把离屏帧或 CDP 帧流交给消费端。前者服务整个桌面，后者只服务浏览器自身画面。

#### WPE Headless（WebKit）

**定位**：WPE 的平台后端之一，让 WebKit 在没有原生显示服务器的环境中渲染。

**画面输出**：渲染到离屏缓冲区，通过 **DMA-BUF / SHM** 导出给消费者，例如 GStreamer 管道或自定义 GPU 合成程序。
`WPEViewHeadless` 是每帧 buffer 照常交出去、只是不上屏（源码注释："notifies that each buffer has
been rendered … without producing visible output"），所以**帧一直存在**，
playwright 的 `page.screenshot()` 就是从这里取的。

**传输协议**：
- WPE 本身**不规定统一传输协议**，只负责把原始帧交给上层。
- **WebRTC** 是 WPE 生态中最成熟的实时传输路径，支持 **GstWebRTC** 和 **LibWebRTC** 两种后端，已有 Amazon Luna、Zoo 等产品案例。
- **Screencast** 路径输出逐帧 **JPEG** 图片，Playwright 的 `page.screencast` 已覆盖 WebKit，WebKit 侧上限约 **25 FPS**。
- 也可由消费者自行编码为 **H.264/VP9 over WebSocket**，构建类似 voxl 的自定义流媒体管道。

**抓屏抓不到它**：无头 WPE 不创建任何 X 窗口，`xwininfo -root -tree` 里只有窗口管理器自己，
VNC / voxl 对着那块屏截出来是全黑。要让人能看、能接管只有两条路：走协议（screenshot / screencast），
或者给它一个 **Wayland 合成器**当宿主 —— WPE **没有 X 后端**，
`Source/WebKit/WPEPlatform/wpe/` 下只有 `wayland/`、`drm/`、`headless/`。

**两套 API（名字容易混）**：老的 **legacy**（`libwpe` + `WPEBackend-fdo`）和新的 **WPEPlatform**。
关键差别只有一条：legacy 的窗口后端**只认 dmabuf**，拿到 SHM 帧直接丢弃，所以没 GPU 就出不了画面；
WPEPlatform 两种都认，而且自己用 GBM 开 render node，不依赖合成器给设备。
playwright 自带的 webkit 用哪一套是会变的（1.52～1.62 只有 legacy，1.63 起只剩 WPEPlatform），
判断办法：`nm -D libWPEWebKit-2.0.so.1 | grep wpe_display_wayland_new` —— 有这个符号就是 WPEPlatform
（别查 `wpe-display-wayland` 这类注册名字符串，1.64 起查不到了，但功能还在）。

**特点**：输出原始帧，编码和传输由上层决定；适合嵌入式、云游戏、自定义流媒体管道。

#### Chromium Headless

**定位**：Chrome 的无窗口运行模式，浏览器内部管理帧缓冲，不创建平台窗口，也不需要 Xvfb。

**画面输出**：主要通过 **CDP screencast** 输出逐帧 **JPEG** 图片；也可由工具解码后写入共享内存，或封装成 WebRTC/H.264 流。

**传输协议**：
- 核心是 **Chrome DevTools Protocol（CDP）** 的 `Page.startScreencast` / `Page.screencastFrame`。
- 每帧是**独立 JPEG 编码的图片**，通过 **WebSocket** 按 DevTools 协议推送，不是视频流。
- 消费端可解码后写入 **POSIX 共享内存**（如 `wbb`），或转封装为 **WebRTC/H.264**（如 `vscreen`）。
- 带宽效率低于 H.264 视频流方案，因为每帧独立压缩，不复用帧间冗余。

**特点**：适合自动化、截图/PDF、爬虫、CI 测试；screencast 本质是图片流，只覆盖浏览器自身，不提供完整桌面环境。


## 第 1 层：显示服务 / 图形协议

**名称**：窗口系统（Window System）
**实现**：
- X11 路线：`Xvfb` 作为 X Server 的内存实现，客户端经 `DISPLAY=:99` 接入
- Wayland 路线：`Weston`、wlroots 系（`cage`、`sway`、`labwc`）
- 关键区别：X11 显示服务与窗口管理分离；Wayland 合成器将两者合一
- **选哪个还影响 GPU 和能配什么远程方案**：`Xvfb` 只能软件渲染（见第 0 层）；
  wlroots 系能用 GPU，而且只有它支持 `wlr-screencopy` / 虚拟键鼠这些协议，
  所以 `wayvnc` 只能配 wlroots（挂 Weston 会直接报 "Screencopy protocol not supported"）


## 第 2 层：窗口管理 / 桌面环境

**名称**：窗口管理器（Window Manager, WM）
**实现**：
- **堆叠式**：`Openbox`、`Fluxbox`（窗口可重叠，轻量）
- **平铺式**：`i3`、`Awesome WM`、`bspwm`（自动网格排列，适合自动化）
- **完整桌面环境**：`XFCE`、`LXDE`、`LXQt`（带面板、文件管理器，较重）
- Xvfb 本身**不管理窗口**，WM 是让对话框焦点、堆叠行为正常的**事实必需品**
- Wayland 这边没有"单独的 WM"这一层：合成器自己就管窗口。`cage` 是单应用 kiosk 式
  （只把一个程序铺满屏），`sway` / `labwc` 才是常规多窗口


## 第 3 层：远程传输协议

**名称**：远程显示协议（Remote Display Protocol）
**实现**：
- **VNC / RFB**：像素级帧缓冲差异传输。X11 这边：`x11vnc`、`TigerVNC`、`KasmVNC`（WebP 压缩）；
  Wayland 这边：`wayvnc`（**只服务 wlroots 系合成器**，默认无认证，建议只绑回环 + ssh 转发）
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