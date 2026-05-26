# WebKit 多进程架构全景

## 核心分层

```
┌──────────────────────────────────────────────────────────────────┐
│                    UIProcess (浏览器主进程)                         │
│                                                                  │
│  WebProcessPool ─── 管理所有 WebProcessProxy                      │
│       │                                                          │
│       ├─ WebProcessProxy ──────→ 管理一个 WebContent 子进程        │
│       │      │                                                    │
│       │      ├─ WebPageProxy (页面代理)                            │
│       │      ├─ WebFrameProxy (iframe 代理)                       │
│       │      └─ SuspendedPageProxy (冻结页面代理)                  │
│       │                                                          │
│       ├─ NetworkProcessProxy ──→ 管理 NetworkProcess              │
│       │                                                          │
│       ├─ GPUProcessProxy ──────→ 管理 GPUProcess                  │
│       │                                                          │
│       └─ ModelProcessProxy ────→ 管理 ModelProcess                │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                   子进程 (Sandboxed)                               │
│                                                                  │
│  WebProcess (WebContent 进程) ←── 每个标签页/站点可能不同          │
│      ├─ WebPage (实际渲染页面的对象, 管理 Document/Frame)          │
│      ├─ WebFrame (框架对象)                                       │
│      ├─ 渲染引擎 (WebCore: DOM/样式/布局/绘制)                     │
│      └─ JavaScriptCore + WebAssembly                              │
│                                                                  │
│  NetworkProcess ←── 通常全局唯一，处理网络请求                      │
│      ├─ NetworkConnectionToWebProcess (每个 WebProcess 一个连接)   │
│      ├─ NetworkResourceLoader (加载资源)                          │
│      ├─ WebCookieManager (Cookie 管理)                            │
│      ├─ AuthenticationManager (HTTP 认证)                         │
│      ├─ NetworkCache (磁盘缓存)                                   │
│      └─ ServiceWorker 管理等                                      │
│                                                                  │
│  GPUProcess (可选) ─── 渲染加速进程                                 │
│  ModelProcess (可选) ─── 机器学习模型进程                           │
└──────────────────────────────────────────────────────────────────┘
```

---

## 一、Proxy 是什么

**Proxy = 代理**。它在 UIProcess 端代表一个远端子进程对象。可以理解为：你在浏览器主进程里看到的 `WebProcessProxy` 并不是 WebContent 进程本身，而是一个**本地替身**，通过它你可以启动、终止、发送 IPC 消息给那个真正的子进程。

```
┌─ UIProcess ─────────────────┐     IPC 管道      ┌─ 子进程 ────────────┐
│ WebProcessProxy (代理)  ────┼───────────────────┼──→ WebProcess (真实) │
│   - 持有 ProcessLauncher    │                    │   - 持有 WebCore    │
│   - 持有 IPC::Connection    │                    │   - 实际的渲染引擎  │
│   - 封装 State (Launching/  │                    │                     │
│       Running/Terminated)   │                    │                     │
└─────────────────────────────┘                    └─────────────────────┘
```

### Proxy 的职责

1. **`connect()`** — 创建 `ProcessLauncher`，让操作系统启动一个子进程
2. **`didFinishLaunching()`** — 子进程启动后，用返回的 socket/管道句柄创建 `IPC::Connection`（服务端），然后 flush 掉启动期间的积压消息
3. **`send()` / `sendSync()` / `sendWithAsyncReply()`** — 通过 Connection 向子进程发消息
4. **`terminate()`** — 杀进程
5. **State 管理** — 追踪进程是 `Launching`、`Running` 还是 `Terminated`

### 各类 Proxy 的继承链

```
AuxiliaryProcessProxy                        (基类: 连接管理、启动、心跳、节流)
  ├── WebProcessProxy                        (processName = "WebContent", 管理 WebPageProxy 集合)
  ├── NetworkProcessProxy                    (processName = "Network", 管理网络连接分配)
  ├── GPUProcessProxy                        (processName = "GPU", 管理 GPU 渲染)
  └── ModelProcessProxy                      (processName = "Model", 管理 ML 模型)
```

---

## 二、Pool 是什么

**Pool = 池子**。`WebProcessPool` 是 WebKit 最顶层的管理器，一个池子里管理 N 个进程。

```
WebProcessPool (进程池)
  ├── m_processes → Vector<Ref<WebProcessProxy>>   ←── 所有 Web 进程代理
  ├── m_networkProcess → NetworkProcessProxy        ←── 网络进程代理
  ├── m_gpuProcess → GPUProcessProxy                ←── GPU 进程代理
  ├── m_modelProcess → ModelProcessProxy            ←── Model 进程代理
  ├── m_visitedLinkStore                            ←── 共享的访问链接状态
  ├── m_backForwardCache                            ←── 页面缓存 (SuspendedPage)
  ├── m_prewarmedWebProcess                         ←── 预预热进程
  └── m_configuration                               ←── 配置 (ProcessPoolConfiguration)
```

### Pool 的核心工作

- 创建新的 Web 进程 (`createNewWebProcess`)
- 决定让哪个 Web 进程承载新页面 (`processForNavigation`, `processForSite`)
- 管理网络进程 (`ensureNetworkProcess`)
- 终止所有进程 (`terminateAllWebContentProcesses`)
- 进程预预热 (`prewarmProcess`)

### 多 Pool 场景

一个浏览器可以有多个 Pool。每个 Pool 有自己的进程集合，用于多 session 隔离。例如：

