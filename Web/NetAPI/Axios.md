#web/js/httpclient 

# 配置
- [默认配置 | Axios中文文档 | Axios中文网](https://www.axios-http.cn/docs/config_defaults#%E9%85%8D%E7%BD%AE%E7%9A%84%E4%BC%98%E5%85%88%E7%BA%A7)
- `axios < axios.create() < request`

# interceptor
- 拦截器只是一个Promise
	- 如果有传递错误处理参数，则错误将被吞噬，下一个Promise会执行then，除非在错误处理中抛出异常
	- 对于下一个Promise
		- 参数理所当然的是成功处理或者错误处理的返回值
		- 捕获的是成功处理或者错误处理抛出的异常
	- 成功处理抛出的异常，当然是下一个Promise的catch处理
- 拦截器允许修改请求、响应的任何属性

# 错误
- 客户端在请求时就发生错误，error.response、error.message是空，可以使用code（什么错误），stack（堆栈）属性
- 请求超时：error.response是空，推荐用error.message
- 



# BUG
## Client network socket  disconnected before secure TLS connection was established

- [服务器配置问题](https://stackoverflow.com/questions/67579933/https-post-via-axios-throwing-error-client-network-socket-disconnected-eproto)
- [服务器平台配置变更导致](https://www.workerman.net/q/9255)
- [别人的情况，以及讨论，好像是服务器的问题](https://community.fly.io/t/error-client-network-socket-disconnected-before-secure-tls-connection-was-established/3911/7)
- [客户端TLS版本太旧](https://stackoverflow.com/questions/61402539/node-js-client-network-socket-disconnected-before-secure-tls-connection-was-es)
- [换成非Axios也会出现这种问题](https://stackoom.com/question/3mjsK)