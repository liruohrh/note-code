- 默认footer：token相关显示有`↑` input, `↓` output, `R` cache read, `W` cache write, `CH` latest cache hit rate), cost, context usage

```bash
printf "%s\n" npm:@heyhuynhgiabuu/pi-search npm:pi-subagents npm:gentle-engram npm:context-mode npm:pi-token-usage npm:pi-token-burden npm:pi-mcp-extension | xargs -n1 pi install

# powershell
"" -split " " | Foreach-Object { pi install $_  }
```

- pi-token-usage：可以显示项目、项目今日、今日
- pi-token-burden：查看token花费的分布
- pi-mcp-extension: PROJECT/.pi/mcp.json ~/.pi/agent/mcp.json