- `WebProcessPool("default")` → 常规浏览
- `WebProcessPool("incognito")` → 无痕浏览（独立的 NetworkProcess）

---

## 三、AuxiliaryProcess 详解

这是**子进程侧**的公共基类，实现了所有类型子进程的公共初始化流程。

### 源码位置

| 文件 | 平台 | 作用 |
|---|---|---|
| `Shared/AuxiliaryProcess.h` | 通用 | 基类声明 |
| `Shared/AuxiliaryProcess.cpp` | 通用 | 基类实现 |
| `Shared/Cocoa/AuxiliaryProcessCocoa.mm` | Cocoa (macOS/iOS) | 平台初始化 |
| `Shared/ios/AuxiliaryProcessIOS.mm` | iOS | iOS 特有初始化 |
| `Shared/mac/AuxiliaryProcessMac.mm` | macOS | macOS 特有初始化 |
| `Shared/win/AuxiliaryProcessMainWin.cpp` | Windows | 命令行解析 + 平台初始化 |
| `Shared/unix/AuxiliaryProcessMain.cpp` | Linux/Unix | 命令行解析 + 平台初始化 |

### 继承结构

```
AuxiliaryProcess (子进程侧基类)
  ├── WebProcess    (WebContent 进程)
  └── NetworkProcess (网络进程)
```

### `AuxiliaryProcess::initialize()` — 初始化流程 (全代码解析)

位于 `Source/WebKit/Shared/AuxiliaryProcess.cpp:86-125`：

```cpp
void AuxiliaryProcess::initialize(AuxiliaryProcessInitializationParameters&& parameters)
{
    // 0x00: Trace 事件标记
    TraceScope traceScope(ProcessInitializeStart, ProcessInitializeEnd);

    // 0x01: 启用线程安全检查
    WTF::RefCountDebugger::enableThreadingChecksGlobally();

    // 0x02: 设置进程类型
    //   Cocoa 平台在 XPCServiceInitializer() 中已调用 setAuxiliaryProcessType()
    //   其他平台在这里调用
    setAuxiliaryProcessType(parameters.processType);
    // 参数: parameters.processType = WebContent / Network / GPU / Model

    // 0x03: 设置 WebCore::ProcessIdentifier
    //   给这个进程一个全局唯一的 ID，用于 IPC 路由
    RELEASE_ASSERT_WITH_MESSAGE(parameters.processIdentifier, ...);
    Process::setIdentifier(*parameters.processIdentifier);

    // ===================================================================
    // 0x04: 【平台初始化】—— 不同操作系统做不同的事情
    // ===================================================================
    platformInitialize(parameters);

    // ===================================================================
    // 0x05: 【沙箱初始化】—— 进入沙箱环境
    // ===================================================================
    SandboxInitializationParameters sandboxParameters;
    initializeSandbox(parameters, sandboxParameters);

    // ===================================================================
    // 0x06: 【进程初始化】—— 子类覆写，做特定进程类型的初始化
    // ===================================================================
    initializeProcess(parameters);

    // 0x07: 初始化日志频道 (Logging)
    WTF::logChannels().initializeLogChannelsIfNecessary();
    WebCore::logChannels().initializeLogChannelsIfNecessary();
    WebKit::logChannels().initializeLogChannelsIfNecessary();

    // 0x08: 设置进程名称
    initializeProcessName(parameters);

    // 0x09: 安全保护
    //   只有 UIProcess 才能生成 SessionID、WebPageProxyIdentifier
    //   子进程调用会触发 ASSERT
    PAL::SessionID::enableGenerationProtection();
    WebPageProxyIdentifier::enableGenerationProtection();

    // ===================================================================
    // 0x0A: 【IPC 连接建立】—— 用 UIProcess 传过来的连接句柄建立 IPC
    // ===================================================================
    // 创建客户端 Connection (子进程作为 client 端)
    Ref connection = IPC::Connection::createClientConnection(
        WTF::move(parameters.connectionIdentifier));
    m_connection = connection.ptr();

    // 让子类有机会在连接上注册自己的 MessageReceiver
    initializeConnection(connection.ptr());

    // 打开连接，开始收发消息
    connection->open(*this);
}
```

### 各平台 `platformInitialize()` 对比

#### Cocoa 平台 (`AuxiliaryProcessCocoa.mm`)

```cpp
void AuxiliaryProcess::platformInitialize(const AuxiliaryProcessInitializationParameters& parameters)
{
    // macOS: 设置 QoS 策略 (LATENCY_QOS_TIER_0, THROUGHPUT_QOS_TIER_0)
    initializeTimerCoalescingPolicy();

    // iOS: 启用非规范化浮点数支持 (Denormals)
    FloatingPointEnvironment::singleton().enableDenormalSupport();

    // 保存主线程浮点环境，防止子线程改变影响主线程
    FloatingPointEnvironment::singleton().saveMainThreadEnvironment();

    // chdir 到 Bundle 路径
    [[NSFileManager defaultManager] changeCurrentDirectoryPath:[[NSBundle mainBundle] bundlePath]];

    // 设置客户端 Bundle Identifier
    setApplicationBundleIdentifier(parameters.clientBundleIdentifier);

    // 获取 audit_token 用于安全检查
    if (xpc_connection_t conn = parameters.connectionIdentifier.xpcConnection) {
        audit_token_t auditToken;
        xpc_connection_get_audit_token(conn, &auditToken);
        setApplicationAuditToken(auditToken);
    }

    // macOS: 禁用 NSTextView 降级到 LayoutManager
    disableDowngradeToLayoutManager();
}
```

