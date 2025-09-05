# defer执行一行函数
- 此时会将变量直接捕获，如果该变量中后面发生变化，defer里的必保函数的该变量不会改变
- 解决方法：使用`defer func(){ foo(xxx) }()` 而不是`defer foo(xxx)` 