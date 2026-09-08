# EvalError 报错


```
EvalError: Refused to evaluate a string as JavaScript because 'unsafe-eval'
or 'trusted-types-eval' is not an allowed source of script in the following
Content Security Policy directive:
"script-src 'self' 'strict-dynamic' 'report-sample' 'nonce-zSIFzzJqfiBI9R-mX7l0q7GG'"
```

## 一句话结论

页面的 CSP 白名单里**没有 `'unsafe-eval'`**，所以任何「把字符串当代码执行」的操作都被浏览器拦掉。
用 Playwright 的 `WaitForFunction` 撞上它是必然的 —— 它需要在页面主 world 里把你传的表达式
字符串编译成函数才能轮询，那一步走的就是 `eval`。

## 一、策略逐项拆解

```
script-src 'self' 'strict-dynamic' 'report-sample' 'nonce-zSIFzzJqfiBI9R-mX7l0q7GG'
```

| 值 | 作用 |
|---|---|
| `'self'` | 同源脚本。**一旦有 `'strict-dynamic'` 它就被忽略了**，留着纯粹是给不支持 strict-dynamic 的老浏览器兜底 |
| `'nonce-xxx'` | 只有 `<script nonce="xxx">` 能执行。nonce **必须每个响应重新随机生成**，写死等于没设 |
| `'strict-dynamic'` | 已被信任的脚本（带对 nonce 的）用 `document.createElement('script')` 动态加载的子脚本自动继承信任，于是不用再维护一长串域名白名单 |
| `'report-sample'` | 违规上报时附带被拦代码的前 40 个字符，方便定位是哪一行 |

真正决定「拦什么」的是**没写出来的两项**：

| 缺失的值 | 后果 |
|---|---|
| 没有 `'unsafe-eval'` | `eval()`、`new Function()`、`setTimeout("字符串")`、`setInterval("字符串")` 全部抛 `EvalError` |
| 没有 `'unsafe-inline'` | 不带 nonce 的内联 `<script>`、以及 `onclick=` 这类事件属性全部不执行 |

常见的连带受害者：Vue 的 runtime-compiler 版本、部分模板引擎、老的 JSON polyfill、某些 WASM 加载路径。

## 二、Playwright 侧：为什么 `WaitForFunction` 会中招

`Evaluate` 和 `WaitForFunction` 走的不是一条路：

| API | 机制 | 受 CSP 影响 |
|---|---|---|
| `page.Evaluate()` | 表达式交给调试协议一次性执行，不碰 `eval` | 否 |
| `page.WaitForFunction()` | 在页面主 world 装一个轮询器，需要先把字符串**编译成函数** | **是** |
| `page.WaitForURL()` | 纯 Go/Node 侧实现，监听 frame 导航事件，不注入任何 JS | 否 |
| `page.URL()` | 读的是缓存的 frame URL | 否 |

所以下面这种写法在严格 CSP 站点上必然报 `EvalError`：

```go
page.WaitForFunction(fmt.Sprintf(`() => window.location.href === %q`, communityUrl))
```

### 改法，按推荐顺序

**1. 换 `WaitForURL`（最干净）**

```go
// 精确字符串 —— 注意是 glob，* ? [ ] 会被当通配符
err := page.WaitForURL(communityUrl)

// URL 里含特殊字符时用正则
err := page.WaitForURL(regexp.MustCompile(`^` + regexp.QuoteMeta(communityUrl) + `$`))

// 带超时
err := page.WaitForURL(communityUrl, playwright.PageWaitForURLOptions{
    Timeout:   playwright.Float(15000),
    WaitUntil: playwright.WaitUntilStateDomcontentloaded,
})
```

第二个参数接受 `string`（glob）、`*regexp.Regexp`、`func(string) bool` 三种形式。

**2. 建 context 时关掉 CSP**

只能在创建时设，之后改不了：

```go
context, err := browser.NewContext(playwright.BrowserNewContextOptions{
    BypassCSP: playwright.Bool(true),
})

// 持久化 profile
context, err := pw.WebKit.LaunchPersistentContext(userDataDir,
    playwright.BrowserTypeLaunchPersistentContextOptions{
        BypassCSP: playwright.Bool(true),
    })
```

