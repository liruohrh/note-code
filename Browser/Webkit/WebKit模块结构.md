# WebKit 模块结构

## 顶层目录

```
Source/
  ├── bmalloc/         ← 内存分配器
  ├── WTF/             ← C++ 基础库
  ├── PAL/             ← 平台抽象层
  ├── JavaScriptCore/  ← JS 引擎 + WebAssembly
  ├── WebCore/         ← 渲染引擎
  ├── WebGPU/          ← WebGPU 标准实现
  ├── WebKit/          ← 多进程壳
  ├── WebKitLegacy/    ← 旧版 WebKit API 层
  ├── WebDriver/       ← WebDriver 实现
  ├── WebInspectorUI/  ← Inspector 前端 (HTML/JS/CSS)
  ├── ThirdParty/      ← 第三方库 (libwebrtc, ANGLE, ICU 等)
  └── cmake/           ← CMake 配置文件
```

## 模块依赖关系

从 `Source/WebKit/CMakeLists.txt:749` 得到的编译链接依赖:

```cmake
set(WebKit_FRAMEWORKS
    JavaScriptCore
    PAL
    WTF
    WebCore
    bmalloc
)
```

```
                           ┌──────────┐
                           │ bmalloc   │ (内存分配器)
                           └─────┬─────┘
                                 │
                           ┌─────▼─────┐
                     ┌─────│    WTF    │─────┐          ┌──────────────┐
                     │     │ (基础库)   │     │          │  ThirdParty  │
                     │     └───────────┘     │          │ (libwebrtc,  │
                     │           │           │          │  ANGLE, ICU..│
                     │           │           │          └──────────────┘
               ┌─────▼─────┐    │    ┌──────▼──────┐
               │    PAL    │    │    │ JavaScriptCore│
               │ (平台抽象)  │    │    │  (JS 引擎)   │
               └───────────┘    │    └──────────────┘
                                │
                     ┌─────────▼──────────┐
                     │      WebCore        │
                     │ (渲染引擎: DOM/CSS/  │
                     │  布局/绘制/网络栈)   │
                     └─────────┬──────────┘
                               │
                     ┌─────────▼──────────┐
                     │      WebKit         │
                     │ (多进程壳)           │
                     │ Frameworks: JSC,    │
                     │ PAL, WTF, WebCore,  │
                     │ bmalloc             │
                     └──┬──────┬──────┬───┘
                        │      │      │
               ┌────────┘      │      └────────┐
         ┌─────▼─────┐  ┌─────▼─────┐  ┌──────▼──────┐
         │ WebProcess │  │Network   │  │ GPUProcess  │
         │ (可执行文件) │  │Process   │  │ (可执行文件)  │
         └───────────┘  │(可执行文件) │  └─────────────┘
                        └───────────┘
```

## 各模块详解

### bmalloc — 内存分配器

| 项目 | 内容 |
|---|---|
| 用途 | WebKit 专用的 malloc/free 实现，替代系统内存分配器 |
| 位置 | `Source/bmalloc/` |
| 依赖 | 无（裸系统调用） |
| 关键类 | `MallocHeap`, `IsoHeap`, `Scavenger` |

### WTF — Web Template Framework

| 项目 | 内容 |
|---|---|
| 用途 | C++ 基础类库：字符串、容器、智能指针、线程、RunLoop、原子操作 |
| 位置 | `Source/WTF/wtf/` |
| 依赖 | 平台 libc / STL（但禁用 RTTI 和异常） |
| 关键类 | `String`, `AtomString`, `Vector`, `HashMap`, `HashSet`, `RefPtr`, `WeakPtr`, `RunLoop`, `Thread`, `Lock`, `JSONValues` |
| 特点 | `sizeof(String) == sizeof(void*)`、COW、缓存哈希、双编码 (8-bit/16-bit) |

### PAL — Platform Abstraction Layer

| 项目 | 内容 |
|---|---|
| 用途 | 平台抽象层：封装 OS 特定的功能调用 |
| 依赖 | WTF |
| 关键类 | `SessionID`, `SystemSleepListener`, `HysteresisActivity` |

### JavaScriptCore — JS 引擎

| 项目 | 内容 |
|---|---|
| 用途 | JavaScript 引擎 + WebAssembly、Parser、JIT、GC、Inspector 协议 |
| 位置 | `Source/JavaScriptCore/` |
| 依赖 | WTF, bmalloc |
| 关键组件 | `Parser`, `BytecodeGenerator`, `DFG JIT`, `FTL JIT`, `GC (Heap)`, `WebAssembly`, `Intl` |
| 规模 | 约 120 万行（最大模块之一） |

