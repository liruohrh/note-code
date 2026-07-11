# 介绍
- 2 种执行方式
	- 设置环境变量和 PATH：`mise activate xxxshell`
	- shim：在 use 或者安装时会自动在`~/.local/share/mise/shims`创建可执行文件链接
		- `mise activate --shims`  则会设置到 PATH 中
		- https://mise.jdx.dev/dev-tools/shims.html#shims-vs-path
- 专门用于sdk等管理，同时适配shell、ide环境
	- `mise use tool@version `会自动安装，同时设置mise.toml
		- `-g/--global`：全局使用

# 安装
- MISE_INSTALL_PATH=xxx/mise
- MISE_DATA_DIR=xxx/mise
	- 或者XDG_DATA_HOME

# 使用

- mise.toml
	- 如tool版本、环境变量
	- 全局（.config/mise/config.toml）、项目（mise.toml）
- 使用已安装路径：`mise link tool@version path`
- 查看当前 tools `mise ls`
- 查看可获取 tools `mise ls-remote xx`
- 安装tool：`mise use xxx | mise use -g xxx`
	- `mise use go:xxx`：backend安装tool，用go安装go的工具，但是不放在gobin，而是作为mise tool，每个不同go会用其自己的gobin
- 设置环境变量：`mise set xxx | mise set -g xxx`