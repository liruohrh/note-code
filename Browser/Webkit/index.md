
# WebKit 版本信息

- 分支
  - safari-7624.1.16.11-branch：Apple Safari 对应版本的 release branch（冻结主线 + 维护分支）
- tag
  - Safari-533.10
    - Safari浏览器
  - WebKit-7613.2.6
    - WebKit引擎
  - releases/Apple/Safari-10-iOS-10.0、releases/Apple/Safari-8.0.8-macOS-10.10.5
    - Apple 官方 release snapshot（绑定 OS + Safari 版本的源码快照）
  - releases/Apple/Safari-Technology-Preview-144
    - 新特色实验渠道
  - webkitgtk-2.36.4
    - GTK port版本、Linux 桌面浏览器（Epiphany 等）、嵌入式 GTK 应用
    - [webkitgtk](https://docs.webkit.org/Ports/WebKitGTK%20and%20WPE%20WebKit/TipsForMaintainers.html#advisories)
  - wpewebkit-2.44.4
    - WPE（嵌入式）版本、Smart TV、车载系统、IoT 浏览器
    - 📌 和 GTK 的关系：
      - 共用 WebKit core
      - 不同 UI backend（Wayland / 嵌入式设备）


# Base
- Webkit 26.4   (playwright webkit v2306) 
	- webkit的版本，playwright补丁版本
	- webkitgtk2.53.3：gtk版本
- WebKit 26.4  (playwright webkit v2276)

- `https://cdn.playwright.dev/dbazure/download/playwright`
	- `builds/webkit/2276/webkit-win64.zip`
	- `builds/webkit/2306/webkit-ubuntu-24.04.zip`
	- packages\playwright-core\src\server\registry\index.ts，DOWNLOAD_PATHS
	- packages\playwright-core\browsers.json
- 跟踪webkit commit与playwright补丁版本方法
	- 查看对应browser_patches\webkit\UPSTREAM_CONFIG.sh commit时的packages\playwright-core\browsers.json里的版本
	- 但注意，跟踪revision即可，不用跟踪revisionOverrides（特定os的版本）
	- 但也不完全这样，  比如 2272（"2026-03-24 16:57:06 +0000"）-2287（ "2026-05-05 10:28:01 -0700"） 都是webkit 6b34ac51510516bd6a3ec2f5edc97413758d3ab1（"2026-03-30T18:00:14-07:00"），下个版本修改于c8604ecd97ffcc50b6c269df544b7cc36f258d3b（"2026-05-07T10:14:30-07:00"）
		- 2276 "2026-04-03 07:50:45 -0700"
		- 因此严格来说是2276版本才对，不管感觉不用这么准确，就要修改webkit base commit时的playwright webkit补丁版本即可


# 功能


## 远程调试页面和自动化

- Tools/Scripts/build-webkit是默认开启的，除非传递参数`--no-experimental-features`
	- 不需要自己在 `/CMakeLists.txt`加入`option(ENABLE_EXPERIMENTAL_FEATURES "Enable experimental features" ON)`


## WebRTC
### GStreamer-WebRTC 
散装组合方案
ICE -> libnice 、librice
DTLS -> OpenSSL/GnuTLS  
Media -> GStreamer （多媒体插件系统）
Codec -> 插件

---

它是 Igalia 给 WebKitGTK/WPE 做的、基于 GStreamer(webrtcbin)的 WebRTC 实现，用来替代 Google 的 libwebrtc。

存在的优势

| GStreamerWebRTC 的优点 | 说明                                                                        |
| ------------------- | ------------------------------------------------------------------------- |
| 摆脱 libwebrtc 巨型依赖   | libwebrtc 是 394M 的 Google 源码，难编、更新快、体积大；GStreamerWebRTC 复用系统现成的 GStreamer |
| 媒体栈统一               | WebKitGTK 播放视频本来就用 GStreamer，WebRTC 也走它 → 编解码/管线统一，而非 libwebrtc 自带一套媒体引擎  |
| 硬件加速 / 系统编解码        | 直接用 GStreamer 的 VA-API 等硬件编解码、系统 codec                                    |
| 发行版友好               | 动态链系统库(gstreamer/libnice)，安全更新只需升系统库，不用重编整个 WebKit                        |

 缺陷（不选用它的核心原因）
它面世时间短、成熟度不足，功能完整性与跨端互操作性均不如 libwebrtc，各类 Bug 更多—— librice 堆崩溃就是典型案例。
而 libwebrtc 是 Chrome 同款底层实现，经过海量线上场景验证，跨平台互通兼容性最优。

---

GStreamer、librice是（只是说我在2026发现）开发团队推进的方向，但是不稳定（比如无法全包大多数OS都可用，甚至连主流的Ubuntu24.4都有问题，会崩溃）


### LibWebRTC
Chromium统一方案