⚠ 如果是 `ConnectOverCDP` / `Connect` 连到已经跑起来的浏览器再复用 `browser.Contexts()[0]`，
那个 context 已经建好了，`BypassCSP` **设不上** —— 只能 `browser.NewContext(...)` 新建，或走第 1 种。

⚠ 关掉 CSP 会让页面行为偏离真实环境，调试可以，跑真实场景要谨慎。

**3. 轮询逻辑挪到 Go 侧自己写**

```go
for i := 0; i < 30; i++ {
    if page.URL() == communityUrl { break }
    page.WaitForTimeout(200)
}
```

## 三、给自己的页面配这套策略

核心要求：**每次请求生成新 nonce**，同时塞进响应头和模板。

### Go（net/http）

```go
package main

import (
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"html/template"
	"net/http"
)

var tpl = template.Must(template.New("page").Parse(`<!DOCTYPE html>
<html>
<head><title>demo</title></head>
<body>
  <h1>hello</h1>
  <script nonce="{{.Nonce}}">
    console.log("这段能跑，因为带了 nonce");
    try { eval("1+1") } catch (e) { console.error(e.message) }  // 被 CSP 拦
  </script>
  <script>console.log("这段跑不了，没有 nonce")</script>
</body>
</html>`))

func newNonce() string {
	b := make([]byte, 16)
	rand.Read(b)
	return base64.RawURLEncoding.EncodeToString(b) // 形如 zSIFzzJqfiBI9R-mX7l0q7GG
}

func handler(w http.ResponseWriter, r *http.Request) {
	nonce := newNonce()

	w.Header().Set("Content-Security-Policy", fmt.Sprintf(
		"script-src 'self' 'strict-dynamic' 'report-sample' 'nonce-%s'; "+
			"object-src 'none'; "+
			"base-uri 'none'; "+
			"report-uri /csp-report",
		nonce))

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	tpl.Execute(w, map[string]string{"Nonce": nonce})
}

func report(w http.ResponseWriter, r *http.Request) {
	buf := make([]byte, 4096)
	n, _ := r.Body.Read(buf)
	fmt.Printf("CSP violation: %s\n", buf[:n])
}

func main() {
	http.HandleFunc("/", handler)
	http.HandleFunc("/csp-report", report)
	http.ListenAndServe(":8080", nil)
}
```

打开 `http://localhost:8080`，控制台里就是文章开头那条 `EvalError`。

`object-src 'none'` 和 `base-uri 'none'` 是配 nonce 方案时的标配：前者堵掉 `<object>`/`<embed>` 这条
绕过路径，后者防止注入 `<base href>` 把相对路径脚本劫持到别的域。

### meta 标签（只适合本地快速试）

必须放在 `<head>` 里、任何脚本之前：

```html
<meta http-equiv="Content-Security-Policy"
      content="script-src 'self' 'strict-dynamic' 'report-sample' 'nonce-testnonce123'">
```

局限：**不支持 `report-uri` / `report-to`**，且 nonce 写死在静态 HTML 里等于公开。

### Nginx

```nginx
add_header Content-Security-Policy "script-src 'self' 'strict-dynamic' 'report-sample' 'nonce-$request_id'; object-src 'none'; base-uri 'none'" always;
```

`$request_id` 是内置的 32 位随机十六进制串，每请求唯一，可以当 nonce。
但这**只对静态页有意义** —— 动态页得让后端把同一个 nonce 写进 `<script>` 标签，
Nginx 和后端各生成各的对不上。

## 四、上线前

先用 `Content-Security-Policy-Report-Only` 头跑一段时间，只上报不拦截，把站点里所有违规点收集齐
再切强制模式。否则严格 CSP 一上，内联脚本、`eval`、第三方 SDK 大概率挂一片。

```go
w.Header().Set("Content-Security-Policy-Report-Only", policy)
```

两个头可以同时下发：强制头挂一套已验证的宽松策略，Report-Only 头挂待收敛的严格策略。


