
# 索引的问题
- 动态元素索引变化比较频繁，会导致索引一会1一会10的，但是这种情况相对比较少

- 提示词
	- 不同browsercli
		- 用browser-use完成 https://www.csdn.net/ 的登录，等你了解到登录需要输入什么再和我要这些，账号密码 > 邮箱验证码 > 手机验证码，你应该先激活虚拟环境，然后就可以执行browser-use命令了。
		- 用playwright-cli完成 https://www.csdn.net/ 的登录，等你了解到登录需要输入什么再和我要这些，账号密码 > 邮箱验证码 > 手机验证码。
		- 用agent-browser完成 https://www.csdn.net/ 的登录，等你了解到登录需要输入什么再和我要这些，账号密码 > 邮箱验证码 > 手机验证码。
	- 要注意icon语义化（通常都是类名中包含icon信息，即语义化信息），如果有很多同级元素如i、span、图片，然后前面一点或者后面一点有提到某些东西如“其他登录选项”（通常只是文本提示），那么这些元素大概率就是这些item，此时可以尝试获取父级html，分析html（非文本匹配，而是className、id匹配），即便没有很多相同元素，如果提到某些东西如“其他登录选项”（通常只是文本提示）且在其附近文本中没有，则应该也尝试获取父级html，进行分析。
	- 结果
		- 都可以发现图标登录选项
			- agent-browser不行
			- TODO：强调“其他登录选项”只是提示，不可交互，寻找周围元素的id、className
		- 效率待分析


# 存在清洗过头，但可用其他方式弥补，如icon代替文本语义

- icon代替文本语义
	- playwright-cli、agent-browser、browser-use都不太行，尽管browser-use还保留了一些html标签，但是没有文本，AI不会自动去判断此处是否有可能是登录方法，而是直接放弃判断
		- 因此相比browser-usetoken用得更多，agent-browser完全不保留 id，可能playwright-cli才是最好的选择
	- 解决方法
		- 保留id
		- i、svg保留class
		- image（title、alt基本都会保留的），大都不需要，最多就是保留url最后一段
		- span等其他
			- 按类名匹配过滤
			- 给AI这样的示例，提示要其父节点的html
				- 比如 `要注意icon语义化（通常都是类名中包含icon信息，即语义化信息），如果有很多同级元素如i、span、图片，然后前面一点或者后面一点有提到某些东西如其他登录选项，那么这些元素大概率就是这些item，此时可以尝试获取父级html，分析html`
			- 保留常见icon的类名
## playwright-cli
- 基本上就保留了AccessibilityTree，基本上都是整个页面
- 某些情况下还会保留元素id

### 1. span icon（csdnlogin）
- https://www.csdn.net/  ， 点击登录后
- 登录方式是icon而不是文本：`<span data-v-7e28454b="" class="login-third-item login-third-qq"></span>`
- ”其他登录方式“和“微信登录”、“验证码登录”等同时出现
	- “微信登录”、“验证码登录”等可能会被认为就是“其他登录方式"，因为“其他登录方式"可能是以css的方式显示在上方

```yaml
- generic [ref=e60]:
- text: 终于等到你～
- img [ref=e61]
- generic [ref=e62]:
- generic [ref=e63]:
  - generic [ref=e64]: 登录可享更多权益
  - generic [ref=e65]: 将博客内容转为可运行代码 提升学习效率
- generic [ref=e66]:
  - generic [ref=e68]:
	- generic [ref=e69] [cursor=pointer]: 微信登录
	- generic [ref=e70] [cursor=pointer]: 验证码登录
	- generic [ref=e71] [cursor=pointer]: APP登录
  - generic [ref=e73]:
	- generic [ref=e74]:
	  - img
	- generic [ref=e75]: 打开微信扫一扫，快速登录/注册
- paragraph [ref=e78]: 其他登录方式
```

