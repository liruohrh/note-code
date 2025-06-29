- version: 1.21
- toolchain包含go、gofmt命令

- `go get go@version`：更新go.mod的go版本且下载Go（一个完整的Go）
	- 下载的包：`golang.org/toolchain@v0.0.1-go_VERSION_._GOOS_-_GOARCH_
	- 如果 `GOSUMDB=off` ，工具链下载会因为缺少验证而失败。模式 `GOPRIVATE` 和 `GONOSUMDB` 不适用于工具链下载。
- `go get toolchain@version`
	- 会在比go.mod的go更高时，添加指令`toolchain go{version}`（toolchain默认就是go.mod的go），还可能会下载 `golang.org/x/xxxpackage`

- go在运行命令时，如果go.mod声明的go或者toolchain比当前go版本更高时，自动执行`go get go@version`（可以通过go version确定到底使用了什么版本）

- goenv  GOTOOLCHAIN  控制toolchain（覆盖go.mod的go、toolchian），和`go get go@version`一样，会下载Go
	- 默认`GOTOOLCHAIN=auto`，即使用当前go、go.mod的go、toolchain中版本最高的
	- `GOTOOLCHAIN=go{version}` 强制使用这个版本 
	- `GOTOOLCHAIN=go{version}+auto` 使用这个版本、go.mod的go、toolchain中版本最高的
	- GOTOOLCHAIN=auto 等价于 GOTOOLCHAIN=local+auto（local就是所运行的go版本）

- `go get` 和 `go mod tidy` 命令保持 `go` 行大于或等于任何必需依赖模块的 `go` 行
	- 也就是下载依赖时可能会导致go 行更新
	- https://go.dev/doc/toolchain#get