#### Windows 平台 (`AuxiliaryProcessMainWin.cpp`)

```cpp
void AuxiliaryProcess::platformInitialize(const AuxiliaryProcessInitializationParameters&)
{
    // 禁用 CRT 断言弹框 —— 进程崩溃时不要弹 UI 对话框
    //（子进程通常是无头/后台进程，不应弹窗）
    WTF::disableCRTDebugAssertDialog();
}
```

Windows 的命令行解析 (`parseCommandLine`)：
```cpp
bool AuxiliaryProcessMainCommon::parseCommandLine(int argc, char** argv)
{
    for (int i = 0; i < argc; i++) {
        if (!strcmp(argv[i], "-clientIdentifier"))
            // 解析 HANDLE (IPC 管道的句柄)
            m_parameters.connectionIdentifier = IPC::Connection::Identifier {
                reinterpret_cast<HANDLE>(parseIntegerAllowingTrailingJunk<uint64_t>(argv[++i])...)
            };
        else if (!strcmp(argv[i], "-processIdentifier"))
            // 解析进程 ID
            m_parameters.processIdentifier = ...;
        // Playwright patch: SharedArrayBuffer 支持
        else if (!strcmp(argv[i], "-enable-shared-array-buffer"))
            m_parameters.shouldEnableSharedArrayBuffer = true;
        // JSC 选项
        else if (!strcmp(argv[i], "-configure-jsc-for-testing"))
            JSC::Config::configureForTesting();
        else if (!strcmp(argv[i], "-disable-jit"))
            JSC::ExecutableAllocator::disableJIT();
    }
}
```

#### Linux/Unix 平台 (`AuxiliaryProcessMain.cpp`)

```cpp
void AuxiliaryProcess::platformInitialize(const AuxiliaryProcessInitializationParameters&)
{
    struct sigaction signalAction;
    memset(&signalAction, 0, sizeof(signalAction));
    sigemptyset(&signalAction.sa_mask);
    signalAction.sa_handler = SIG_IGN;
    // 忽略 SIGPIPE —— 避免写入已关闭的 socket 时进程被杀死
    // （WebKit 子进程间通信使用 socketpair，断连时写操作会触发 SIGPIPE）
    sigaction(SIGPIPE, &signalAction, nullptr);
}
```

Unix 的命令行解析:
```cpp
bool AuxiliaryProcessMainCommon::parseCommandLine(int argc, char** argv)
{
    // argv[1] = processIdentifier (uint64)
    // argv[2] = connectionIdentifier (int, socket fd)
    parseInteger<uint64_t>(argv[1])     → m_parameters.processIdentifier
    parseInteger<int>(argv[2])          → m_parameters.connectionIdentifier (UnixFileDescriptor)
    // 可选: --configure-jsc-for-testing
    // Playwright: --enable-shared-array-buffer
}
```

### `initializeProcess()` — 子类覆写

#### WebProcess (`WebProcess.cpp:407`)

```cpp
void WebProcess::initializeProcess(const AuxiliaryProcessInitializationParameters& parameters)
{
    // 从 extraInitializationData 读取 LockdownMode / EnhancedSecurity
    m_isLockdownModeEnabled = parameters.extraInitializationData
        .get<HashTranslatorASCIILiteral>("enable-lockdown-mode"_s) == "1"_s;
    m_isEnhancedSecurityEnabled = parameters.extraInitializationData
        .get<HashTranslatorASCIILiteral>("enable-enhanced-security"_s) == "1"_s;

    // 清空进程权限（降权）
    WTF::setProcessPrivileges({ });

    // 配置 JavaScriptCore
    JSC::Options::allowNonSPTagging() = false;
    // Playwright: 非 Cocoa 平台启用 SharedArrayBuffer
    //（Cocoa 平台通过 XPC Service 的 xpcplist 设置）
    if (parameters.shouldEnableSharedArrayBuffer)
        JSC::Options::useSharedArrayBuffer() = true;
    JSC::Options::notifyOptionsChanged();

    // 设置 MessagePort 通道（Worker 间通信）
    MessagePortChannelProvider::setSharedProvider(WebMessagePortChannelProvider::singleton());

    platformInitializeProcess(parameters);
    updateCPULimit();  // 启动 CPU 监控

    // 初始化 Inspector 的 ID 生成器
    Inspector::IdentifiersFactory::initializeWithProcessID(parameters.processIdentifier->toUInt64());
}
```

#### NetworkProcess

类似 WebProcess，但专注网络栈初始化，包括 Cache 初始化, Cookie Store, 网络 Session 等。

### `initializeConnection()` — WebProcess 覆写版本

```cpp
void WebProcess::initializeConnection(IPC::Connection* connection)
{
    // 1. 调用基类 (AuxiliaryProcess::initializeConnection)
    //    Linux/GLib: 发送 socket 凭据
    AuxiliaryProcess::initializeConnection(connection);

    // 2. 设置连接断开时的回调
    //    GTK/WPE: 等待 10s 后调用 atexit 清理 (EGL 显示等)
    //    其他: 直接从后台队列 _exit()
    connection->setDidCloseOnConnectionWorkQueueCallback(callExitCallback);

    // 3. 注册各种 Dispatcher
    protect(eventDispatcher())->initializeConnection(*connection);             // 事件分发
    protectedWebInspectorInterruptDispatcher()->initializeConnection(*connection); // Inspector

    // 4. 通知所有 Supplement 连接已建立
    for (auto& supplement : m_supplements.values())
        supplement->initializeConnection(connection);
}
```

