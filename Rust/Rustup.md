- rustup是toolchain管理命令行工具，详细见 https://rust-lang.github.io/rustup/concepts/index.html
- 更新：`rustup update`
- 卸载：`rustup self uninstall`

# 配置
- settings.toml
```toml
default_host_triple = "x86_64-pc-windows-msvc"
default_toolchain = "nightly-x86_64-pc-windows-msvc"
profile = "default"
```
- 这几个配置一定要设置好，特别是`default_host_triple`，`rustup default`无法修改
	- `rustup[EXE] set default-host <HOST_TRIPLE>`
		- 安装时会设置
	- `rustup[EXE] set profile [PROFILE_NAME]`
		- default：默认，编译器、标准库、rust-docs
		- minimal：仅 Rust 编译器（`rustc`）和 Cargo，不含标准库（需手动安装）。
		- complete：包含所有组件（如 `rustfmt`、`clippy`、`miri` 等）。
