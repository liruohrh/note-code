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
# 常见配置需求

# Channel
- 模型的处理速度会很大程度上影响回复速度，比如`nvidia/deepseek-ai/deepseek-v3.2`，几分钟后才回复

# Model
- 需要配置models（模型配置）、agents（智能体配置，比如聊天界面、默认智能体）
	- model引用格式：`{provider}/{modelId}`，如`nvidia/deepseek-ai/deepseek-v3.2`
	- models配置会被缓存到`.openclaw\agents\main\agent\models.json`（有时候没有正确同步，比如删除无用的）
- cost：token美元计费，免费推荐都设置为0（仅显示token消耗）
```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "deepseek": {
        "baseUrl": "https://api.deepseek.com",
        "apiKey": "sk-xxxxxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "deepseek-chat",
            "name": "DeepSeek Chat",
            "api": "openai-completions",
            "reasoning": false,
            "input": ["text"],
            "cost": {
              "input": 0.28,
              "output": 0.42,
              "cacheRead": 0.028,
              "cacheWrite": 0
            },
            "contextWindow": 131072,
            "maxTokens": 8192,
            "compat": {
              "supportsUsageInStreaming": true
            }
          },
          {
            "id": "deepseek-reasoner",
            "name": "DeepSeek Reasoner",
            "api": "openai-completions",
            "reasoning": true,
            "input": ["text"],
            "cost": {
              "input": 0.28,
              "output": 0.42,
              "cacheRead": 0.028,
              "cacheWrite": 0
            },
            "contextWindow": 131072,
            "maxTokens": 65536,
            "compat": {
              "supportsUsageInStreaming": true
            }
          }
        ]
      },
      "nvidia": {
        "baseUrl": "https://integrate.api.nvidia.com/v1",
        "apiKey": "nvapi-xxxxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "deepseek-ai/deepseek-v3.2",
            "name": "Nvidia Deepseek-v3.2",
            "api": "openai-completions",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 131072,
            "maxTokens": 4096,
            "compat": {
              "supportsUsageInStreaming": true
            }
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "nvidia/deepseek-ai/deepseek-v3.2"
      },
      "models": {
        "deepseek/deepseek-chat": {
          "alias": "DeepSeek"
        },
        "deepseek/deepseek-reasoner": {
          "alias": "DeepSeek Reasoner"
        },
        "nvidia/deepseek-ai/deepseek-v3.2": {
          "alias": "Nvidia Deepseek-v3.2"
        }
      },
      "workspace": "F:\\data\\.openclaw\\workspace",
      "compaction": {
        "mode": "safeguard"
      }
    }
  }
}

```

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
      "autoGenerate": true, 
      "caPath": "F:\\data\\.openclaw\\openclaw.ca.crt",
      "certPath": "F:\\data\\.openclaw\\openclaw.crt",
      "keyPath": "F:\\data\\.openclaw\\openclaw.key"
    }
  }
}
```

- autoGenerate：自动生成
	- 或者用`https://github.com/FiloSottile/mkcert`，生成+自动安装根证书
	- 需要安装openssl
	- 默认生成路径为`gateway\tls`，注意，不会生成caPath
- 如果想不显示证书不可信或者用TUI：安装caPath
	- TUI的nodejs会进行校验，如果不安装，需要设置环境变量`NODE_TLS_REJECT_UNAUTHORIZED=0`
# 问题

## “HTTP 401: Authentication Fails, Your api key: *** is invalid”
- 解决方法：删除`.openclaw\agents\main\agent\auth-profiles.json`
- 从解决401来看，OpenClaw目前在配置修改功能上有很大问题，提供多种配置方式，同时又将配置拆分到不同持久化位置，且同步机制没有做好
- openclaw.json中也包含了auth.profiles，不知道是不是同一个东西，删除后重新运行gateway没有再创建这个auth-profiles.json
- `.openclaw\agents\main\agent\models.json` 也有
- 好像是初始化程序+配置优先级问题，最好删了，只用 openclaw.json
- 优先级：
	- `agents/main/agent/models.json`
	- `agents/main/agent/auth-profiles.json`
	- `openclaw.json``