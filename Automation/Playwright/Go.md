- `playwright.Install`：安装驱动、浏览器
	- 默认路径：`%APPDATA%/ms-playwright-go`
- 运行
	- 启动NodeJS服务器：`playwright.Run`
		- `node cli.js run-driver`
	- 启动浏览器：
		- `pw.Chromium.ConnectOverCDP`：使用CDP连接已启动的浏览器
		- `pw.Chromium.LaunchPersistentContext`：使用Playwright启动浏览器


- 所有操作都有超时时间，可在Page#SetDefaultTimeout设置，默认30s
- 对于load事件，如果已经load，则立即返回，如果页面重新加载，则重新等待load

- CSS Selector就是Locator（有更多特殊的用法比如WaitFor，所有元素都是一个Locator，Page也是一个Locator）
	- 一些特殊的Locator GetBy操作
		- Text：是一个interface{}类型，因为可以是字符串、regexp.Regexp
			- GetBy的时候还有Exact选项（精确匹配，即完全相等）
			- 注意：
				- 这个text是多空格变一个、换行变空格、trimSpace后的text，且input.type是button、submit匹配的是value而不是text content
				- 匹配的是最小元素
	- Err：这个方法不是获取Err，也不知道是什么，Locator必须要执行一个操作后才会进行获取，如`Locaotr(xx).Waitfor`

# 启动
- 使用Playwright中的BrowserType
	- Launch：使用node启动浏览器，返回一个浏览器（无contexts）
	- LaunchPersistentContext：使用node启动浏览器，且仅返回一个context，browser对象是nil，只能有一个context
	- Connect：连接用node启动的浏览器（也就是连接用一个js服务器启动的浏览器）
	- ConnectOverCDP：直接使用CDP连接已经启动的浏览器
- 每个BrowserContext都是一个独立的浏览器，newContext并不是无痕，而是一个特殊的独立浏览器，用独立的cookies等数据