### WebCore — 渲染引擎

| 项目 | 内容 |
|---|---|
| 用途 | 浏览器渲染核心：DOM、CSS 解析/样式/布局/绘制、网络栈、媒体、GPU 渲染 |
| 位置 | `Source/WebCore/` |
| 依赖 | WTF, JavaScriptCore, PAL, ThirdParty (ICU, libwebrtc, ANGLE, cairo/skia 等) |
| 子目录 | `dom/`, `css/`, `page/`, `layout/`, `rendering/`, `platform/`, `loader/`, `html/`, `svg/`, `bindings/`, `Modules/` |
| 特点 | 不依赖 WebKit（即不依赖多进程架构），可在 WebKitLegacy 中单独使用 |

### WebKit — 多进程壳

| 项目 | 内容 |
|---|---|
| 用途 | 多进程架构管理：进程创建/销毁、IPC、API 层、自动化 |
| 位置 | `Source/WebKit/` |
| 依赖 | WTF, JavaScriptCore, WebCore, PAL, bmalloc |
| 产物 | WebKit.dll / shared library + 3 个子进程 exe |

## WebKit 目录内部结构

```
Source/WebKit/
  ├── UIProcess/       ← 浏览器主进程逻辑（只在主进程中运行）
  │   ├── API/         ← API 层
  │   │   ├── C/      ← WK* C 语言 API（跨平台公共 API）
  │   │   ├── Cocoa/  ← WKWebView ObjC API（仅 macOS/iOS）
  │   │   ├── glib/   ← WebKitGTK/WPE API（仅 Linux）
  │   │   └── API*.h  ← 内部 C++ API 类（API::PageConfiguration 等）
  │   ├── Network/    ← NetworkProcessProxy（网络进程代理）
  │   ├── GPU/        ← GPUProcessProxy
  │   ├── Model/      ← ModelProcessProxy
  │   ├── Launcher/   ← ProcessLauncher（进程启动器）
  │   ├── Automation/ ← Web 自动化（WebDriver）
  │   ├── WebPageProxy.h/cpp
  │   ├── WebProcessProxy.h/cpp
  │   └── WebProcessPool.h/cpp
  │
  ├── WebProcess/      ← Web 内容进程逻辑（在子进程中运行）
  │   ├── WebPage/     ← WebPage（渲染页面）
  │   ├── WebCoreSupport/ ← 桥接 WebCore 回调到 WebKit IPC
  │   ├── Network/     ← NetworkProcessConnection（连回网络进程）
  │   ├── GPU/         ← GPUProcessConnection
  │   ├── InjectedBundle/ ← InjectedBundle API
  │   └── WebProcess.h/cpp
  │
  ├── NetworkProcess/  ← 网络进程逻辑
  │   ├── NetworkResourceLoader, NetworkSession, NetworkCache
  │   ├── Cookies/, Storage/, ServiceWorker/, webrtc/
  │   └── NetworkProcess.h/cpp
  │
  ├── GPUProcess/      ← GPU 进程逻辑（可选，默认开启）
  │
  ├── ModelProcess/    ← 机器学习模型进程（可选）
  │
  ├── Shared/          ← 所有进程共享的代码
  │   ├── API/         ← 内部 C++ API 类（APIItBrowser 等）
  │   │   └── c/       ← WK* C API 的跨进程序列化支持
  │   ├── AuxiliaryProcess.h/cpp ← 子进程基类
  │   ├── AuxiliaryProcessCreationParameters.h ← 子进程初始化参数
  │   ├── WebPageCreationParameters.h
  │   └── WebProcessCreationParameters.h
  │
  └── Platform/        ← 跨进程基础设施
      └── IPC/         ← IPC 框架 (Connection, Encoder, Decoder, Messages)
```

## 各子进程入口

子进程都是独立可执行文件，链接 WebKit 框架：

```cmake
# CMakeLists.txt:757-759
set(WebProcess_LIBRARIES WebKit)
set(NetworkProcess_LIBRARIES WebKit)
set(GPUProcess_LIBRARIES WebKit)
```

