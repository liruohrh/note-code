
- https://github.com/WebKit/WebKit/blob/ae4576e425cf4eee9960dcd6de57b5ec693cab91/Introduction.md?plain=1#L3
- Source/bmalloc：内存分配
- Source/WTF (Web Template Framework)：cpp基础库，以及平台无关的API，如
- Source/WTF （JavaScriptCore）
- Source/WebCore：渲染引擎，Document、WebAPIs
- Source/WebKit
	- [多进程架构](https://github.com/WebKit/WebKit/blob/ae4576e4/Introduction.md?plain=1#L40-L40)
		- **UIProcess** - 管理用户界面的应用程序进程（例如，Safari、邮件）。 
		- **WebProcess** - （WebProcess）加载和执行 Web 内容的沙盒进程
			- 该进程是多例的，可多Page共享一个（比如`window.open()`创建的页面Source/WebKit/UIProcess/WebProcessPool.cpp:1334-1340，WebProcessPool::processForSite， `(relatedPage && !relatedPage->isClosed() && relatedPage->hasSameGPUAndNetworkProcessPreferencesAs(pageConfiguration) && !siteIsolationEnabled)`）
			- [关于单进程设置](#WebProcess::Singleton)
		- **NetworkProcess** - 处理所有网络请求和存储管理
		- **GPUProcess** - 管理图形操作，包括 WebGL 和合成。
		- ModelProcess：渲染和管理 3D 模型内容
		- 进程都在WebKit下有一个目录xxx，主文件xxx，以及用不同平台的xxxMain（main函数），main都是用Source\WebKit\Shared\AuxiliaryProcessMain.h处理

- UI Porcess可以等同于MiniBrowser这个简单的App，或者说Safari，因此主要调用的API是此处的。
	- 跨平台：Source\WebKit\UIProcess\API\C（里面有依然有平台专属如mac）
		- 
	- 平台专属如：Source\WebKit\UIProcess\API\ios
# 数据存储：
- Source\WebKit\UIProcess\API\APIPageConfiguration.h
	- Source\WebCore\page\PageConfiguration.h
- Source\WebKit\UIProcess\WebsiteData\WebsiteDataStore.h
	- parameters使用处
		- Source\WebKit\NetworkProcess\NetworkProcess.cpp，NetworkProcess::addWebsiteDataStore
		- Source\WebKit\WebProcess\WebProcess.cpp，WebProcess::setWebsiteDataStoreParameters
- Source\WebKit\Shared\WebsitePoliciesData.h
- Source\WebKit\UIProcess\API\APIProcessPoolConfiguration.h
- 
这四个类的职责层次完全不同，并不重复。下面逐一说明：
---

## 层次关系总览

```
ProcessPoolConfiguration   ← 进程池级别（WebProcess 管理策略）
        ↓ 用于创建
    WebProcessPool
        ↓ 被引用于
    PageConfiguration      ← 单个页面创建时的静态配置
        ├── WebsiteDataStore   ← 数据存储运行时对象（不是配置类）
        └── defaultWebsitePolicies
                ↓ 导航时动态下发
        WebsitePoliciesData    ← 每次导航的动态策略（非创建时配置）
```

---

## 各类职责

### 1. `API::ProcessPoolConfiguration`

**作用：** 控制 `WebProcessPool`（Web 进程池）的行为，是**进程管理层**的配置。

关键字段：
- `injectedBundlePath` — 注入的 bundle 路径
- `processSwapsOnNavigation` — 导航时是否切换进程（Site Isolation）
- `isAutomaticProcessWarmingEnabled` — 是否预热进程
- `usesSingleWebProcess` — 是否强制单进程
- `isJITEnabled` — 是否启用 JIT

**使用时机：** 创建 `WebProcessPool` 之前，一次性设置，之后不可更改。

---

### 2. `API::PageConfiguration`

**作用：** 创建单个 `WKWebView`/`WebPageProxy` 时的**静态配置**，是最常用的配置入口。

它聚合了其他对象的引用：

关键字段：
- `processPool` — 使用哪个进程池
- `websiteDataStore` — 使用哪个数据存储（决定 session）
- `preferences` — `WebPreferences`（JS 开关、功能开关等）
- `userContentController` — 注入脚本/内容规则
- `defaultWebsitePolicies` — 默认网站策略

**使用时机：** 创建 WebView 时传入，之后大部分字段不可修改。

---

### 3. `WebsiteDataStore`

**作用：** 这不是一个"配置类"，而是一个**运行时数据管理对象**，对应一个浏览 session。

管理的内容：
- Cookies、LocalStorage、IndexedDB、Cache、ServiceWorker 注册等
- 隐私保护（ITP/Tracking Prevention）
- 数据的增删查（`fetchData`、`removeData`）
- 对应一个 `PAL::SessionID`（persistent 或 ephemeral）

**使用时机：** 通过 `PageConfiguration::setWebsiteDataStore()` 关联到页面。多个 WebView 可以共享同一个 `WebsiteDataStore`（共享 session）。

---

### 4. `WebsitePoliciesData` 

**作用：** 这是**每次导航时动态下发给 WebProcess 的策略**，不是创建时的配置。

关键字段：
- `autoplayPolicy` — 自动播放策略
- `customUserAgent` — 覆盖 User-Agent
- `allowsContentJavaScript` — 是否允许 JS
- `preferredContentMode` — 桌面/移动模式
- `customHeaderFields` — 自定义请求头
- `contentExtensionEnablement` — 内容拦截规则开关

**使用时机：** 在 `decidePolicyForNavigationAction` 回调中，通过 `WKWebpagePreferences`（ObjC 层）动态设置，每次导航都可以不同。

---

### 一句话总结

| 类 | 层次 | 时机 | 可变性 |
|---|---|---|---|
| `ProcessPoolConfiguration` | 进程池 | 创建 Pool 前 | 一次性 |
| `PageConfiguration` | 单个页面 | 创建 WebView 时 | 创建时 |
| `WebsiteDataStore` | 数据/Session | 运行时管理 | 持续可操作 |
| `WebsitePoliciesData` | 单次导航 | 每次导航回调中 | 每次导航可变 |


# IPC机制
- 如Source\WebKit\UIProcess\WebPageProxy.cpp、WebPageProxy::setUserAgent
	- ` webProcess.send(Messages::WebPage::SetUserAgent(m_userAgent), pageID)`
	- 即WebPage实现SetUserAgent
		- Source\WebKit\WebProcess\WebPage\WebPage.messages.in
		- Source\WebKit\WebProcess\WebPage\WebPage.cpp

# Playwright curlProxy修改思路
- 配置WebsiteDataStore
	- 在Source\WebKit\UIProcess\WebsiteData\curl\WebsiteDataStoreCurl.cpp添加setNetworkProxySettings
		- 设置属性m_proxySettings
			- platformSetNetworkParameters时设置参数
		- 给networkProcess发送m_proxySettings IPC
			- 给现存的进程设置
	- 在Source\WebKit\NetworkProcess\NetworkProcess.h、Source\WebKit\NetworkProcess\NetworkProcess.messages.in添加setNetworkProxySettings
	- 在Source\WebKit\NetworkProcess\curl\NetworkProcessCurl.cpp实现setNetworkProxySettings
		-  networkStorageSession->setProxySettings
		- CurlContext::singleton().setProxySettings(proxySettings)
		- 然后在CurlContext用这个proxySettings

# Playwright App思路

- MainWindow：窗口，也是一个页面，只做了单窗口单页面功能
- WebKitBrowserWindow：WebView持有对象，控制WebView
- Tools\Playwright\win\WinMain.cpp：
	- `configureDataStore(WKWebsiteDataStoreRef dataStore)`：配置每个configureDataStore，包含此处创建第一个以及inspector的browserContext创建的
		- 其重新设置了proxy
		- 自己可以重新设置doh等
	- `WebKitBrowserWindow::createPageCallback(WKPageConfigurationRef configuration)`
		- 创建的每一个page的callback，包含此处创建第一个以及inspector的browserContext创建的
- Inspector
	- Source\WebKit\UIProcess\InspectorPlaywrightAgent.cpp
		- InspectorPlaywrightAgent就是PlaywrightBackendDispatcherHandler
	- Source\WebKit\UIProcess\InspectorPlaywrightAgentClient.cpp
	- inspector命令实现方法
		- 在ource\JavaScriptCore\inspector\protocol定义类型、命令（请求+响应）、监听事件（监听如Dom事件发送给客户端）
			- 如Playwright.json
			- 命令名=函数名、函数参数、函数返回值
		- 实现这些，如Source\WebKit\UIProcess\InspectorPlaywrightAgent.cpp
		- Source/JavaScriptCore/inspector/scripts/generate-inspector-protocol-bindings.py生成
			- `WebKitBuild\Release\JavaScriptCore\DerivedSources\inspector\InspectorFrontendDispatchers.cpp` 类（监听事件，发送消息）
			- InspectorFrontend（如PlaywrightFrontendDispatcher）
			- 生成 WebKitBuild\Release\JavaScriptCore\DerivedSources\inspector\InspectorBackendDispatchers.cpp（处理命令，接收和分发消息）
			- InspectorBackendDispatcher（如PlaywrightBackendDispatcher、PlaywrightBackendDispatcherHandler（全是虚函数））
			- 生成类型定义
			- WebKit原生实现的在Source\WebCore\inspector\agents中，如InspectorPageAgent.cpp
		- 每次修改，重新编译JavaScriptCore
			- 因为在Source\JavaScriptCore\CMakeLists.txt里执行了generate-inspector-protocol-bindings.py


# WebProcess


## WebProcess::Singleton

`usesSingleWebProcess` 的设置时机和方式取决于平台和配置：
1. Cocoa 平台（macOS/iOS）
	- 在 MiniBrowser 中，通过设置控制器的 `perWindowWebProcessesDisabled` 属性来决定
	- Tools/MiniBrowser/mac/AppDelegate.m (L294-297)
2. GLib 平台（GTK）
	- GLib API 已经废弃了单进程模式的选择。从 2.26 版本开始，只允许多进程模式
	-  Source/WebKit/UIProcess/API/glib/WebKitWebContext.cpp (L1790-1811)


# JS API

## bom对象navigator
- Source\WebCore\page\Navigator.cpp
### 绑定配置
Source\WebCore\page\Navigator.idl
### 生成的代码
- WebKitBuild\Release\WebCore\DerivedSources\JSNavigator.cpp
- JSNavigatorDOMConstructor::initializeProperties：初始化对象
- JSNavigatorPrototype::finishCreation：做一些条件过滤
	- 如userAgentData不满足添加就删除
		- `!(jsCast<JSDOMGlobalObject*>(globalObject())->scriptExecutionContext()->isSecureContext()`
			- `[SecureContext]`
		- `downcast<Document>(jsCast<JSDOMGlobalObject*>(globalObject())->scriptExecutionContext())->settingsValues().navigatorUserAgentDataJavaScriptAPIEnabled`
			- `[EnabledBySetting=NavigatorUserAgentDataJavaScriptAPIEnabled]`
			- WebKitBuild\Release\WebCore\DerivedSources\Settings.cpp
			- Source\WebCore\Scripts\SettingsTemplates\Settings.cpp.erb
			- Source\WebCore\Scripts\GenerateSettings.rb
			- Source\WebCore\CMakeLists.txt
				- 执行了GenerateSettings.rb，settings文件有
				- Source\WebCore\page\Settings.yaml
				- Source\WTF\Scripts\Preferences\UnifiedWebPreferences.yaml
			- 其实这个settings和preferences是一个意思，比如在Source\WebKit\WebProcess\WebPage\WebPage.cpp，WebPage::updatePreferences，就会复制prefeerences
		- `downcast<Document>(jsCast<JSDOMGlobalObject*>(globalObject())->scriptExecutionContext())->quirks().needsNavigatorUserAgentDataQuirk())``
			- `[EnabledByQuirk=needsNavigatorUserAgentData]`
		- 即要SecureContext
			- settings.navigatorUserAgentDataJavaScriptAPIEnabled：设置Source\WTF\Scripts\Preferences\UnifiedWebPreferences.yaml中设置NavigatorUserAgentDataJavaScriptAPIEnabled中的webcore为true
				- 或者简单点在Source\WebKit\UIProcess\API\C\WKPreferences.cpp中，添加WebPreferences::setNavigatorUserAgentDataJavaScriptAPIEnabled的函数，并在app里调用
			- quirks.needsNavigatorUserAgentDataQuirk：在Source\WebCore\page\Quirks.cpp添加域名handler 启用 NeedsNavigatorUserAgentData，或者直接设置Quirks#needsNavigatorUserAgentDataQuirk返回true


## Fetch

### 从fetch到被 MixedContentChecker block
1. fetch() → DocumentThreadableLoader::loadRequest(async 分支)DocumentThreadableLoader.cpp:604 → CachedResourceLoader::requestRawResource → requestResource
2. CachedResourceLoader::requestResource CachedResourceLoader.cpp:1115 调 canRequest(type=RawResource, ...)
3. canRequest 最后一步 CachedResourceLoader.cpp:628 调 checkInsecureContent
4. checkInsecureContent CachedResourceLoader.cpp:479(RawResource 命中那组 case)调 MixedContentChecker::shouldBlockRequest
5. MixedContentChecker::shouldBlockRequest MixedContentChecker.cpp:132:
  - isMixedContent(行 76)= isDocumentSecure(browserscan=https) && !SecurityOrigin::isSecure("http://127.0.0.1") → true
  - 行 145 那个"potentially trustworthy 就放行"的豁免,只在 isUpgradable == Yes 时生效;而 fetch 的 RawResource 是 IsUpgradable::No(CachedResourceLoader.cpp:447),所以豁免不适用
  - → return true(拦截)
6. checkInsecureContent 返回 false → canRequest 返回 false
7. requestResource 回到 CachedResourceLoader.cpp:1117,造出 ResourceError{..., "Not allowed to request resource", ResourceError::Type::AccessControl}
8. DocumentThreadableLoader::loadRequest:609 → logErrorAndFail → logError(ThreadableLoader.cpp:166):因为 error.isAccessControl() 为真,拼出 " due to access control checks."

## includes
- 像Source\WebCore\Modules\WebGPU\NavigatorGPU.idl ，没有单独的cpp实现文件，其是一个mixin，在Source\WebCore\page\Navigator.idl中`Navigator includes NavigatorGPU;`，因此实现文件也在Navigator.cpp

# XXXRef指针机制

 1. 为什么不直接用 WebPageProxy*？

  因为 WebKit 的 C API 需要向前兼容和二进制兼容。如果直接暴露 WebPageProxy*，C
  代码就能看到类的内部（成员函数、成员变量），后续版本改了 WebPageProxy 的内部结构就会破坏所有已编译的代码。

  typedef const struct OpaqueWKPage* WKPageRef 是一个不透明指针（opaque pointer）：

  // 在 .h 里只声明了 struct 名，没定义它的成员
  typedef const struct OpaqueWKPage* WKPageRef;

  // 使用者只能声明和传递指针，无法解引用
  WKPageRef page = GetSomePage();   // ✅ 可以
  page->doSomething();              // ❌ 编译错误，struct 不完整

  这样 C 侧代码对这个指针什么也做不了，只能把它传给其他 C API 函数。WebKit 内部在 toImpl 里再把它转回真实的
  WebPageProxy*。这就是接口与实现分离。

  2. WK_ADD_API_MAPPING 是什么？

  它是一个宏，用来给模板提供类型映射表。不是 toImpl 的声明也不是实现。

```c++
#define WK_ADD_API_MAPPING(TheAPIType, TheImplType) \
  template<> struct APITypeInfo<TheAPIType> {      \
	  using ImplType = TheImplType;                 \
  };
template<typename APIType> struct APITypeInfo;

// 使用：
WK_ADD_API_MAPPING(WKPageRef, WebPageProxy)
// 展开为：
template<> struct APITypeInfo<WKPageRef> {
  using ImplType = WebPageProxy; // 类型别名
};
// 也就是说定义APITypeInfo<WKPageRef>类型
```


  这相当于说："给模板系统注册一条记录：WKPageRef → 对应的实现类是 WebPageProxy"。

  3. toImpl 是什么？

  toImpl 是模板函数（在 WKSharedAPICast.h 里）：

```c++
template<typename T, typename ImplType = typename APITypeInfo<T>::ImplType>
auto toImpl(T t) -> ImplType*
{
  return downcast<ImplType>(API::Object::unwrap(/* ... */));
}
```

  它的工作原理：
```c++
toImpl(wkPageRef)           // T = WKPageRef
→ APITypeInfo<WKPageRef>  // 模板推导，找到映射：ImplType = WebPageProxy
→ 返回类型 = WebPageProxy* // 自动推导，无需手动指定
 
// 这就解释了为什么 toProtectedImpl(pageRef) 返回 RefPtr<WebPageProxy>：
toProtectedImpl(pageRef)
→ toImpl(pageRef)                   // WKPageRef → WebPageProxy*
→ RefPtr<WebPageProxy>(webPageProxy) // 自动包装成智能指针
```
  4. 整个模式的总结

  ┌─ C API（对外公开）────────────────────────────────┐
  │  WKPageRef = OpaqueWKPage*     ← 不透明指针       │
  │  void WKPageSetCustomUserAgent(WKPageRef, ...)     │
  └────────────────────────────────────────────────────┘
                           │
                           ▼
  ┌─ WKAPICast（内部转换）─────────────────────────────┐
  │  WK_ADD_API_MAPPING(WKPageRef, WebPageProxy)       │
  │  toImpl(wkRef) → WebPageProxy*                     │
  └────────────────────────────────────────────────────┘
                           │
                           ▼
  ┌─ WebKit 内部（真正的实现）────────────────────────┐
  │  WebPageProxy::setCustomUserAgent(...)              │
  └────────────────────────────────────────────────────┘

  不用直接 WebPageProxy* 的原因：
  - 二进制兼容性：不透明指针的 ABI 不会变
  - 语言边界：C 接口可以被任何语言调用（Python、Rust 等通过 FFI）
  - 编译隔离：C 侧不需要 include WebKit 内部头文件
  - 安全：C 测无法直接操作对象内部


# 日志

## Release日志
- 用法：`RELEASE_LOG(channel, "xxxx")`
	- 分等级：RELEASE_LOG_DEBUG、RELEASE_LOG_INFO、RELEASE_LOG_ERROR
- `#define RELEASE_LOG_DISABLED !(USE(OS_LOG) || ENABLE(JOURNALD_LOG) || OS(ANDROID))`
	- 默认stderr，因此如果没有实现则可以定义RELEASE_LOG_DISABLED=0

- `Source/WebKit/Platform/Logging.h`：定义chanel
```c++
#ifndef LOG_CHANNEL_PREFIX
#define LOG_CHANNEL_PREFIX WebKit2Log
#endif

#define WEBKIT2_LOG_CHANNELS(M) \ M(API) \ ...
WEBKIT2_LOG_CHANNELS(DECLARE_LOG_CHANNEL)
```
- Source\WTF\wtf\Assertions.h
```c++
#define DECLARE_LOG_CHANNEL(name) \ extern WTFLogChannel LOG_CHANNEL(name);

#define LOG_CHANNEL(name) JOIN_LOG_CHANNEL_WITH_PREFIX(LOG_CHANNEL_PREFIX, name)
#define LOG_CHANNEL_ADDRESS(name) &LOG_CHANNEL(name),
#define JOIN_LOG_CHANNEL_WITH_PREFIX(prefix, channel) JOIN_LOG_CHANNEL_WITH_PREFIX_LEVEL_2(prefix, channel)
#define JOIN_LOG_CHANNEL_WITH_PREFIX_LEVEL_2(prefix, channel) prefix ## channel


typedef struct {
    WTFLogChannelState state;
    const char* name;
    WTFLogLevel level;
#if !RELEASE_LOG_DISABLED && USE(OS_LOG)
    SUPPRESS_UNRETAINED_MEMBER __unsafe_unretained os_log_t osLogChannel;
#endif
} WTFLogChannel;
```
- 如 对WEBKIT2_LOG_CHANNELS里的每一个channel
	- `extern WTFLogChannel WebKit2LogAPI`  (`##`是字符串拼接)



### 在 Windows 上如何实现

Windows 目前走的是 `RELEASE_LOG_DISABLED` 分支，原因是没有定义 `ENABLE_RELEASE_LOG`。要在 Windows 上启用，有两种思路：

**方案 A：启用 fallback 的 `fprintf(stderr)` 分支**

在 CMake/构建系统中加入：

```
add_compile_definitions(ENABLE_RELEASE_LOG=1)
```

这会让 `RELEASE_LOG_DISABLED` 变为 0，然后走到 `else` 分支，用 `fprintf(stderr)` 输出。这是改动最小的方式。

**方案 B：添加 Windows 原生分支（ETW 或 OutputDebugString）**

在 `Assertions.h` 的 `#elif ENABLE(JOURNALD_LOG)` 之后、`#else` 之前，添加：

```
#elif OS(WINDOWS)    #define RELEASE_LOG(channel, ...) do { \      auto& logChannel = LOG_CHANNEL(channel); \      if (logChannel.state != WTFLogChannelState::Off) { \          char buf[1024]; \          snprintf(buf, sizeof(buf), "[WebKit:%s] " __VA_ARGS__); \          OutputDebugStringA(buf); \      } \  } while (0)
```

`OutputDebugString` 输出到 Windows 调试器（Visual Studio Output 窗口 / DebugView 工具）。更完整的方案是用 **ETW（Event Tracing for Windows）**，类似 `os_log` 的结构化日志，但实现复杂得多。



# 进程关系和启动
- 类似点
	- 进程：XXXProcess
	- 客户端控制Process的类：XXXProcessProxy类
	- XXXCreationParameters.h、XXXCreationParameters.serialization.in：进程IPC  initialize的参数
	- 每个进程相关的类都继承AuxiliaryProcess，通用的可以放在此处
- Source\WebKit\UIProcess\AuxiliaryProcessProxy.cpp
	- 一创建立刻connect、**initialize**（使用创建参数调用初始化IPC））
- Source\WebKit\Shared\AuxiliaryProcess.cpp
- **Source\WebKit\Shared\AuxiliaryProcessCreationParameters.h**
- Source\WebKit\Shared\AuxiliaryProcessCreationParameters.serialization.in
- Source\WebKit\Shared\AuxiliaryProcessMain.h
	- 主程序，直接
		- platformInitialize
		- parseCommandLine
		- InitializeWebKit2
		- initializeAuxiliaryProcess
		- run
		- platformFinalize
	- 平台覆盖，如Source\WebKit\Shared\win\AuxiliaryProcessMainWin.cpp
	- 各进程不同平台有不同实现，如
		- Source\WebKit\NetworkProcess\NetworkProcessMain.h
		  - Source\WebKit\NetworkProcess\EntryPoint\win\NetworkProcessMain.cpp
		  - Source\WebKit\NetworkProcess\curl\NetworkProcessMainCurl.cpp
		  - `AuxiliaryProcessMain<NetworkProcessMainCurl>(argc, argv)`
		- Source\WebKit\WebProcess\EntryPoint\win\WebProcessMain.cpp
		  - Source\WebKit\WebProcess\win\WebProcessMainWin.cpp
		  - `AuxiliaryProcessMain<WebProcessMainWin>(argc, argv)`
		- 