---

## 四、"真正的工作初始化" — initialize 之后

`AuxiliaryProcess::initialize()` 建立 IPC 连接后，UIProcess 会发来特定类型的初始化消息。以 WebProcess 为例：

### 完整的时序

```
UIProcess                                     子进程 (WebProcess)
───────                                       ───────────────────

1. AuxiliaryProcessProxy::connect()
   └─→ ProcessLauncher 启动进程

2. 进程启动                                   3. AuxiliaryProcess::initialize()
                                                   ├─ platformInitialize()   ← 平台相关
                                                   ├─ initializeSandbox()
                                                   ├─ initializeProcess()   ← JSC 等
                                                   └─ initializeConnection()
                                                       ├─ 创建 IPC::Connection
                                                       └─ connection->open()

4. Proxy::didFinishLaunching(connID)
   ├─ 创建 IPC::Connection (服务端)
   └─ 发送积压的 Pending Messages
       └─ 例如: CreatePage, InitializeWebProcess

5. 发送 InitializeWebProcess 消息 ───────────→  6. WebProcess::initializeWebProcess(params)
                                                       ├─ 设置 WebsiteDataStore
                                                       ├─ 配置 MemoryPressureHandler
                                                       ├─ 注册 URL Scheme (local, noAccess 等)
                                                       ├─ 加载插件/扩展
                                                       ├─ 初始化 Supplement
                                                       └─ 回复 UIProcess: "准备好了"

7. 页面创建消息 ─────────────────────────────→  8. WebPage::WebPage()
                                                       ├─ 创建 Page (WebCore::Page)
                                                       ├─ 创建主 Frame
                                                       └─ 开始加载/渲染
```

### `initializeWebProcess` 具体做什么

```cpp
void WebProcess::initializeWebProcess(
    WebProcessCreationParameters&& parameters,
    CompletionHandler<void(ProcessIdentity)>&& completionHandler)
{
    // 立即回复，让 UIProcess 知道进程身份
    completionHandler(ProcessIdentity { ProcessIdentity::CurrentProcess });

    // 设置 DataStore（SessionID、Cookie 存储路径等）
    if (parameters.websiteDataStoreParameters)
        setWebsiteDataStoreParameters(WTF::move(*parameters.websiteDataStoreParameters));

    // 设置 PresentingApplicationPID
    setLegacyPresentingApplicationPID(parameters.presentingApplicationPID);

    // Cocoa 平台 WebProcess 初始化
    platformInitializeWebProcess(parameters);

    // 设置线程优先级 (比 UIProcess 略低)
    WTF::Thread::setCurrentThreadIsUserInteractive(-1);

    // 配置内存压力处理器
    if (!m_suppressMemoryPressureHandler) {
        auto& memoryPressureHandler = MemoryPressureHandler::singleton();
        memoryPressureHandler.setLowMemoryHandler([...] (Critical critical, ...) {
            // 后台页面: 即使非紧急也按紧急处理
            // 缓存/预热进程: 直接退出
        });
    }

    // 注册各种 URL Scheme
    registerURLSchemeAsEmptyDocument(...);
    registerURLSchemeAsSecure(...);
    registerURLSchemeAsLocal(...);
    registerURLSchemeAsNoAccess(...);
    // ...

    // 设置日志
    // ...

    // 初始化所有 Supplement
    for (auto& supplement : m_supplements.values())
        supplement->initialize(parameters);
}
```

---

## 五、UIProcess 侧进程创建全流程

### 5.1 API 层入口 — 从应用程序调用到 WebKit

进程创建始于上层 API 调用，以 Windows 平台的 Playwright 为例：

```
Playwright (WebKitBrowserWindow.cpp)
  │
  ├─ MainWindow::init() → WKViewCreate(rect, conf, hWnd)
  │                       └──→ WKViewCreate() (API/C/win/WKView.cpp)
  │                              └──→ WebPageProxy::create()
  │
  └─ WKPageLoadURL() / WKViewNavigateTo()
        └──→ WebPageProxy::loadRequest()
               └──→ processForNavigation()  ← 首次加载触发进程创建
```

**API 层到 WebKit 的入口:**
- **C API**: `WKViewCreate()`, `WKPageCreate()` — 传统 C 接口
- **Modern API (Cocoa)**: `WKWebView` initWithFrame → 内部调用相同的 WebKit 核心
- **Playwright 层**: `WebKitBrowserWindow` 封装 `WKView`/`WKPage` 进行页面管理，`createViewCallback()` 和 `createPageCallback()` 作为创建回调

### 5.2 WebPageProxy 构造 — 首次关联进程

`WebPageProxy` 构造时（`WebPageProxy.cpp:873`），通过 `PageConfiguration` 获得 `WebProcessProxy` 引用：

```cpp
// WebPageProxy.cpp:873
WebPageProxy::WebPageProxy(PageClient& pageClient, WebProcessProxy& process, Ref<API::PageConfiguration>&& configuration)
    : m_legacyMainFrameProcess(process)    // ← 记录关联的进程
    , m_pageGroup(*configuration->pageGroup())
    , m_preferences(configuration->preferences())
    // ...
{
    // 构造函数不立即启动进程
    // 进程启动由 launchProcess() 触发
}
```

**关键点:** `WebPageProxy` 构造时传入的 `process` 不一定已启动。它可能是：
- 一个 Dummy 进程（从未启动）
- 一个已存在的运行中进程
- 一个预预热进程

