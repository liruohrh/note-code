
# 对比

✅❌



|                        | [playwright-cli](https://github.com/microsoft/playwright) | [browser-agent](https://github.com/browser-use/browser-use) | [agent-browser](https://github.com/vercel-labs/agent-browser) | [Avenir-Web](https://github.com/Princeton-AI2-Lab/Avenir-Web) |
| ---------------------- | --------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| 元素操作方式                 | DOM清洗                                                     | DOM清洗                                                       | DOM清洗                                                         | 文本+状态+视觉                                                      |
| 指定用户数据目录               | ✅--profile                                                | ❌                                                           | ✅--profile                                                    |                                                               |
| 指定会话（浏览器会话，用于多开时指定浏览器） | ✅--s                                                      | ✅--session                                                  | ✅--session                                                    |                                                               |
| 指定浏览器可执行路径             | ❌                                                         | ❌                                                           | ❌                                                             |                                                               |
| 默认系统浏览器                | ✅                                                         | ✅                                                           | ✅                                                             |                                                               |
|                        |                                                           |                                                             |                                                               |                                                               |
|                        |                                                           |                                                             |                                                               |                                                               |
|                        |                                                           |                                                             |                                                               |                                                               |
|                        |                                                           |                                                             |                                                               |                                                               |

# 其他
- session：浏览器会话，就和双击运行一个浏览器一样，用来标识正在运行的浏览器，无其他作用
- profile：
	- playwright、agent-browser：指定userdatadir
		- agent-browser：相对路径会放在`~\.agent-browser\browsers\chrome-147.0.7727.57`
	- browser-use：拷贝系统浏览器profile
- agent-browser：可以设置很多参数，还有一个不错的dashboard webapp
-  browser-use：默认使用系统浏览器
	- 用户数据目录：只能是临时的，默认全新用户数据目录
		- 指定profile：从系统浏览器profile中拷贝到临时目录
			- Default：默认profile，对于chrome来说，如果有登录Google账号，那么会要求手动验证一次（即登录）
			- 其他profile
	- 数据管理：只有cookie命令
	- 因此用什么profile无所谓，用户数据目录无法控制，想要管理登录态，只能用cookie命令
	- **browser-use-tui** 可以设置用户数据目录、profile，但是必须配置模型，只能执行任务


# 人爬的过程
- 打开网页
- 查看页面
- 如果没有找到自己要的，且有东西在加载，就等一下
- 还是没有自己要的，就找一下自己要的相近的
- 怎么找的？文本或者语义化图片
- 找到后，元素定位
	- id
	- 一些accessibility属性
	- class（可能最多找3个父级的定位）
	- 最后才是文本