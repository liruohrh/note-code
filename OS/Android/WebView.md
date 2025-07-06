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
		//UserAgent放在headers中是无用的，必须给webview.settings设置
		//如果url不以/结尾，会自动变为以/结尾
			webView.loadUrl(url!!, additionalHttpHeaders)
		}else{
			webView.loadUrl(url!!)  
		}
	}
}
```


# WebView常见Settings
- loadsImagesAutomatically（true）：加载所有schema的image
- blockNetworkImage（false）：阻断加载网络schema的image
- blockNetworkLoads：阻断加载所有网络资源
	- 有android.Manifest.permission.INTERNET时默认false
	- 没有网络权限时设置为false，会抛出 SecurityException 
- javaScriptEnabled（false）：可执行JS
- domStorageEnabled（false）：DOM Storage API
- userAgentString：不设置就用默认的，在headers中的是会被忽视的
- CacheMode：
- MixedContentMode：http/https混合

# WebView常见方法
- evaluateJavascript：执行JS，回调接收返回值
	- 返回值：返回最后一行执行的表达式，无返回值则是字符串`"null"`

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

执行顺序（[可以做个参考](https://blog.csdn.net/freak_csh/article/details/95530243)）
- onPageStarted
- shouldOverrideUrlLoading (if navigation by click or js)
	- 如果重定向，回到onPageStarted，这个原本的URL可能也会进行调用onPageFinished
- shouldInterceptRequest (many times per resource)
- onReceivedHttpError/onReceivedError (optional)
- onPageFinished：对于动态部分则可能仍然在进行中



# 坑
- https://blog.csdn.net/AoXue2017/article/details/113705253