进程实际启动发生在以下时机:
1. **首次加载** — `WebPageProxy::loadRequest()` → 触发 `launchProcess()`
2. **页面创建** — `finishAttachingToWebProcess()` → `initializeWebPage()` 发 CreateWebPage
3. **进程崩溃后恢复** — `launchProcess(ProcessLaunchReason::Crash)`
4. **进程切换 (Swap)** — `launchProcess(ProcessLaunchReason::ProcessSwap)`

### 5.3 WebPageProxy::launchProcess() — 决定使用哪个进程

这是 UIProcess 侧进程创建的核心（`WebPageProxy.cpp:1390`）：

```cpp
void WebPageProxy::launchProcess(const Site& site, ProcessLaunchReason reason)
{
    // 1. 断开与旧进程的关联（清理老的 MessageReceiver、PageMap）
    protect(legacyMainFrameProcess())->removeWebPage(*this, ...);
    removeAllMessageReceivers();

    Ref processPool = m_configuration->processPool();

    // 2. 【核心决策】—— 选择或创建进程
    if (/* Site Isolation 已有匹配的 BrowsingContextGroup 进程 */) {
        m_legacyMainFrameProcess = frameProcess->process();
    } else if (/* 有相关页面，复用其进程以避免跨进程通信 */) {
        m_legacyMainFrameProcess = relatedPage->ensureRunningProcess();
    } else {
        // ← 最终走到 WebProcessPool::processForSite() 做完整决策
        m_legacyMainFrameProcess = processPool->processForSite(
            websiteDataStore(), ..., site, ...);
    }

    // 3. 关联 WebPageProxy 到选中的进程（注册 MessageReceiver 等）
    process->addExistingWebPage(*this, WebProcessProxy::BeginsUsingDataStore::Yes);
    addAllMessageReceivers();

    // 4. 在子进程侧创建 WebPage 对象（发 CreateWebPage IPC 消息）
    finishAttachingToWebProcess(site, reason);
    //   └─ initializeWebPage()
    //        └─ process->send(Messages::WebProcess::CreateWebPage(...), 0);
}
```

### 5.4 WebProcessPool::processForSite() — 进程选择决策树

这是"到底在哪里创建进程"的完整决策逻辑（`WebProcessPool.cpp:1274`）：

```cpp
Ref<WebProcessProxy> WebProcessPool::processForSite(
    WebsiteDataStore& websiteDataStore,
    WebProcessProxy::IsolatedProcessType isolatedProcessType,
    const std::optional<Site>& site, ...)
{
    // ==================== 决策树: 优先复用，最后新建 ====================

    // 1. 共享进程模式: 尝试从 WebProcess 缓存中取
    if (isolatedProcessType == Shared) {
        if (RefPtr process = webProcessCache().takeSharedProcess(...))
            return process.releaseNonNull();
    }

    // 2. Site Isolation 模式: 按站点精准匹配
    if (site && !site->isEmpty()) {
        // 2a. WebProcess Cache 命中
        if (RefPtr process = webProcessCache().takeProcess(*site, ...))
            return process.releaseNonNull();

        // 2b. 复用 SuspendedPage 的进程（恢复冻结页面）
        if (RefPtr process = SuspendedPageProxy::findReusableSuspendedPageProcess(...))
            return process.releaseNonNull();
    }

    // 3. 取预预热进程（空闲时预先创建好的）
    if (RefPtr process = tryTakePrewarmedProcess(websiteDataStore, ...))
        return process.releaseNonNull();

    // 4. 单进程模式: 直接复用已有进程
    if (usesSingleWebProcess()) {
        for (Ref process : m_processes) {
            // 跳过预热进程和 dummy 进程
            if (process->isPrewarmed() || process->isDummyProcessProxy())
                continue;
            return process;
        }
    }

    // ==================== 最终手段: 创建全新进程 ====================
    Ref process = createNewWebProcess(&websiteDataStore, lockdownMode, ...);
    process->setIsolatedProcessType(isolatedProcessType);
    return process;
}
```

**决策优先级总结：**

| 优先级 | 策略 | 条件 | 代码位置 |
|---|---|---|---|
| 1 | WebProcess Cache | 有缓存的进程可用 | `webProcessCache().takeProcess()` |
| 2 | SuspendedPage 复用 | 有冻结页面的进程 | `SuspendedPageProxy::findReusable...()` |
| 3 | 预预热进程 | 池中有空闲预热进程 | `tryTakePrewarmedProcess()` |
| 4 | 单进程复用 | 配置了单进程模式 | `usesSingleWebProcess()` |
| 5 | **创建新进程** | 以上都不满足 | `createNewWebProcess()` |

### 5.5 WebProcessPool::createNewWebProcess() — 创建全新进程

```cpp
// WebProcessPool.cpp:845
Ref<WebProcessProxy> WebProcessPool::createNewWebProcess(
    WebsiteDataStore* websiteDataStore,
    WebProcessProxy::LockdownMode lockdownMode,
    EnhancedSecurity enhancedSecurity,
    WebProcessProxy::IsPrewarmed isPrewarmed, ...)
{
    // 1. 创建 WebProcessProxy —— 构造时立即触发 connect() 启动子进程
    auto processProxy = WebProcessProxy::create(
        *this, websiteDataStore, lockdownMode, enhancedSecurity,
        isPrewarmed, crossOriginMode,
        ShouldLaunchProcess::Yes,          // ← 立即启动
        enableWebAssemblyDebugger);

    // 2. 准备进程参数 (WebProcessCreationParameters) 并发送
    //    - 读取 Preferences、URL Scheme 注册、SandboxExtension
    //    - 设置 Session 信息、InjectedBundle 路径
    //    - 调用 process.initializeWebProcess(params)
    //      即通过 IPC 发送 InitializeWebProcess 消息给子进程
    initializeNewWebProcess(processProxy, websiteDataStore, isPrewarmed);

    // 3. 加入进程列表
    m_processes.append(processProxy.copyRef());

    return processProxy;
}
```

