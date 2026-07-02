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
- 执行 `node package/cli.js run-driver` 
	- run-driver：其他语言执行这个，用进程输入输出JSON交互，可以多开浏览器
	- run-server：远程Playwright服务器，用PlaywrightServer进行ws交互，可以多开浏览器，通过请求头设置参数启动BrowserServer，一个wsclient对一个浏览器，无法多个ws共享一个浏览器。
		- 多个wsclient对一个浏览器：928dee489672b156d2fd063fa04b7ab4a7188cf9, 自v1.53.0 2025-05-23 10:07:33 +0000 起有这个功能，但是截止 v1.61.1 2026-060-30都没有改为一个正式的api（可以用，但是选项是`_xxx`, 不像是可以正式用的样子）
	- launch-server：启动一个BrowserServer，即只能打开一个浏览器
	- close：run-driver、run-server、launch-server的client执行close都会进行gracefully close，即需要执行playwright对象的close，无需执行browser、browserContext的close，会直接向浏览器发送close命令
		- run-server：关闭输入=close
		- launch-server：关闭进程=close或者浏览器进程
- 使用Playwright中的BrowserType
	- Launch：使用node启动浏览器，返回一个浏览器（无contexts）
	- LaunchPersistentContext：使用node启动浏览器，且仅返回一个context，browser对象是nil，只能有一个context
	- Connect：连接用node启动的浏览器（也就是连接用一个js服务器启动的浏览器）
		- Browser#Close、Playwright#Close都会关闭playwright，因为浏览器被关闭了
	- ConnectOverCDP：直接使用CDP连接已经启动的浏览器
- 每个BrowserContext都是一个独立的浏览器，newContext并不是无痕，而是一个特殊的独立浏览器，用独立的cookies等数据
- close
	- node,browser
	- 关闭pw，browser也会被关闭
	- 关闭本进程，node、browser也会被关闭
	- 关闭持久化进程，建议先关闭browserContext，表现得像termiate

