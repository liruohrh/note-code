# 调用
```kotlin

val webView = createWebView()
call(webView)



func createWebView(): WebView{
    val webView = WebView(splitties.init.appCtx)
    webView.settings.run{
	    javaScriptEnabled=true
	    domStorageEnabled=true
	    blockNetworkImage=true
	    userAgentString=xxx
	    mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
    }
    webView.webViewClient = xxx
}

func call(webView: WebView){
	if(isLoadHtml){
		if(hasHistoryURL){
		    webView.loadDataWithBaseURL(url, html, "text/html", getEncoding(), url)
		}else{
			webView.loadData(html, "text/html", getEncoding())
		} 
	}else{
		if(hasAdditionalHttpHeaders){
			webView.loadUrl(url!!, additionalHttpHeaders)
		}else{
			webView.loadUrl(url!!)  
		}
	}
}
```


# WebView常见Settings
- LoadsImagesAutomatically（true）：自动加载data/network url schema的image（即img标签）
- BlockNetworkImage（false）：阻断加载network url schema的image
- BlockNetworkLoads：阻断加载所有网络资源
	- 有android.Manifest.permission.INTERNET时默认false
	- 没有网络权限时设置为false，会抛出 SecurityException 
- JavaScriptEnabled（false）：可执行JS
- DomStorageEnabled（false）：DOM Storage API
- UserAgentString：设置后，忽视User-Agent Client Hints headers 和 navigator.userAgentData
- CacheMode：
- MixedContentMode：http/https

# WebView常见方法
- evaluateJavascript：执行JS，返回值回调

# WebViewClient
- 接收notifications 和 requests
	- 比如拦截网络请求，执行page加载完成回调
- 主要方法
	- onPageFinished：page加载完成
		- 因为页面是异步绘制的，页面的JS可能会修改DOM，page就不算加载完
			- `webView.postVisualStateCallback`：在WebView#onDraw前执行
	- onReceivedSslError：资源请求发生SSL错误
- shouldInterceptRequest：拦截请求，返回响应
	- 响应为null则继续执行这个请求
- shouldOverrideUrlLoading：撤销URL的加载，即取消请求
- onLoadResource：将要加载的资源


# 坑
- https://blog.csdn.net/AoXue2017/article/details/113705253