#### initializeNewWebProcess() 准备的参数

```cpp
// WebProcessPool.cpp:995
void WebProcessPool::initializeNewWebProcess(
    WebProcessProxy& process, WebsiteDataStore* websiteDataStore,
    WebProcessProxy::IsPrewarmed isPrewarmed)
{
    WebProcessCreationParameters parameters;

    // 日志参数
    parameters.auxiliaryProcessParameters = AuxiliaryProcessProxy::auxiliaryProcessParameters();

    // InjectedBundle 路径 + SandboxExtension
    parameters.injectedBundlePath = m_resolvedPaths.injectedBundlePath;
    // ...

    // 各种 URL Scheme 注册
    parameters.urlSchemesRegisteredAsSecure = ...;
    parameters.urlSchemesRegisteredAsLocal = ...;
    parameters.urlSchemesRegisteredAsCORSEnabled = ...;
    // ... (共约 15 类 URL Scheme)

    // Cache 模型
    parameters.cacheModel = LegacyGlobalSettings::singleton().cacheModel();

    // 语言偏好
    parameters.overrideLanguages = configuration().overrideLanguages();

    // WebsiteDataStore 参数 (SessionID, Cookie 路径等)
    if (websiteDataStore)
        parameters.websiteDataStoreParameters = webProcessDataStoreParameters(process, *websiteDataStore);

    // Cross-Origin 策略
    parameters.crossOriginMode = process.crossOriginMode();

    // 【发送】—— 通过已建立的 IPC 连接发送给子进程
    process.initializeWebProcess(WTF::move(parameters));

    // 如果是预热进程，加入预热集合
    if (isPrewarmed == WebProcessProxy::IsPrewarmed::Yes)
        m_prewarmedProcesses.add(process);
}
```

### 5.6 WebProcessProxy 构造与 connect() 的触发时机

关键设计：**WebProcessProxy 构造时立即启动子进程**，而不是等第一次使用时再启动。

```cpp
// WebProcessProxy.cpp 构造实现
WebProcessProxy::WebProcessProxy(..., ShouldLaunchProcess shouldLaunchProcess, ...)
    : AuxiliaryProcessProxy(...)
{
    if (shouldLaunchProcess == ShouldLaunchProcess::Yes)
        connect();  // ← 构造时立即启动子进程！
}

// AuxiliaryProcessProxy::connect()
void AuxiliaryProcessProxy::connect()
{
    m_processStart = MonotonicTime::now();

    // 组装启动参数
    ProcessLauncher::LaunchOptions launchOptions { m_processIdentifier };
    getLaunchOptions(launchOptions);     // 填充 extraInitializationData

    // 创建 ProcessLauncher 并启动
    m_processLauncher = ProcessLauncher::create(this, WTF::move(launchOptions));
}
```

### 5.7 进程创建的三种触发场景

#### 场景 A: 首次加载 — InitialProcess

```
WKViewCreate(pageConfig)
  │
  ├─ WebPageProxy::create(process = DummyProxy)
  │     └─ DummyProxy: 关联 WebProcessPool，但未真正 connect()
  │
  └─ WebPageProxy::loadRequest()
        └─ WebPageProxy::launchProcess(InitialProcess)
              └─ WebProcessPool::processForSite()
                    ├─ tryTakePrewarmedProcess()  ← 优先取预热进程
                    └─ createNewWebProcess()      ← 或新建
                          ├─ WebProcessProxy::create()
                          │   └─ connect() → ProcessLauncher
                          └─ initializeNewWebProcess()
                                └─ 发 InitializeWebProcess 消息
```

#### 场景 B: 导航时进程切换 — ProcessSwap

```
WebPageProxy::decidePolicyForNavigationAction()
  │
  └─ processForNavigation(page, frame, navigation, ...)
        │
        ├─ processForNavigationInternal()
        │     ├─ 检查是否跨站点
        │     ├─ 是 → processForSite() → 可能获得新进程
        │     └─ 否 → 复用当前源进程
        │
        └─ 如果切换到新进程:
              └─ launchProcess(ProcessSwap)
                    └─ finishAttachingToWebProcess()
                          └─ 发 CreateWebPage 到新进程
```

#### 场景 C: 进程崩溃后恢复 — Crash

```
WebProcessProxy::processDidTerminateOrFailedToLaunch()
  │
  └─ WebPageProxy::processDidCrash()
        └─ launchProcess(Crash)
              └─ 同首次加载流程
```

### 5.8 AuxiliaryProcessProxy::didFinishLaunching() — 回连

子进程启动后，`ProcessLauncher` 获得子进程的管道句柄，回调 `didFinishLaunching`：

