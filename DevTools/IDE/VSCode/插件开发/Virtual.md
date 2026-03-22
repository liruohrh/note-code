
- 2者可以同时有，但是schame不能一样
- TextDocumentContentProvider：单个只读文件
	- https://code.visualstudio.com/api/extension-guides/virtual-documents
- FileSystemProvider：一个文件系统
	- [Virtual Workspaces](https://code.visualstudio.com/api/extension-guides/virtual-workspaces)
	- 在工作区打开虚拟工作目录，就如同Github Repositories插件一样
	- 用户在使用这个功能时，会被提醒：running in a restricted mode and that some extensions are deactivated or work with limited functionality.