- [Firefox扩展开发文档](https://developer.mozilla.org/zh-CN/docs/Mozilla/Add-ons/WebExtensions)
- [Chrome/Chromium扩展开发文档](https://developer.chrome.com/docs/extensions?hl=zh-cn)

# 创建项目与应用扩展

- 项目结构
  - 对于 chrome，只需要一个 manifest.json 即可
- 加载扩展
  - 对于 chrome，打开扩展程序页面，点击加载已解压的扩展程序，选择项目根目录，还可以点击刷新按钮进行更新

# 插件结构

- manifest.json
  - 项目信息，权限申请等
  - 在根目录下
- service worker
  - 监听事件等，比如快捷键
  - 通常是根目录下的 background.js（设其`background.service_worker`）
  - [支持的事件/API](https://developer.chrome.com/docs/extensions/mv3/service_workers/events/)
- content scripts
  - 内容脚本文件，即对页面的脚本
  - 通常是根目录下的 scripts，需要设置在`content_scripts`中，为 scrpits 分组，每组可以包含多个 js 文件，多个 matches 规则
- The popup and other pages
  - 弹出页面（点击插件图标时弹出）和其他页面
  - popup 可以单独立写在 popup 目录
- 交互模式
  - 基于`chrome.action.onClick`的全自动模式（点击扩展仅仅启动扩展，可以在 Badge 中显示 text 告诉用户是否开启了）
    - 逻辑主要集中在 background 和 content scripts
      - service worker 可以调用`chrome.scripting`（比 content scritp 更加灵活）
  - 基于`popup`的多菜单多设置模式（点击扩展，可以启动，也可以设置启动，以及设置其他东西）
    - 每次点击 popup 会重新渲染 popup 页面/执行 js（即每次都会恢复初始状态）
- 生命周期
  - popup：点击扩展安装后到点击其他地方关闭扩展的 popup
    - 启动
      - 扩展启动（点击扩展按钮就是启动扩展）
      - 刷新 devtools
  - service_worker：一直在后台（但是有可能会停止）
    - 启动
      - 扩展启动
    - [https://developer.chrome.com/docs/extensions/mv3/service_workers/service-worker-lifecycle/#installation](https://developer.chrome.com/docs/extensions/mv3/service_workers/service-worker-lifecycle/#installation)
  - content_script：与页面绑定，即与 tab 绑定
    - 启动
      - 页面加载完
- 通信
  - 发送消息并处理响应：`chrome.runtime.sendMesage`
    - 对于 content_script，因为其与 tab 绑定，因此最好用`chrome.tabs.sendMessage`指定 tab 发送
  - 监听消息并响应：`chrome.runtime.onMessage`
    - sender 带有 tab，对于 content script 比较方便，不用再查询 tabs
  - 利用`chrome.storage`和`chrome.storage.onChanged`也可以做成通信的效果，但是要只要值必须要改变，最好就带上时间戳
- [debug](https://developer.chrome.com/docs/extensions/mv3/tut_debugging/#debug_bg)
	- manifest.json：
		- 添加扩展时
		- 扩展管理页面的 Errors 按钮
	- service worker：
		- 扩展管理页面的 Errors 按钮
		- 扩展管理页面点击 Service Worker 会打开到 devtools 进行调式（比如打印到控制台）
		- 打开 chrome-extension://YOUR_EXTENSION_ID/manifest.json，打开 devtools，applications/service workers
		  - 如果修改了，点击 update
		  - 如果需要调式，点状态旁边的 start
	- content_scripts：
		- 扩展管理页面的 Errors 按钮
		- 该页面的 devtools，控制台中顶部有个下拉菜单选择扩展/所有
	- popup：
		- 扩展管理页面的 Errors 按钮
		- 因为是单独的页面，因此需要右键检查，单独打开一个 devtools（如果需要重新加载，刷新 devtools）

# chrome API

- [https://developer.chrome.com/docs/extensions/reference](https://developer.chrome.com/docs/extensions/reference)
- [简单的介绍](https://juejin.cn/post/7035782439590952968#heading-21)

## 使用范围

|                  | service_worker | content_script | popup |
| ---------------- | -------------- | -------------- | ----- |
| chrome.action    | ✔️             | ✔️             | ✔️    |
| chrome.commands  |                |                |       |
| chrome.runtime   | ✔️             | ✔️             | ✔️    |
| chrome.windows   | ✔️             |                | ✔️    |
| chrome.tabGroups | ✔️             |                | ✔️    |
| chrome.tabs      | ✔️             |                | ✔️    |
| chrome.scripting | ✔️             | ✔️             | ✔️    |
| chrome.omnibox   | ✔️             |                | ✔️    |
| chrome.storage   | ✔️             | ✔️             | ✔️    |
| chrome.alarms    | ✔️             | ❌             | ❌    |
| await/module     | ✔️             | ❌             | ✔️    |
|                  |                |                |       |

## chrome.action

- 代表右上角插件按钮
- 比如 Badge（徽章，标记），就是右上角插件，可以设置文字，背景色等
- `onClick`点击插件按钮事件，传入当前标签页（但是当有 popup 不会触发）

## chrome.commands

- 监听快捷键，发出命令事件

## chrome.runtime

- `chrome.runtime.onInstalled`安装后（第一次安装后，更新也算安装，chrome 更新也算安装）
  - 参数：InstalledDetails
    - reason：一个枚举
      - `export enum OnInstalledReason {INSTALL = "install",UPDATE = "update",CHROME_UPDATE = "chrome_update",SHARED_MODULE_UPDATE = "shared_module_update"}`
    - previousVersion：更新前的版本
- `chrome.runtime.onMessage`从一个 js 中发送来的消息（`chrome.runtime.sendMessage`），需要响应一个值
  - 参数：
    - message：`sendMessage`方法的 message 对象
    - sender：发送脚本信息
    - sendResponse：响应一个 any

## chrome.windows

- 浏览器有 N 个 window，一个 window 有 N 个 Tab
- `chrome.windows.update(windowId, {focused: true})`更新 window 为聚焦状态

## chrome.tabGroups

- 一个 TabGroup 可以有 N 个 Tab，一个 Tab 可以不属于任意一个 TabGroup

## chrome.tabs

- 与标签页交互, [https://developer.chrome.com/docs/extensions/reference/tabs/](https://developer.chrome.com/docs/extensions/reference/tabs/)
- Tab
  - id：tab 的 id
  - title：tab 的标题
  - windowId：所属 window
  - groupId：所属 tabGroup
  - active：表示是活跃的，并不是表示是被选中的
  - highlighted：当前窗口高亮的 tab，即选中的 tab（chrome 33 之前是 selected）
- `chrome.tabs.query(queryInfo[, callback])`该函数可以从当前窗口中查询符合条件的 tabs（空对象表示获取所有）
- `chrome.tabs.update(tabId, {highlighted: true})`更新 tab 为选中状态（不知道为什么设置 active=true 也可以）

## chrome.scripting

在指定标签页执行脚本

## chrome.omnibox

- 操作地址栏，输入关键字后（配置`"omnibox": {"keyword": "api"}`）按空格或者点击即可，会有一个扩展的 icon-16
- `chrome.omnibox.onInputEntered`
- `chrome.omnibox.onInputChanged`

## chrome.storage

- `chrome.storage.local`适合存储大量数据
- `chrome.storage.sync`会同步到用户登录的所有 chrome 浏览器
- `chrome.storage.session`数据会进行加密
- `chrome.storage.managed`

## chrome.alarms

- 定时器（使用这个比 setTimeout 更好一些）
- `chrome.alarms.create`创建定时事件（最好带上 name，监听器就可以根据 name 做判断）
  - 有 callback 时会调用 callback，但是 onAlarm 监听器仍会执行
  - 如果同名则取消早发生的
  - 使用解压即开发时，不会限制 alarm，但是正式上线时，至少 1 分钟才会触发
  - 使用解压的扩展，会立即触发，忽视延迟
- `chrome.alarms.onAlarm`监听定时事件

# 报错

- Could not establish connection. Receiving end does not exist.
  - service worker 使用 tabs 发生消息，但是 content script 并没有激活
    - 可能需要刷新一下 content script 对应的页面

# V3 的问题

- service worker 改为不是一直活跃的状态，会不断安装卸载
  - 像 setTimeout 这样的方法就不能保证可以触发（但也不一定，大部分情况还是可以用的）