```cpp
// AuxiliaryProcessProxy.cpp:345
void AuxiliaryProcessProxy::didFinishLaunching(
    ProcessLauncher* launcher,
    IPC::Connection::Identifier&& connectionIdentifier)
{
    // 检查启动耗时（超过 1 秒打 fault 日志）
    auto launchTime = MonotonicTime::now() - m_processStart;
    if (launchTime > 1_s)
        RELEASE_LOG_FAULT(Process, "...");

    if (!connectionIdentifier)
        return;  // 启动失败

    // 创建 IPC::Connection (UIProcess 端是 Server 端)
    RefPtr connection = IPC::Connection::createServerConnection(
        WTF::move(connectionIdentifier), Thread::QOS::UserInteractive);
    m_connection = connection.copyRef();
    connectionToProcessMap().add(m_connection->uniqueID(), *this);

    connectionWillOpen(*connection);
    connection->open(*this);

    // 【关键】发送启动期间积压的 Pending Messages
    // 包括 InitializeWebProcess、CreateWebPage 等
    for (auto&& pendingMessage : std::exchange(m_pendingMessages, { })) {
        if (pendingMessage.asyncReplyHandler)
            connection->sendMessageWithAsyncReply(...);
        else
            connection->sendMessage(...);
    }

    // Cocoa: 创建进程生命周期断言
    // macOS: 设置 BoostedJetsam 防止被系统杀死
}
```

### 5.9 NetworkProcess 的创建

NetworkProcess 的创建机制不同，它由 `NetworkProcessProxy` 管理，**通常全局唯一**：

```cpp
// NetworkProcessProxy.h
static Ref<NetworkProcessProxy> ensureDefaultNetworkProcess();

// 内部实现
Ref<NetworkProcessProxy> NetworkProcessProxy::ensureDefaultNetworkProcess()
{
    if (auto existing = defaultNetworkProcess(); existing)
        return existing->process;  // ← 复用已有实例

    auto proxy = NetworkProcessProxy::create();  // ← 全局唯一创建
    proxy->connect();  // ← 启动 Network 进程
    return proxy;
}
```

**NetworkProcess 创建触发时机（由 WebProcessPool / WebsiteDataStore 触发）：**

```
WebPageProxy::launchProcess()
  └─ WebsiteDataStore 首次使用
        └─ WebsiteDataStore::networkProcess()
              └─ NetworkProcessProxy::ensureDefaultNetworkProcess()

或: WebProcessPool::initializeNewWebProcess()
      └─ 获取 DataStore 参数时需要 NetworkProcess
```

**Web vs Network 进程创建对比：**

| 特性 | WebProcess | NetworkProcess |
|---|---|---|
| 创建时机 | 每个页面/站点需要时 | 首次需要网络服务时 |
| 数量 | 多个（每站点/每隔离域） | 通常一个（每 Session 一个） |
| 创建触发 | `processForSite()` → `createNewWebProcess()` | `ensureDefaultNetworkProcess()` |
| 复用策略 | 缓存 + 预热 + Site Isolation 复用 | 全局单例 |
| 生命周期 | 页面关闭后可缓存或终止 | 随 ProcessPool 生命周期 |

### 5.10 进程预预热 (Process Prewarm)

预预热是 WebKit 的关键性能优化，在空闲时预先创建 WebProcess：

```cpp
// WebProcessPool.cpp:1123
void WebProcessPool::prewarmProcess()
{
    // 限制: 最多 1 个预热进程
    if (m_prewarmedProcesses.computeSize() >= prewarmedProcessCountLimit())
        return;

    // 创建预热进程，标记 IsPrewarmed::Yes
    createNewWebProcess(
        nullptr,                // ← 不关联 WebsiteDataStore
        lockdownMode,
        EnhancedSecurity::Disabled,
        IsPrewarmed::Yes        // ← 预热标记
    );
}
```

**预热进程的取用：**

```cpp
// WebProcessPool.cpp:853
RefPtr<WebProcessProxy> WebProcessPool::tryTakePrewarmedProcess(...)
{
    for (Ref process : m_prewarmedProcesses) {
        // 检查 LockdownMode 匹配
        if (process->lockdownMode() != lockdownMode) continue;

        // 检查进程是否还活着（从睡眠恢复后可能已死）
        if (process->wasTerminated()) continue;

        prewarmedProcess = process.ptr();
        break;
    }

    // 设置 DataStore
    prewarmedProcess->setWebsiteDataStore(websiteDataStore);
    prewarmedProcess->markIsNoLongerInPrewarmedPool();
    return prewarmedProcess;
}
```

**预热触发时机：**
- 首次页面加载完成后自动触发（[自动预热]）
- `didFinishLoad()` → `prewarmProcess()`
- 客户端也可以显式调用 `WKContextPrewarmWebProcess()`

### 5.11 完整生命周期 (UIProcess 侧)

```
时间线          UIProcess 动作                                      子进程状态
────            ──────────────                                      ─────────

T0              WKViewCreate
                ├─ WebPageProxy::create(process = dummy)            (尚无进程)
                └─ WebPageProxy 构造完成

T1              WebPageProxy::loadRequest()
                └─ launchProcess(InitialProcess)
                     └─ processForSite()
                           ├─ [可选] tryTakePrewarmedProcess()     已有进程, Running
                           └─ [新建] createNewWebProcess()
                                 ├─ WebProcessProxy::create()
                                 │   └─ connect()                  Launching...
                                 │       └─ ProcessLauncher
                                 │
                                 └─ initializeNewWebProcess()      Running → 收参数

T2              finishAttachingToWebProcess()
                └─ initializeWebPage()
                     └─ 发 CreateWebPage ────────────────────────→ WebPage::WebPage()

T3              导航/站点变更
                ├─ [同站点] 复用当前进程
                └─ [跨站点] processForNavigation()
                     ├─ 旧进程 → Suspend/缓存/终止
                     └─ 新进程 → 重复 T1~T2

T4              页面关闭
                └─ WebPageProxy::close()
                     └─ WebProcessProxy::removeWebPage()
                          当页数为 0:
                          ├─ 可缓存 (WebProcess Cache) ← 快速恢复
                          ├─ 可终止 (释放资源)
                          └─ 或保留 (取决于策略)
```

