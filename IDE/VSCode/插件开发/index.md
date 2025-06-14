
- https://code.visualstudio.com/
- 文档非常详细
# Extension Guides
- 一些能力，如Command

# UX/UE（User Experience）Guidelines
- https://code.visualstudio.com/api/ux-guidelines/overview
- Activity Bar：一些ViewContainer按钮，点击会在Primary Sidebar打开View，一个ViewContainer可以有多个view
- Sidebars
	- Primary Sidebar（left）：通常显示资源管理器、timeline
	- Secondary Sidebar（right）：通常显示outline
- Editor：编辑器，包括打开的文件和编辑区
- Status Bar：如右下角的文件language标识
- Panel：如teriminal、output


# 脚手架scaffold

- [Your First Extension | Visual Studio Code Extension API](https://code.visualstudio.com/api/get-started/your-first-extension)
- 使用

- `npm install --global yo generator-code`
- `yo code`

# 调式插件

- 就使用生成的launch中的调试配置
- 最新的包含`"preLaunchTask": "${defaultBuildTask}"`删除或者注释掉，不然没法运行插件
- 更新需要重启

# 激活插件
- https://code.visualstudio.com/api/references/activation-events#Start-up

# UI区域
## 编辑区
- 最多9个(`vscode.ViewColumn`)编辑器，每个编辑器都有一个TabGroup
	- `vscode.window.visibleTextEditors`  
	- `vscode.window.activeTextEditor`
	- `vscode.window.tabGroups.all`
	- `vscode.window.tabGroups.activeTabGroup`
- vscode.window.visibleTextEditors


# 视图容器(ViewContainer)

# 视图(View)
## TreeView
- TreeItem失去焦点时不会自动清空view的selection，同时也无法监听，顶多按ESC手动取消焦点
- menu
	- 默认用command字符串排序，另一种就是group加`@n`
- fire：触发多次仅执行一次
- 事件
	- onDidChangeVisibility：初次加载时可见也会传递true


# 持久化
- `context.workspaceState`：当前workspace数据
- `context.globalState`：全局数据

- extensionUri 、extensionPath：插件所在目录
- storageUri：插件针对一个工作区的数据存储目录（可能不存在，需要自己创建）
	- 注意不是storageState数据存储的目录，而是额外的数据
	- `{USER_DATA}\workspaceStorage\{workspaceId}\{authorname.extname}`
- globalStorageUri：同storageUri，只不过是globalStorage
- logUri：output panel的日志
	- `%appdata%/{appname}/logs/{yyyyMMddThhmmss}/window4/exthost/{authorname.extname}`


# 弹出对话框
- `vscode.window.showXXX`
- 如 [showErrorMessage](https://code.visualstudio.com/api/references/vscode-api#2623)：左下角弹出对话框，因为是error因此是红色的
## 参数
- message：显示的message
- items：每个元素将被渲染成一个文本按钮选项，该showXX函数将返回这个元素
	- 如果是一个对象，isCloseAffordance=true且modal=true时替换cancel按钮
	- ![[vscode_dialog.png]]
- options:
	- modal：变成中间的对话框
	- detail：message是标题，detail是详情
	- ![[vscode_dialog_modal.png]]


## showInputBox
- 在中间显示
- ![[vscode_inputbox.png]]
- 属性
	- value：默认填充的值
	- valueSelection：选择start到end，让用户方便地选择性修改value的部分内容
	- ignoreFocusOut：计算没有焦点也不会关闭
	- validateInput：返回空表示通过，错误信息将替换prompt

## showQuickPick
- 列表item选择器
- ![[vscode_QuickPick.png]]

- QuickPickItemKind.Separator：仅使用label属性，不渲染为一个item，而是下一个item的尾部文字

## 其他
- showOpenDialog：打开系统资源管理器，打开一个文件
- showSaveDialog：打开系统资源管理器，选择一个路径，将uri的文件保存到该路径
- showWorkspaceFolderPick：选择工作区的一个folder（在多工作区时选择一个根工作区）

- showNotebookDocument：在编辑器打开一个notebook文件
	- 需要用`vscode.workspace.openNotebookDocument`打开
- showTextDocument：在编辑器打开一个文本文件
	- 需要用`vscode.workspace.openTextDocument`打开

# 显示进度条
- `vscode.window.withProgress`
- options
	- location
		- `ProgressLocation.SourceControl`：source control这个ViewContainer会显示加载状态，完成后有一个通知
		- `ProgressLocation.Window`：底部状态栏
		- `ProgressLocation.Notification：左下脚通知栏区


# Buildin
## Command
- workbench.action.openSettings：打开设置，参数：`search`
- setContext：设置一个上下文，无法读，用于contributes中的when
- vscode.open：打开一个文件，默认在当前tabGroup
	- 参数TextDocumentShowOptions：
		- preview：默认true，会一直在当前tab打开
		- viewColumn：指定编辑器，默认当前