```html
<div data-v-92f0ae06="" class="login-box-bottom">
<div data-v-7e28454b="" data-v-92f0ae06="" class="login-third">
<p data-v-7e28454b="">其他登录方式</p> 
<div data-v-7e28454b="" id="thirdLogin" class="login-third-items">
<span data-v-7e28454b="" id="last-login2" class="last-login-way" style="display: none;">上次登录</span> 
<span data-v-7e28454b="" class="login-third-item login-third-passwd login-third-first-item"></span>
 <!----> 
<span data-v-7e28454b="" class="login-third-item login-third-qq"></span> 
<span data-v-7e28454b="" class="login-third-item login-third-weibo"></span> <span data-v-7e28454b="" class="login-third-item login-third-baidu"></span> <span data-v-7e28454b="" class="login-third-item login-third-github"></span> <span data-v-7e28454b="" class="login-third-item login-third-huawei"></span> <span data-v-7e28454b="" class="login-third-item login-third-hbuilder"></span> 
<span data-v-7e28454b="" class="login-third-item login-third-google"></span> <span data-v-7e28454b="" id="tip_box" class="medal-hover-tips">关联账号领取专属勋章</span>
</div>
</div> <!----></div>
```



### 2. svg/img icon（juejinlogin）
- https://juejin.cn/  ， 点击登录后
- 这一个倒是因为img没有清洗掉（注意这个img只是图片的意思，不是img标签）

```yaml
- generic [ref=e839]:
  - generic [ref=e840]:
	- generic [ref=e841]: 其它登录：
	- generic [ref=e842]:
	  - img [ref=e844]
	  - img "微信" [ref=e852] [cursor=pointer]
	  - img "icon_GitHub" [ref=e854]
  - generic [ref=e860] [cursor=pointer]: 密码登录
```

```html
<div data-v-79737cbc="" class="other-login-box">
<div data-v-79737cbc="" class="oauth-box">
<span data-v-79737cbc="">其它登录：</span> 
<div data-v-79737cbc="" class="oauth">
<div data-v-79737cbc="" class="oauth-bg">
<svg data-v-79737cbc="" width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" class="weibo-icon">...</svg>
</div> 
<div data-v-79737cbc="" class="oauth-bg">
<img data-v-79737cbc="" title="微信" alt="微信" src="//lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/e0ff12435b30910520c9a3aac9b90487.svg" class="oauth-btn"></div>
 <div data-v-79737cbc="" class="oauth-bg">
 <svg data-v-79737cbc="" width="46px" height="46px" viewBox="0 0 46 46" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="github-icon">...</svg></div>
</div>
</div> 
<span data-v-79737cbc="" class="clickable">

              密码登录

            </span> <!----></div>
```


## agent-browser
- 基本上就保留了AccessibilityTree，基本上都是整个页面

- csdnlogin
```yaml
- generic
  - generic
    - Iframe [ref=e2]
      - generic
        - generic
          - StaticText "终于等到你～ "
          - image
        - generic
          - generic
            - StaticText "登录可享更多权益"
            - StaticText "将博客内容转为可运行代码"
            - StaticText " "
            - StaticText "提升学习效率"
          - generic
            - StaticText "微信登录"
            - StaticText "验证码登录"
            - StaticText "APP登录"
          - generic
            - image
            - image
            - StaticText "打开微信扫一扫，快速登录/注册"
          - paragraph
            - StaticText "其他登录方式"
          - generic
    - image
```


- juejinlogin
```yaml
- StaticText "其它登录："
- image
- image "微信" [ref=e6] clickable [cursor:pointer]
- image "icon_GitHub"
- generic [ref=e7] clickable [cursor:pointer]
- StaticText "密码登录"
```
## browser-use
- 其清洗的内容相对少，因此清洗后内容比较多，且如果页面太多，需要滑动才能获取页面的更多内容
	- 保留了比较完整的HTML

- csdnlogin
```html
|scroll element[369]<iframe name=passport_iframe /> (scroll)
	终于等到你～
	登录可享更多权益
	将博客内容转为可运行代码
	提升学习效率
	[3802]<span />
		微信登录
	[3808]<span />
		验证码登录
	[3811]<span />
		APP登录
	打开微信扫一扫，快速登录/注册
	其他登录方式
	[230]<span />
	[231]<span />
	[232]<span />
	[233]<span />
	[234]<span />
	[235]<span />
	[236]<span />
	[237]<span />
```

- juejinlogin
```html
其它登录：
[852]<div />
	[4368]<svg /> <!-- SVG content collapsed -->
[4376]<div />
	[147]<img title=微信 alt=微信 />
[853]<div />
	[4378]<svg /> <!-- SVG content collapsed -->
[854]<span />
	密码登录
```