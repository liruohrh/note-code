# server
- 也叫 virtual server，nginx可以配置N个virtual server
	- 不同virtual server可以监听同一个port
	- 根据Host请求头匹配，匹配失败看[listen](#listen) 
- server有一个默认的`root html; index index.html`
# listen
- `listen ip:port [default_server]`
- 默认第一个server是默认server，也可以显示设置
	- 但如果有设置ip，则默认是第一个相同ip的server
# server_name
- `server_name name...`
- 可以有多个server_name，是根据Host请求头匹配的
	- 如果无header=Host，则处理无Host请求头的请求
	- 如果是空Host，则仍然是默认server处理请求
- name语法：`*.xxx.top`通配符、`.xxx.top`泛子域名、正则表达式
	- [详细](https://nginx.org/en/docs/http/ngx_http_core_module.html#server_name)

## 无Host处理
- https://nginx.org/en/docs/http/request_processing.html
	- 有提到server_name为空就处理无Host请求，但是在1.18.0测试，无法自己处理，只能用nginx的默认响应400处理（可以在该server的日志中看见请求）
- 以下是折中方案，也可以反向代理到服务器，反正就是错误响应码处理
```nginx
server {
    listen 80;
    server_name "";
    root vhosts/server3.nginx.top;
    index index.html;
    access_log logs/server3.nginx.top_access.log combined;
    error_log logs/server3.nginx.top_error.log info;
    error_page 400 = @no_host;
    location @no_host {
        try_files /index.html =404;
    }
}
```

# root
- `root path`
- path：默认html
	- 绝对、相对（nginx目录）
	- 可以是变量，除了`$document_root` and `$realpath_root`
- 设置根目录，即`/`
	- 寻找文件时会拼接这个根目录
# alias
- `alias path`
- 匹配路径的别名，是文件路径直接替换为该alias，而不是拼接

# index
- 指定访问目录响应的文件
- 默认：`index index.html`


# default_type
- 默认的content-type，即给types指令中映射失败的请求响应content-type（比如无扩展名）
- nginx提供一个默认的mime-type配置，在`conf/mime.types`且默认被`nginx.conf`include
# types
- mime-type关联文件扩展名
```
types{
	text/html html htm shtml;
}
```

# try_files
- `try_files file ... uri;    try_files file ... =code;`
- 按顺序查看文件是否存在，存在则响应，不存在则响应uri或者code。
- 注意，如果`$uri`是文件URL，而不是目录URL，在尝试`$uri/`时仍然会进行重定向而不是响应`$uri/index.html`
	- 因此，如果不想被重定向，就自己加上`$uri/index.html`而不是`$uri/`
	- 如果想所有请求都这样，则给每个root配置
		- 但是要注意，这是优先级最低的
			- 可以删除原来的
			- 也可以给原来的配置这样的配置（不过都这样了，不如直接以/结尾呢）
```
location / {
    root htmls;
    try_files $uri $uri/index.html =404;
}
```


# error_page
- `error_page code... [=[response]] uri;`
- response：响应码
- uri：错误页

- 更高效处理error_page
```nginx
error_page 404 400 = @fallback;
location @fallback {
    proxy_pass http://backend;
}
```
# location

```nginx
location [ = | ~ | ~* | ^~ ] _uri_ { ... }  
location @_name_ { ... }
```
- 按定义顺序匹配，匹配到一个后就停止，除非里面的指令让他进行重定向之类的
- 操作符（按顺序）
	- `=`：精确匹配，一旦找到就停止匹配
	- `^~`：前缀匹配
	- `~`：正则表达式，忽视大小写
	- `~*`：正则表达式，忽视大小写
	- 无：最长前缀匹配
	- /：默认匹配
- URI 
- `location @xxx {} `：定义一个URI，可以让其他配置重定向到此URI，如[error_page](#error_page)
## trailing slash
- nginx严格遵循HTTP URL语义，a是文件而a/是目录
	- 但为了权衡，当请求a，文件不存在则会自动重定向到a/（无法配置禁用开启）
	- 为了可以在访问a时a不存在尝试当作目录访问即访问a/index.html，参考[try_files](#try_files)
- 当访问目录时，会获取index文件，没有就会响应404
## slash
- 如果是一些xxx_pass配置，则会在没有slash时重定向到slash，除非自己配置了带slash的