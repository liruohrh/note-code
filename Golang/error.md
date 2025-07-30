# 推荐写法
- `action1: description1; action2: description2: err`
	- action：动作、数据
	- description：对action的额外补充
- 对于在函数调用处的错误处理，则是适当补充上下文、场景


## 例子

### action

```go

//action+description
// 原写法
return fmt.Errorf("fail to click avatar, maybe not login: %w", err)
// 推荐写法
return fmt.Errorf("click avatar: element .caret not found or timeout (10s): %w", err)

//多action
return fmt.Errorf("encounter 503 on body; reload attempted but still fail to click .caret: %w", err)
```

### 上下文、场景
```go
// b.go —— 只做“自己”的事
func readConfig(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        // 这里只描述“读文件”失败即可
        return nil, fmt.Errorf("read config %s: %w", path, err)
    }
    return data, nil
}

// a.go —— 再决定是否补充
func loadUser() error {
    cfg, err := readConfig("user.toml")
    if err != nil {
        // 这里再补充“loadUser 场景”
        return fmt.Errorf("load user: %w", err)
    }
    // ...
    return nil
}
```
