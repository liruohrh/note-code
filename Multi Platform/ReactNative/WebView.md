- react-native-webview
```jsx
<WebView source={{ uri: url, headers }}/>
```
- source可以看作被WebView作为useEffect的依赖了，更新会重新加载source

# 交互
- React Native => WebView
	- injectedJavaScript：page loaded执行，即DOMContentLoaded已经发生过了
		- 必须返回`true`
		- **IOS必须设置onMessage**
	- `webViewRef.injectJavaScript`：允许执行多次JS
	- injectedJavaScriptBeforeContentLoaded：在创建 document 元素之后但在其他子资源完成加载之前执行
	- injectedJavaScriptObject：window.onload时也可用，传递对象给WebView，不过因为是JSON序列化，因此不能使用引用，也就是说是一个只读的
		- WebViewAPI：`window.ReactNativeWebView.injectedObjectJson()`
	- `webViewRef.postMessage(str)`：在webView中监听window的message事件
- WebView => React Native
	- WebViewAPI：`window.ReactNativeWebView.postMessage(str)`
	- `<WebView onMessage={(event)=>event.nativeEvent.data}/>`

# Cookie
- https://github.com/react-native-webview/react-native-webview/blob/master/docs/Guide.md#managing-cookies
- 自己传递headers也可以