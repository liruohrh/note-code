
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

### 无头模式的应用：如浏览器

**与 Xvfb 的一句话区别**：Xvfb 是完整的虚拟 X 显示服务器，让“有头应用”以为有屏幕；WPE/Chromium Headless 是浏览器内部的无窗口渲染，直接把离屏帧或 CDP 帧流交给消费端。前者服务整个桌面，后者只服务浏览器自身画面。

#### WPE Headless（WebKit）

**定位**：WPE 的平台后端之一，让 WebKit 在没有原生显示服务器的环境中渲染。

**几个名词**（一帧从画出来到显示，中间换手的环节）：

- **libwpe**：只定义"后端接口"，帧最后去哪由具体 backend 决定。
- **WPEBackend-fdo**（freedesktop.org）：最常用的 libwpe 后端，在浏览器进程里内嵌一个迷你
  Wayland 服务端，把 Web 进程画好的帧**导出**给宿主程序显示 —— 要么 GPU 的 EGLImage，
  要么内存里的 SHM。
- **dmabuf / EGLImage**：内核的缓冲共享机制，一块（显存）缓冲用一个 fd 表示，进程间零拷贝传递；
  EGLImage 是 EGL 层对它的句柄。GPU 渲染的帧走这条。
- **SHM**：普通共享内存里的像素数组，CPU 渲染（llvmpipe）只能走这条。
- **render node**（`/dev/dri/renderD128`）：GPU 的"只算不显示"入口。**拿不到 ≠ 没 GPU** ——
  X 客户端靠 X 服务器的 DRI3 拿设备 fd（`Xvfb` 不支持，所以报 `failed to get driver name for
  fd -1`），Wayland 客户端靠合成器通告的 dmabuf 设备（软件渲染的合成器不通告）。
  链路不给，就算机器上插着显卡也只能退 llvmpipe。

**先分清两套 API**（同一个 WPE，名字容易混）：

| | legacy | WPEPlatform（新） |
|---|---|---|
| 怎么认 | bundle 里有 `libwpe-1.0.so.1` + `libWPEBackend-fdo-1.0.so.1` | `libWPEWebKit-2.0.so.1` 里有 `wpe_display_wayland_get_type` / `wpe_display_headless_new` |
| 后端怎么选 | 编译期挑 `HeadlessViewBackend` / `WindowViewBackend` | 运行期 `WPE_DISPLAY` 环境变量选，外挂模块走 `WPE_PLATFORMS_PATH` |
| 有哪些后端 | fdo（嵌套 Wayland）+ headless | `wpe-display-wayland` / `wpe-display-drm` / `wpe-display-headless`，**没有 x11** |
| 软件渲染能不能出画面 | 不能，窗口后端只认 EGL/dmabuf，拿到 SHM 直接拒（`cannot yet handle wpe_fdo_shm_exported_buffer`） | 能，`WPEViewWayland` 认 `WPE_IS_BUFFER_SHM` |

注意 `WPE_DISPLAY` 要写**注册全称** `wpe-display-wayland`，写成 `wayland` 会报
`Display of type wayland was not found`，看起来像"没编进去"，其实只是名字错了。

**playwright 自带的 webkit 用哪一套，是会变的**（1.52～1.62 只有 legacy，1.63 起 legacy 被删光
只剩 WPEPlatform）。逐版本矩阵、检测与下载脚本都在 itbrowser 仓库：
`docs/playwright-wpe.md` + `scripts/pw-wpe.py`。

**画面输出**：渲染到离屏缓冲区，通过 **DMA-BUF / SHM** 导出给消费者，例如 GStreamer 管道或自定义 GPU 合成程序。
`WPEViewHeadless` 的做法是每帧 buffer 照常交出去、只是不上屏（源码注释："notifies that each
buffer has been rendered … without producing visible output"），所以**帧一直存在**，
playwright 的 `page.screenshot()` 就是从这里取的（`AcceleratedBackingStore::takeSnapshot`）。

**传输协议**：
- WPE 本身**不规定统一传输协议**，只负责把原始帧交给上层。
- **WebRTC** 是 WPE 生态中最成熟的实时传输路径，支持 **GstWebRTC** 和 **LibWebRTC** 两种后端，已有 Amazon Luna、Zoo 等产品案例。
- **Screencast** 路径输出逐帧 **JPEG** 图片，Playwright 的 `page.screencast` 已覆盖 WebKit，WebKit 侧上限约 **25 FPS**。
- 也可由消费者自行编码为 **H.264/VP9 over WebSocket**，构建类似 voxl 的自定义流媒体管道。

**抓屏抓不到它**：无头 WPE 不创建任何 X 窗口，`xwininfo -root -tree` 里只有窗口管理器自己，
VNC / voxl 对着那块屏截出来是全黑。要让人能看、能接管，只有两条路 —— 走协议
（screenshot / screencast，上面那条），或者给它一个 Wayland 合成器当宿主（WPE 没有 X 后端）。
后者在 Xvfb 里套一层 `weston --backend=x11` 就能做到，但页面等于被软件画两遍，比有头 GTK 贵得多；
具体做法、坑和开销对比见 createrlib 的 `docs/虚拟桌面.md`。

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