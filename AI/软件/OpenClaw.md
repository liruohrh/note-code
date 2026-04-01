- `openclaw dashboard` 打开Web UI
- `openclaw gateway`  动gateway
- `openclaw gateway start` 后台启动gateway、启动任务计划程序（windows）
	- 执行`.openclaw/gateway.cmd`
- 配置文件 `.openclaw/openclaw.json`


# 问题

## “HTTP 401: Authentication Fails, Your api key: *** is invalid”
- 解决方法：删除`.openclaw\agents\main\agent\auth-profiles.json`
- 从解决401来看，OpenClaw目前在配置修改功能上有很大问题，提供多种配置方式，同时又将配置拆分到不同持久化位置，且同步机制没有做好
- openclaw.json中也包含了auth.profiles，不知道是不是同一个东西，删除后重新运行gateway没有再创建这个auth-profiles.json