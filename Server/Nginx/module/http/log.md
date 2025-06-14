- https://nginx.org/en/docs/http/ngx_http_log_module.html
- 就近原则：location的不会使用http的
- 目录必须手动创建
# access_log
- 开启：`access_log path [format [buffer=size] [gzip[=level]] [flush=time] [if=condition]];`
- 关闭：`access_log off;`
- 默认：`access_log logs/access.log combined;`

# error_log
- `error_log file [level];`
- 默认：`error_log logs/error.log error;`
- level：`debug`, `info`, `notice`, `warn`, `error`, `crit`, `alert`, or `emerg`.
	- debug需要以debug配置编译nginx
		- https://nginx.org/en/docs/debugging_log.html