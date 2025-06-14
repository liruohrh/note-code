- 这是package.json的一个属性，描述vscode应用的，因此打包后package.json仍然是插件目录下的文件
# viewsContainers
- 一个viewsContainer包含多个View
- 目前支持activitybar、panel、auxiliaryactivitybar（Second Sidebar）
- 属性
	- id：viewId（views中的id）
	- titile：标题
	- icon：
		- 引用VSCode资源
			- https://code.visualstudio.com/api/references/icons-in-labels
			- 如`$(heart)`
		- 引用自定义资源
			- 不知道为什么，我的图标总是显示全白（dark）或者全黑（light），即便图片是24x24，透明色、模仿SpringBoot
			- SpringBoot的logo就可以用[SpringBoot VSCode](https://github.com/Microsoft/vscode-spring-boot-dashboard)

# views
- 配置view
# 关于group属性
- [官方没有介绍group有什么值，只介绍了排序和一些view的group](https://code.visualstudio.com/api/references/contribution-points#Sorting-of-groups)
	- navigation：总是第一排
	- inline：被渲染为一个toolbar，即item标题后面的action按钮
	- group会用一条写分隔
		- group排序：`n_group`表示排序，如`2_xxx`表示xxx排到第2个
		- group内排序：`group@n`，如`xxx@1`表示在xxx里排到第1个