- 非持久化context的userdatadir`%temp%/playwright_chromiumdev_profile-xxxxx`

- 3种启动方式
	- Launh：仅启动后台浏览器，无context，必须newContext来操作浏览器
		- 无法设置userdatadir（临时目录），完全无状态
		- `"D:\data\playwright\chromium-1169\chrome-win\chrome.exe" --disable-field-trial-config --disable-background-networking --disable-background-timer-throttling --disable-backgrounding-occluded-windows --disable-back-forward-cache --disable-breakpad --disable-client-side-phishing-detection --disable-component-extensions-with-background-pages --disable-component-update --no-default-browser-check --disable-default-apps --disable-dev-shm-usage --disable-extensions --disable-features=AcceptCHFrame,AutoExpandDetailsElement,AvoidUnnecessaryBeforeUnloadCheckSync,CertificateTransparencyComponentUpdater,DeferRendererTasksAfterInput,DestroyProfileOnBrowserClose,DialMediaRouteProvider,ExtensionManifestV2Disabled,GlobalMediaControls,HttpsUpgrades,ImprovedCookieControls,LazyFrameLoading,LensOverlay,MediaRouter,PaintHolding,ThirdPartyStoragePartitioning,Translate --allow-pre-commit-input --disable-hang-monitor --disable-ipc-flooding-protection --disable-popup-blocking --disable-prompt-on-repost --disable-renderer-backgrounding --force-color-profile=srgb --metrics-recording-only --no-first-run --enable-automation --password-store=basic --use-mock-keychain --no-service-autorun --export-tagged-pdf --disable-search-engine-choice-screen --unsafely-disable-devtools-self-xss-warnings --no-sandbox --user-data-dir="C:\Users\devp\AppData\Local\Temp\playwright_chromiumdev_profile-Uc88vD" --remote-debugging-pipe --no-startup-window --flag-switches-begin --flag-switches-end`
	- LaunchPersistentContext：只能用一个BrowserContext
		- 可以设置userdatadir，但不能传到Args设置，只能直接设置  
		- 无browser、只有一个context（userdatadir）
	- ConnectOverCDP：继承该浏览器的所有BrowserContext
		- browser、context的close被无视（用pw的Launch则会优雅关闭）
- BrowserContext
	- NewBrowserContext
		- 无pages，必须自己手动new一个
		- 仅其可以设置StorageState
		- userdatadir：如`%TEMP%/playwright_chromiumdev_profile-Uc88vD`，会自动创建、删除（BrowserContext关闭事件）
	- AddCookies：不会根据当前pages进行过滤，有则替换，无则添加，失效则忽视

- 对于userdatadir（其实最好还是不要用这个，推荐完全无状态的，通过StorageState、AddCookies来管理状态）
	- 不会立即让浏览器进行刷盘（即cookie可能会丢失），不过通过页面加载可让浏览器触发刷盘机制