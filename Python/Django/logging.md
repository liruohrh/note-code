- django.utils.log模块（直接使用logging模块）
- 内置日志模块：logging、longging.conf

- 配置方式
	- fileConfig：ini文件，且无法设置filter
	- dictConfig：dict对象，最新API

- 配置
	- [dict schema](https://docs.python.org/3/library/logging.config.html#dictionary-schema-details)
	- [自定义对象](https://docs.python.org/3/library/logging.config.html#user-defined-objects)
- 禁用日志方式
	- 手段设置logger对象的disable=True
		- 可以导入对象，或者直接获取logging.getLogger
	- Filtter返回False
	- 因为要禁用，因此不推荐在handler处理
		- 因为处理方式是`logger.log > handler > filter > format > handler do output`


# 组件
## LogRecord：日志数据
- 需要用什么变量，直接看这个类的属性，在formatter中直接用

## filter：日志过滤器
```python
 
 "filters": {  
     "require_debug_false": {  
         "()": "django.utils.log.RequireDebugFalse",  
     },  
     "require_debug_true": {  
         "()": "django.utils.log.RequireDebugTrue",  
     },  
 }  
 class RequireDebugFalse(logging.Filter):  
     def filter(self, record):  
         return not settings.DEBUG  
 class RequireDebugFalse(logging.Filter):  
     def filter(self, record):  
         return settings.DEBUG
```
## formatter：日志格式化
- style：%（`%(xxx)格式化字符串---如d`）、{（占位符`{xxx}`）、$（string.Template，` ${xxx} `）
```python
 "formatters": {  
     "django.server": {  
         "()": "django.utils.log.ServerFormatter",  
         "format": "[{server_time}] {message}",  
         "style": "{",  
     }  
 }  
 class ServerFormatter(logging.Formatter):  
     #self._fmt 对应 format  
     #self.datefmt 对应 datefmt  
     def format(self, record):  
         record.server_time=  
         record.message=  
         ...
```

## handler：日志输出器
```python
 "handlers": {  
     "console": {  
         "level": "INFO",  
         "filters": ["require_debug_true"],  
         "class": "logging.StreamHandler",  
     },  
     "django.server": {  
         "level": "INFO",  
         "class": "logging.StreamHandler",  
         "formatter": "django.server",  
     },  
     #500 都会发生到
     "mail_admins": {  
         "level": "ERROR",  
         "filters": ["require_debug_false"],  
         "class": "django.utils.log.AdminEmailHandler",  
     },  
 }

class AdminEmailHandler(logging.Handler):
	def emit(self, record):
```
- logging.StreamHandler默认`sys.stderr`

## logger: 日志对象
- 继承机制：点分制，如同Java，`father.son`
- propagate：True时会把消息传递给父Logger
	- 推荐设置为False
- exc_info：默认sys.exc_info(此时设置为True即可)，也可以是BaseException
- error方法还只是日志，exception方法默认设置了exc_info=True
- 使用threading.RLock()进行加锁emit即输出
	- `_log > handler.handler > handler.filter > handler.emit > formatter.format > output`
```python
"loggers": {
	"django": {
		"handlers": ["console", "mail_admins"],
		"level": "INFO",
	},
	"django.server": {
		"handlers": ["django.server"],
		"level": "INFO",
		"propagate": False,
	},
}

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 所有等级都会输出
```

### Django
- `django.request`：`django.utils.log.request_logger`
	- 相对底层的http的错误：如：
		- `django.core.handlers.base.BaseHandler.get_response`：获取response后，当响应码至少是400时，使用`logging.log_response`
			- 如：`Not Found: /a/b`
- `django.db.backends`：`django.db.backends.utils.logger`
	- sql日志
	- debug输出`(%.3f) %s; args=%s; alias=%s`
		- duration执行时间、sql、sql参数args、数据库alias

- `django.server`：`django.core.servers.basehttp.logger` 
	- 请求日志
	- 5xx=error、4xx=warning、other=info
	- `msg='"%s" %s %s'`：requestline、resp_status、body_size
 ```
 http.server.BaseHttpRequestHandler.log_request 
 > django.core.servers.basehttp.WSGIRequestHandler.log_message
 > django.server 
 ``` 


# 最后的手段--即无handler可用
```
_defaultLastResort = _StderrHandler(WARNING)
lastResort = _defaultLastResort
```