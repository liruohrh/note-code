# 文件路径与测试、运行 
- 当测试时，如goland通常会在测试目录中执行，导致配置文件路径或者其他路径不对，或者文件相对路径在非项目根目录时总是要做一些修改，比如修改运行目录或者修改文件路径，有人习惯在项目根目录下运行，也有人习惯按ide默认行为运行

## 方法

### embed-配置固定
### 动态-自动寻找项目根目录
```go
// runtime.Caller(0) 获取当前函数所在文件的绝对路径，然后自己调整到项目根路径即可
func GetProjectPath() string {  
    _, file, _, _ := runtime.Caller(0)  
    return filepath.Dir(filepath.Dir(filepath.Dir(file)))  
}

// 或者

func FindProjectRoot(moduleName string) (string, error) {  
    _, filename, _, ok := runtime.Caller(0)  
    if !ok {  
       return "", fmt.Errorf("failed to get current file path")  
    }  
  
    dir := filepath.Dir(filename)  
    for {  
       modFile := filepath.Join(dir, "go.mod")  
       if _, err := os.Stat(modFile); err == nil {  
          file, _ := os.Open(modFile)  
          scanner := bufio.NewScanner(file)  
          if scanner.Scan() {  
             line := scanner.Text()  
             line = strings.TrimSpace(line)  
             if strings.HasPrefix(line, "module") && strings.HasSuffix(line, moduleName) {  
                _ = file.Close()  
                return dir, nil   
}  
          }  
          _ = file.Close()  
       }  
       parent := filepath.Dir(dir)  
       if parent == dir {   
          break  
       }  
       dir = parent  
    }  
    return "", fmt.Errorf("go.mod for %s not found", moduleName)  
}
```


# 模块依赖
- 如果每个都自己调用initXX函数，就需要自己注意init顺序
- 需要能便利地更换依赖，比如事务执行时，事务对象的传递
	- 感觉模块对象可以有withXXX方法来替换某一依赖
# dao、service功能重叠？
- 个人认为dao只做复杂sql查询、单表查询比较合适，如果需要填充关联对象，在不使用dao进行连表的情况下，用service比较合适