- 事件：sender
- 发布事件：
	- `Signal#send`：就是直接遍历receiver，返回`[(receiver, receiver(signal=self, sender=sender, **named))]`，不捕获异常
	- `Signal#send_robust`：捕获每个receiver的异常，元组元素1是异常或者receiver的返回值
- 监听事件：`@receiver`
- 注意，推荐单独写在signals、receivers模块，如果receiver不在django指定的模块中，需要额外导入，推荐在app的ready方法中导入


# 内置Signal
- https://docs.djangoproject.com/en/5.1/ref/signals/