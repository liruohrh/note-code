# go get
- `-u` 表示会讲package以及其依赖更新到最新的minor/patch
	- 这个比较坑爹，如果某个依赖进进行了API变动却没有更新major版本，导致更新到这个API不兼容版本，导致无法编译
- `package@latest`才是更新到最新版本

# 私有包
- `GOPRIVATE`（ 1.15+ 只需要这个）
	- 告诉 Go：`github.com/username/*` 是私有模块。
	- 一旦匹配：
		- 不会走公共模块代理 `proxy.golang.org`
		- 不会走公共校验数据库 `sum.golang.org`
		- 会直接用 `git` 从源码仓库下载
- `GONOPROXY`
	- 作用和 `GOPRIVATE` 的“禁止代理”部分一样，但可以单独控制。
	- 在这里是重复声明，目的是保险（有些工具只识别 `GONOPROXY`）。
- `GONOSUMDB`
	- 告诉 Go：这些模块不要用 `sum.golang.org` 做校验。
	- 公共 sumdb 是用来校验模块是否被篡改的，但私有模块 sumdb 是访问不到的，不关掉会报错。

```bash
# git config 因为go默认使用http，因此要用ssh就必须这样
git config --global url."git@github.com:".insteadOf "https://github.com/"
# 即
# [url "git@github.com:"]  # 或者ssh://git@github.com/
# 	insteadOf = https://github.com/

# go env
# 以下3个都是用逗号分隔，可以用通配符
go env -w GOPRIVATE=github.com/username/* #会自动设置以下2个
go env -w GONOPROXY=github.com/username/*
go env -w GONOSUMDB=github.com/username/*

# ssh config
Host github.com
    User git
    HostName github.com
    PreferredAuthentications publickey
    # 必须无密码才能拉取Go依赖
    IdentityFile ~/.ssh/private_key
```