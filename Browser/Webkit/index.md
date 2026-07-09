
# 基本信息

- https://docs.webkit.org/
- https://trac.webkit.org/wiki
- https://docs.webkit.org/Ports/Introduction.html

## 分支
- safari-7624.1.16.11-branch：Apple Safari 对应版本的 release branch（冻结主线 + 维护分支）
## tag
- Safari-533.10   Safari浏览器
- WebKit-7613.2.6    WebKit引擎
- releases/Apple/Safari-10-iOS-10.0、releases/Apple/Safari-8.0.8-macOS-10.10.5    Apple 官方 release snapshot（绑定 OS + Safari 版本的源码快照）
- releases/Apple/Safari-Technology-Preview-144     新特色实验渠道
- webkitgtk-2.36.4，linux GUI webkit分支
	- GTK port版本、Linux 桌面浏览器（Epiphany 等）、 GTK 应用
	- [webkitgtk](https://docs.webkit.org/Ports/WebKitGTK%20and%20WPE%20WebKit/TipsForMaintainers.html#advisories)
- wpewebkit-2.44.4，linux embedded && headless webkit分支
	- WPE（Web Platform for Embedded）版本、Smart TV、车载系统、IoT 浏览器

## 版本

- 比如
	- Webkit版本：Webkit 26.4
		- 
	- GTK版本：webkitgtk2.53.3
		- `~/.cache/ms-playwright/webkit-2306/minibrowser-gtk/MiniBrowser --version`
	- playwright webkit补丁版本：playwright webkit v2306
		- `playwright-cli install-browser webkit --dry-run`
# Ports
## windows
- https://docs.webkit.org/Ports/WindowsPort.html
- https://webkit.org/building-webkit-on-windows/
## linux
### gtk(headed)
- https://webkitgtk.org/
- https://github.com/Igalia/webkit-container-sdk

#### 类似于chrome:// 的浏览器inspect
- `about:minibrowser  about:data   about:itp ` 
#### webkitgtk官方编译的
https://web-platform-tests.org/running-tests/webkitgtk_minibrowser.html
https://webkitgtk.org/built-products/x86_64/release/beta/MiniBrowser
- sudo apt install webkit2gtk-driver
- /usr/lib/x86_64-linux-gnu/webkit2gtk-4.1/MiniBrowser
- 其实下载libwebkit2gtk-4.1-0即可，此包才是MiniBrowser

### wpe(headless,embedded)
- https://wpewebkit.org/
- https://github.com/WebPlatformForEmbedded
- https://github.com/Igalia/meta-webkit/wiki/WPE

#### 2种构建 libwpe vs wpeplatform
- libwpe 是"WebKit + 薄 ABI + 外挂 backend .so"的老三件套
- WPEPlatform 是 WebKit 把显示/输入/缓冲/后端**全部内建成一个 GTK 式原生库**的新模型(类似 GTK4 内置各 backend)
	- 最新版默认
	- ENABLE_WPE_PLATFORM
## playwright
- [# [Question] How does Playwright track, build and embed the open source WebKit?](https://ray.run/discord-forum/threads/200734-question-how-does-playwright-track-build-and-embed-the-open-source-webkit#:~:text=firefox%20%E9%9C%80%E8%A6%81%E5%AF%B9%E5%85%B6%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7%E5%8D%8F%E8%AE%AE(juggler)%E8%BF%9B%E8%A1%8C%E8%A1%A5%E4%B8%81%E3%80%82)
- [playwright v1.6.2 还有介绍一点补丁的开发和构建流程](https://github.com/microsoft/playwright/tree/v1.6.2/browser_patches)
- [webkit 构建平台](https://build.webkit.org/)
- [slack 交流平台](https://app.slack.com/client/T06G50708/CU84Q46JZ)
- [Building webkit for windows?](https://www.reddit.com/r/Playwright/comments/1mq57n1/building_webkit_for_windows/)
- 不支持 webkit patch 的贡献
	- [https://github.com/microsoft/playwright/issues/28976](https://github.com/microsoft/playwright/issues/28976)
	- [https://github.com/microsoft/playwright/issues/29005](https://github.com/microsoft/playwright/issues/29005)

### 补丁逻辑
- playwright浏览器下载链接： 如 https://cdn.playwright.dev/dbazure/download/playwright/builds/webkit/2306/webkit-ubuntu-22.04.zip
	- `builds/webkit/2276/webkit-win64.zip`
	- `builds/webkit/2306/webkit-ubuntu-24.04.zip`
	- 下载路径：packages\playwright-core\src\server\registry\index.ts，DOWNLOAD_PATHS
	- 浏览器版本：packages\playwright-core\browsers.json
	- 上游版本：browser_patches\webkit\UPSTREAM_CONFIG.sh
- playwright浏览器更新逻辑：
	- [私有仓库 playwright-browsers](https://github.com/microsoft/playwright-browsers) 的自动化修改 packages\playwright-core\browsers.json，如 [feat(webkit): roll to r2327](https://github.com/microsoft/playwright/pull/41684)  
	- [全部更新PR](https://github.com/microsoft/playwright/pulls?q=is%3Apr+Build+has+full+platform+coverage+-+check+that+all+tests+pass+there)  
	- 最好还是使用playwright版本中第一个出现此浏览器版本的commit时的补丁，该commit时的补丁到playwright版本发布时的补丁不知道是否有无更新，  
		按道理是不会更新的，更新就会同时更新浏览器版本和补丁。  
		因此直接用playwright版本发布时的浏览器补丁即可。
	- v1.25.2还保留比较完整的构建和补丁，v1.26.0被正式转为补丁文件方式

---

添加补丁
- `git apply browser_patches\webkit\patches\bootstrap.diff`
- 复制browser_patches\webkit\embedder\Playwright到Tools\Playwright
### release
- 编译完后对可执行文件 执行 `strip xxx` ，库`strip --strip-unneeded xxx`
### 源码分析

- pageConfiguration：这个是在Tools/Playwright里创建，然后通过IPC共享的
- MainWindow
	- 设置pageConfiguration，且创建新的prefs
		- 因此注意pageConfiguration可以只设置一次，但是prefs必须每次都设置
		- 或者在Source\WebKit\UIProcess\WebPreferences.cpp WebPreferences::createWithLegacyDefaults中设置默认的prefs（更推荐，但如果有很多外在因素被覆盖）
			- 但其实最方便的方法是在设置处禁止设置自己配置的prefs，那些更新通知可以不用管
	- 在哪里会new：
		- ui new window
		- inspector的页面创建，调用WebKitBrowserWindow::createPageCallback

# 调试

- [例子](./问题记录#WebRTC mDNS 函数参数求值顺序问题)

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
