```bash
printf "%s\n" npm:@heyhuynhgiabuu/pi-search npm:pi-subagents npm:gentle-engram npm:context-mode npm:pi-token-usage npm:pi-token-burden npm:pi-mcp-extension | xargs -n1 pi install

# powershell
"" -split " " | Foreach-Object { pi install $_  }
```

- `pi-mcp-extension`: PROJECT/.pi/mcp.json ~/.pi/agent/mcp.json