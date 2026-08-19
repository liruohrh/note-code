+ [https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Cookies](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Cookies)
+ 遵循RFC，如[RFC6265](https://www.rfc-editor.org/rfc/rfc6265)
+ Header：请求=Cookie，响应=Set-Cookie
    - Cookie值是多个`cookieName=cookieValue;`拼接
    - Set-Cookie值是一个Cookie字符串，`; ATTR=VAL`拼接，不需要编码
        * Bool值：无=VAL
        * 多个Cookie则多个Set-Cookie

# Cookie属性
+ [https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Set-Cookie](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Set-Cookie)
+ name：名
+ value：值
    - 规范：如在[RFC6265](https://www.rfc-editor.org/rfc/rfc6265#page-8)中：无编码，可以是 US-ASCII 字符集中除了控制字符（CTLs）、空白字符、双引号、逗号、分号和反斜杠之外的任何字符
    - 一般可能直接用URL/Base64编码
+ secure：true则必须使用HTTPs
    - localhost时http也允许
+ http-only：true则不允许JS访问，因此说这样的Cookie仅作用于服务器
    - 设置为true，有助于防止[跨站脚本（xss）攻击](https://developer.mozilla.org/zh-CN/docs/Web/Security/Types_of_attacks#%E8%B7%A8%E7%AB%99%E8%84%9A%E6%9C%AC%EF%BC%88xss%EF%BC%89)

## 匹配请求
+ domain：允许访问Cookie的域名，包含子域名，如`Domain=a.com`，则`b.a.com`也行
+ path：允许发送Cookie的请求path，包含子路径，如`Path=/docs`，则`/docs/a`也行

## 过期时间
+ expires：早期的max-age，使用时间字符串
    - 如：`Wed, 21 Oct 2015 07:28:00 GMT`
+ max-age：客户端有效期，单位为秒
    - `-1`表示`session`，即浏览器会话期间有效
        * `-1`时max-age不需要写入Cookie字符串中
    - 设置这个，有助于防止[会话劫持攻击](https://developer.mozilla.org/zh-CN/docs/Web/Security/Types_of_attacks#%E4%BC%9A%E8%AF%9D%E5%8A%AB%E6%8C%81)

## same-site
### Lax
- 默认
- 顶级导航+安全的请求方法才能 [跨站](跨站与同源.md) （注意和同源无关）
	- 这是 `Lax` 的设计取舍：保住"从外部链接进来仍然认得你"的体验，同时挡住 CSRF 与跨站追踪。`Strict` 连第一行都不放行——从外站链接进来会显示未登录，因此很少有站点对登录态使用 `Strict`。

#### 顶级导航
指导致地址栏那一层（顶层浏览上下文）发生跳转的导航：

|算顶级导航|不算|
|---|---|
|点击 `<a href>` 跳转|iframe 内部的任何导航|
|`window.location = ...`|`<iframe src>` 加载|
|表单提交导致主页面跳转|`fetch` / XHR|
|`window.open()`|`<img>` `<script>` `<link>` 等子资源加载|

#### 安全方法
指 `GET`、`HEAD` 这类不改变服务端状态的方法（libsoup 中即 `SOUP_METHOD_IS_SAFE` 宏）。

实际效果：

|场景|顶级导航|安全方法|Lax cookie|
|---|---|---|---|
|从外站点链接进入本站|✓|✓ GET|**发送** —— 保持登录态|
|外站用 POST 表单提交到本站|✓|✗ POST|不发 —— 挡住 CSRF|
|外站把本站塞进 iframe|✗|✓ GET|不发 —— 挡住跨站追踪|
|外站的 XHR 请求本站接口|✗|✓ GET|不发|

### None
跨域必须secure=true
### Strict
允许跨站

# 问题
## 不知道为什么，在2024/8/10突然发现BUG，springboot2.7.12+axios设置session的cookie没有按要求设置Cookie，导致正常跨域失败
- [https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Set-Cookie](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Set-Cookie)
- 即same-site至少要为None（同时secure=true），不允许Lax
- 但是在直接用axios不用ant design pro后，却不需要这个，？？？无厘头。。。。





# Session
+ 服务端一般是不保存Cookie的，除非这个Cookie是Session
    - 对外暴露SessionId，在服务端保存SessionId对应的Session
+ 在Tomcat中
    - org.apache.catalina.Manager专门负责管理Session
        * maxActiveSessions：默认-1即不允许多Session
    - org.apache.catalina.SessionIdGenerator
        * 16进制，一般16B，使用SecureRandom
    - Session转化Cookie：`org.apache.catalina.core.ApplicationSessionCookieConfig#createSessionCookie`
        * 默认name=JSESSIONID，value=sessionId
        * maxAge、comment：SessionCookieConfig配置的，默认-1，Null
        * domain、secure、httpOnly：SessionCookieConfig配置的或者Context配置
        * path：contextPath（以/结尾）
    - 设置SessionCookie`org.apache.catalina.connector.Response#addSessionCookieInternal`
        * 确保当前Header中的Set-Cookie仅有一个JSESSIONID，有则替换，无则设置
    - 从请求中创建Session	
        * 在创建请求时，就会探测session，且`org.apache.catalina.connector.Request#setRequestedSessionId`
        * Session的有效性：惰性删除，即在访问时校验

## 属性
+ id
+ createTime
+ lastAccessedTime
+ maxInactiveInterval：单位sec，默认30mins
+ session attribute：key-value
    - 注意：不是上面几个