---

## 六、IPC 通信机制

```
UIProcess 侧                         子进程侧
─────────                            ────────
AuxiliaryProcessProxy                AuxiliaryProcess
  │                                      │
  │  m_connection (IPC::Connection)  ──→  m_connection (IPC::Connection)
  │      ↓ Client 端                       ↓ Server 端
  │                                       │
  │  send(msg, destID) ─────────────────→  MessageReceiver::didReceiveMessage()
  │  sendSync(msg, destID) ─────────────→  didReceiveSyncMessage()
  │  sendWithAsyncReply(msg, callback) ─→  然后回调回来
```

### 消息发送方式

| 方式 | 说明 | 使用场景 |
|---|---|---|
| `send()` | 异步单向消息，不等待回复 | 通知性消息 (如 `SetPageMuted`) |
| `sendSync()` | 同步等待回复，最多等 1s | 需要即时结果的查询 |
| `sendWithAsyncReply()` | 异步等待回复（回调） | 大部分 IPC 交互 |

### Pending Messages 机制

进程启动期间（State == `Launching`），所有 `send()` 调用不会丢失：

```cpp
case State::Launching:
    // 启动期间的消息被暂存在 m_pendingMessages 中
    m_pendingMessages.append({ WTF::move(encoder), sendOptions, WTF::move(asyncReplyHandler) });
    return true;
```

等到 `didFinishLaunching()` 时统一 flush。

---

## 七、进程模型的关键概念

### 1. 进程类型 (`AuxiliaryProcessProxy::Type`)

```cpp
enum class Type : uint8_t {
    WebContent,   // Web 渲染进程
    Network,      // 网络进程
    Model,        // ML 模型进程
    GPU,          // GPU 进程
};
```

### 2. 进程状态 (`AuxiliaryProcessProxy::State`)

```cpp
enum class State {
    Launching,   // 正在启动 (ProcessLauncher 工作中)
    Running,     // 正常运行 (IPC 连接已建立)
    Terminated,  // 已终止
};
```

### 3. Site Isolation

- **Shared Process** (`CrossOriginMode::Shared`): 多个站点共享一个 WebProcess
- **Isolated Process** (`CrossOriginMode::Isolated`): 站点独立进程（安全隔离）
- 通过 `WebProcessProxy::m_site` 追踪进程承载的站点
- `BrowsingContextGroup` 负责维护站点到进程的映射

### 4. Process Prewarm

- `IsPrewarmed::Yes` 创建的进程在池中待命
- 创建新页面时优先从预热池取，加速启动
- 预热进程不持有强引用指向 `WebProcessPool`
- 自动预热在首次页面加载完成后触发

### 5. Process Throttler

```
Foreground  →  正常调度, 高优先级
Background  →  降低优先级, 可被系统回收
Suspended   →  进程挂起 (仅保存内存映像)
```

通过 `ProcessAssertion` (Cocoa 平台) 或进程调度策略实现。

### 6. Responsiveness Timer

- 定期向子进程发 `MainThreadPing` 消息
- 超时无响应 → `didBecomeUnresponsive()` → 终止进程
- 调试中的进程会跳过检测

---

## 八、关键文件速查

| 文件 | 层次 | 作用 |
|---|---|---|
| `UIProcess/WebProcessPool.h/cpp` | UIProcess | 进程池管理器，进程创建/调度/终止 |
| `UIProcess/WebProcessProxy.h/cpp` | UIProcess | WebContent 进程代理 |
| `UIProcess/Network/NetworkProcessProxy.h/cpp` | UIProcess | Network 进程代理 |
| `UIProcess/AuxiliaryProcessProxy.h/cpp` | UIProcess | 所有 Proxy 基类 |
| `UIProcess/Launcher/ProcessLauncher.h` | UIProcess | 底层进程启动器 |
| `Shared/AuxiliaryProcess.h/cpp` | Shared | 子进程侧公共基类 |
| `Shared/AuxiliaryProcessCreationParameters.h` | Shared | 进程创建参数 (日志、签名) |
| `WebProcess/WebProcess.h/cpp` | WebProcess | WebContent 进程主体 |
| `NetworkProcess/NetworkProcess.h/cpp` | NetworkProcess | 网络进程主体 |
| `Shared/WebProcessCreationParameters.h` | Shared | WebProcess 配置参数 |
| `Shared/NetworkProcessCreationParameters.h` | Shared | NetworkProcess 配置参数 |

---

## 九、平台相关的进程名对照

| 平台 | WebProcess 可执行文件 | NetworkProcess 可执行文件 |
|---|---|---|
| macOS | `com.apple.WebKit.WebContent.xpc` (XPC Service) | `com.apple.WebKit.Networking.xpc` |
| iOS | 同上 (XPC Service) | 同上 |
| Windows | `WebKitWebProcess.exe` | `WebKitNetworkProcess.exe` |
| Linux (GTK) | `WebKitWebProcess` | `WebKitNetworkProcess` |
| Linux (WPE) | `WPEWebProcess` | `WPENetworkProcess` |
