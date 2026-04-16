- 非持久化context的userdatadir`%temp%/playwright_chromiumdev_profile-xxxxx`

- 每次打开都会是一个全新的，且不会自动删除，因此相对麻烦点

- Launch：可以设置headless、传递参数

- `Launh`：仅启动后台浏览器，无context，必须newContext来操作浏览器
- `LaunchPersistentContext`可以设置userdatadir，且无browser、默认就有一个context（userdatadir）
- 通过CDP连接

- 默认就有一个context
- browser、context的close被无视（用pw的Launch则会优雅关闭）

- newContext：仅其可以设置StorageState
- AddCookies：不会根据当前pages进行过滤，有则替换，无则添加，失效则忽视

- 不会立即让浏览器进行刷盘（即cookie可能会丢失），不过通过页面加载可让浏览器触发刷盘机制