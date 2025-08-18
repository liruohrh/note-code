- 实现
	- 在一个模块注册模块函数（默认导出）
		- 或者可以用使用ReactContext启动startService一个Intent Service
	- 在原生注册service一个自定义的HeadlessJsTaskService
- 要注意的是stopService并不会终止HeadlessJsTaskService的执行

# 不错的例子
- https://github.com/Rapsssito/react-native-background-actions
	- 只是要注意多次start时，因为`startForeground(SERVICE_NOTIFICATION_ID, notification)`（将Background Service提升为Foreground Service以避免被Android随意杀死且允许通知）导致第一个任务执行完释放了通知，后续start的任务就无法进行通知了，除非在第一个start执行完后有新任务进行start