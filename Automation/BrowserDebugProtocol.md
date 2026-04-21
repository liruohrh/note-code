# Chrome Devtool Protocol
- `http://{host}:{--remote-debugging-port}/json/version`
	- 查看是否开启
	- 查看如`webSocketDebuggerUrl`
- `http://{host}:{--remote-debugging-port}/json/`
	- 查看所有页面
	- 远程调试页面
	- 在`chrome://inspect/#devices`添加Discover network targets，即`{host}:{--remote-debugging-port}`
	- 这个响应中有`devtoolsFrontendUrl`其就只是在一个页面上进行页面调试，和`chrome://inspect/#devices`一样
		- 如`https://chrome-devtools-frontend.appspot.com/serve_rev/@97d495678dc307bfe6d6475901104e262ec7a487/inspector.html?ws=localhost:18080/devtools/page/37B4F8D85D25F60CDC16FA9A0B3DA56D`
			- [chromium devtools-frontend](https://chromium.googlesource.com/devtools/devtools-frontend)
		- 不过这个需要开启`--remote-allow-origins="*"`（*表示任意），否则的话只能自己做一个websocket中转
# WebKit
- [WebInspectorUI](https://github.com/WebKit/WebKit/tree/main/Source/WebInspectorUI/UserInterface)
	- 使用方式好像类似于chromium：`http://localhost:8080/Main.html?ws=localhost:9222/devtools/page/1`
- https://github.com/artygus/webkit-webinspector
	- 封装了一点点东西
- https://github.com/RemoteDebug/remotedebug-ios-webkit-adapter
	- 被取代为： https://inspect.dev/
	- 接替者开源仓库： https://github.com/HimbeersaftLP/ios-safari-remote-debug-kit