| 进程 | 入口 (Unix/Linux) | 入口 (Windows) |
|---|---|---|
| WebProcess | `WebProcess/EntryPoint/unix/WebProcessMainUnix.cpp` | `WebProcess/EntryPoint/win/WebProcessMainWin.cpp` |
| NetworkProcess | `NetworkProcess/EntryPoint/unix/NetworkProcessMainUnix.cpp` | `NetworkProcess/EntryPoint/win/NetworkProcessMainWin.cpp` |
| GPUProcess | `GPUProcess/EntryPoint/unix/GPUProcessMainUnix.cpp` | `GPUProcess/EntryPoint/win/GPUProcessMainWin.cpp` |

进程入口的通用流程：

```cpp
// 以 WebProcess 的 unix 入口为例:
int main(int argc, char** argv)
{
    // 1. 解析命令行参数 → AuxiliaryProcessInitializationParameters
    //    --processIdentifier <id>
    //    --connectionIdentifier <socket_fd>
    //    --enable-shared-array-buffer (Playwright patch)

    // 2. 调用 AuxiliaryProcessMainCommon::performInitialization<WebProcess>()
    //    └─ WebProcess::singleton().initialize(params)
    //       └─ AuxiliaryProcess::initialize(params)
    //           ├─ platformInitialize(params)    ← 各平台 OS 初始化
    //           ├─ initializeSandbox(params)     ← 进入沙箱
    //           ├─ initializeProcess(params)     ← JS 引擎等
    //           ├─ initializeConnection(conn)    ← 建立 IPC 连接回 UIProcess
    //           └─ connection->open()            ← 开始收发消息

    // 3. WTF::RunLoop::mainSingleton().run()
}
```

## 关键约束

1. **单向依赖**：`WebCore` 不依赖 `WebKit`。`Shared/` 下的代码属于 `WebKit` 框架，能用 `WebCore` 的类（如 `JSON::Value`），反过来不行。

2. **API 三层**：
   - `API/C/` C API（`WK*Ref`, `extern "C"`）— 跨平台公共 API
   - `API/Cocoa/` ObjC API（`WKWebView`）— 仅 Apple 平台
   - `API/API*.h` 内部 C++ API（`API::PageConfiguration`）— 框架内部和工具直接用的 C++ 类

3. **进程间通信**：`Shared/` 下的结构体通过 IPC 序列化框架跨进程传递（`*.serialization.in` 文件描述序列化格式）。类型支持由 IPC 编解码器自动生成。

4. **统一构建**：所有 `.cpp` 文件在 `Sources.txt` 中列出，默认分组到 unified source 中编译（`@no-unify` 标记例外）。



## API
- Source\WebKit\UIProcess\API\APIPageConfiguration.h
	- include
		- 本模块：`"BrowsingContextGroup.h"` Source\WebKit\UIProcess\BrowsingContextGroup.h
		- Shared：`"WebPreferencesDefaultValues.h"` Source\WebKit\Shared\WebPreferencesDefaultValues.h
		- Shared API：`"APIObject.h"` Source\WebKit\Shared\API\APIObject.h
		- WebCore：`<WebCore/ContentSecurityPolicy.h>`  
			- Source\WebCore\page/csp/ContentSecurityPolicy.h
			- WebKitBuild\Release\WebCore\PrivateHeaders\ WebCore\ContentSecurityPolicy.h
	- 被include处
		- 本模块：Source\WebKit\UIProcess\WebPreferences.cpp
		- 本模块导出的API：Source\WebKit\UIProcess\API\C\WKPage.cpp
- Source\WebKit\Shared\AuxiliaryProcess.cpp
	- include
		- Platform：`"Logging.h"` Source\WebKit\Platform\Logging.h
		- Shared：`"ContentWorldShared.h"` Source\WebKit\Shared\ContentWorldShared.h
		- UIProcess：`"WebPageProxyIdentifier.h"`Source\WebKit\UIProcess\WebPageProxyIdentifier.h
- include规则，比如WebKit
	- WebKit里的文件只能include WebKit_PRIVATE_INCLUDE_DIRECTORIES，而公开文件只能include 同样是公开文件（在WebKitBuild/Release/WebKit/Headers/WebKit里）
- WebKit_PRIVATE_INCLUDE_DIRECTORIES
	- Source/cmake/WebKitMacros.cmake:354里的`_WEBKIT_TARGET_SETUP`宏
	- `WebKit_PRIVATE_INCLUDE_DIRECTORIES = target_include_directories(WebKit PRIVATE "$<BUILD_INTERFACE:${WebKit_PRIVATE_INCLUDE_DIRECTORIES}>")`
