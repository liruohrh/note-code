
- https://nginx.org/en/docs/http/ngx_http_rewrite_module.html
- ```rewrite _regex_ _replacement_ [_flag]_;```
- regex：
- replacement：
	- 尾部添加`?`表示把原URI的queryString带上
	- 如果是`http://, https://, $scheme`，则会停止且重定向
	- 这个就是重写后的路径，而不是说只是替换原来的
		- 比如 regex=a，路径=/a/b，replacement=c，结果是c，而不是/c/b
- flag
	- last：重写成功后，重新匹配location
	- break：重写成功后，不会重新匹配location，而是进行其他处理然后响应
	- redirect：直接重定向302
	- permant：直接重定向301
- 通常，这个会写在server context中
	- 如果在location中，则最大重写次数是10，超过就500（如果写在location中，regex不就和location的URI差不多嘛，就不太好）
	- 都可以写多个rewrite


# 例子
## demo

```
#location /rewrite1
#rewrite ^/rewrite1(/.*)$ /rewrite11$1 break;

2024/12/28 17:34:28 [notice] 33616#31600: *10 "^/rewrite1(/.*)$" matches "/rewrite1/", client: 127.0.0.1, server: , request: "GET /rewrite1/ HTTP/1.1", host: "localhost"

2024/12/28 17:34:28 [notice] 33616#31600: *10 rewritten data: "/rewrite11/", args: "", client: 127.0.0.1, server: , request: "GET /rewrite1/ HTTP/1.1", host: "localhost"

2024/12/28 17:34:28 [notice] 33616#31600: *10 "^/rewrite1(/.*)$" does not match "/rewrite11/index.html", client: 127.0.0.1, server: , request: "GET /rewrite1/ HTTP/1.1", host: "localhost"





#location /rewrite1
#rewrite ^/rewrite1(.*)$ /rewritedir1$1 break;

2024/12/28 17:31:30 [notice] 33872#18652: *9 "^/rewrite1(.*)$" matches "/rewrite1/", client: 127.0.0.1, server: , request: "GET /rewrite1/ HTTP/1.1", host: "localhost"

2024/12/28 17:31:30 [notice] 33872#18652: *9 rewritten data: "/rewritedir1/", args: "", client: 127.0.0.1, server: , request: "GET /rewrite1/ HTTP/1.1", host: "localhost"
```