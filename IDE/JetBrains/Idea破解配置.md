
- **配置目录**：
	- Windows：`%USERPROFILE%\AppData\Roaming\JetBrains\`
    - macOS：`~/Library/Application Support/JetBrains`
    - Linux：`~/.config/JetBrains`
		- `产品名 版本/小写产品名.key`
			- 根据激活码生成的文件
			- idea生成的包含16进制字符`efbbbfffff`、`<certificate-key>`、激活码
				- 因此推荐还是手动输入激活码，否则只能用程序或者16进制编辑器来编辑
		- `产品名 版本/小写产品名.vmoptions`
			- 此处可以配置agent以破解
			- 这个是用户配置，全局配置位于`${INSTALL_DIR}/bin/{可执行文件名}.vmoptions`
			- 远程连接：`jetbrains_client.vmoptions`

- **缓存目录**：
    - Windows：`%USERPROFILE%\AppData\Local\JetBrains\`
    - macOS：`~/Library/Caches/JetBrains`
    - Linux：`~/.cache/JetBrains`
    - `./.home`：文件内容是软件安装路径