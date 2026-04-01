- `openclaw dashboard` 打开Web UI
- `openclaw gateway`  动gateway
- `openclaw gateway start` 后台启动gateway、启动任务计划程序（windows）
	- 执行`.openclaw/gateway.cmd`
- 配置文件 `.openclaw/openclaw.json`
	- [配置参考](https://docs.openclaw.ai/gateway/configuration-reference)
- 环境变量
	- `OPENCLAW_HOEM`：默认 `$HOME`，仅限于用在`~/.openclaw/, agent dirs, sessions, credentials`
		- 基本设置了这个，`~/.openclaw/` 仍然会被openclaw的某些功能使用，而且很多外部代码（插件）可能更加不会遵循，比如QQ机器人
	- `OPENCLAW_STATE_DIR`：默认`~/.openclaw`
		- 如果设置了OPENCLAW_HOEM，最好设置OPENCLAW_STATE_DIR，因为openclaw有时候不遵循OPENCLAW_HOEM，比如gateway服务的脚本路径 `~/.openclaw/gateway.cmd`
	- `OPENCLAW_CONFIG_PATH`：配置文件`~/.openclaw/openclaw.json`，遵循OPENCLAW_HOEM
- WebUI：`http://127.0.0.1:{gateway.port:18789}/#token={token}`
## 常见配置需求

## 仅本机
```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "xxxxxxxxxxxxx"
    }
  }
}
```

## 局域网
```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "lan",
    "controlUi": {
      "allowedOrigins": ["https://192.168.0.106:18789"],
      // 禁用设备认证（否则需要一个一个openclaw devices approve --latest）
      "dangerouslyDisableDeviceAuth": true
    },
    "auth": {
      "mode": "token",
      "token": "xxxxxxxxxxxxx"
    },
    "tls": {
      "enabled": true,
      "certPath": "F:\\data\\.openclaw\\openclaw.pem",
      "keyPath": "F:\\data\\.openclaw\\openclaw.key.pem"
    }
  }
}
```


# 问题

## “HTTP 401: Authentication Fails, Your api key: *** is invalid”
- 解决方法：删除`.openclaw\agents\main\agent\auth-profiles.json`
- 从解决401来看，OpenClaw目前在配置修改功能上有很大问题，提供多种配置方式，同时又将配置拆分到不同持久化位置，且同步机制没有做好
- openclaw.json中也包含了auth.profiles，不知道是不是同一个东西，删除后重新运行gateway没有再创建这个auth-profiles.json