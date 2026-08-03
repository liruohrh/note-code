# TUI
- 默认footer：token相关显示有`↑` input, `↓` output, `R` cache read, `W` cache write, `CH` latest cache hit rate), cost, context usage

# 插件
```bash
printf "%s\n" npm:@heyhuynhgiabuu/pi-search npm:pi-subagents npm:gentle-engram npm:context-mode npm:pi-token-usage npm:pi-token-burden npm:pi-mcp-adapter | xargs -n1 pi install

# powershell
"" -split " " | Foreach-Object { pi install $_  }
```

- pi-token-usage：可以显示项目、项目今日、今日
- pi-token-burden：查看token花费的分布
- gentle-engram：需要额外安装[engram](https://github.com/Gentleman-Programming/engram/releases)
	- 本地sqlite+支持云端存储+mcp、cli
		- 初始化： `engram setup pi` （注意会覆盖mcp配置）
	- 或者pi-mem markdown

```jsonc
{
  "mcpServers": {
    "anysearch": {
      "url": "https://api.anysearch.com/mcp",
      "lifecycle": "eager",
      "headers": {
	      "Authorization": "Bearer xxx"
	  }
    }
  }
}
```
- 或者npm:pi-mcp-adapter，PROJECT/.pi/mcp.json ~/.pi/agent/mcp.json，
	- 额外支持 .mcp.json,  ~/.config/mcp/mcp.json, ~/.agents/mcp.json, ~/.agents/mcp/mcp.json，不需要设置transport

# 配置
- ~/.pi/agent
- 设置语言：~/.pi/agent/AGENTS.md 写思考和输出必须用xxx即可
