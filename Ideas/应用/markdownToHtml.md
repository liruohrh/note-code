# Index
- 很多框架都有本项目的功能，但是可能是不够AI化，希望AI驱动生成美观主题、组件，AI优化内容、生成SEO
- 目标用户：
	- 公司介绍+Blog
	- 产品介绍+Blog
	- 个人博客

# 命令
- 构建
	- 增量时要合适地更新除文档外的东西
	- 强制构建：忽略增量
- 部署
	- github pages
	- 通过ssh自动化部署
- docker容器
	- 构建容器
	- 部署容器


# 增量解析
- 构建：`build/www`(html)
- 解析文件变化以git为主，否则在build/change.json记录，以便增量解析
- markdown路径：默认git忽视的`/contents`
	- 允许指定路径，可在git跟踪中
	- 允许指定git分支
- 以修改时间进行更新？还是hash？

# UI
- 解析每个语法，每个语法都用对应的组件渲染，可自由替换默认组件，每个组件都可以自定义配置
- 可增加自定义语法解析，必须指定组件
- 必须要有主题功能

# 文章内容
- URL：默认名称转英文（如拼音），可配置
- 目录=分类，markdown=分类下的内容
- 目录配置
	- index：默认index.html、index.md、README.md
		- 即点击目录打开的页面
- 页面配置
	- title：
	- description：
	- ...更多SEO字段
- 相同配置
	- directPath：点击重定向的路径


# 搜索
- 开启后构建索引

# AI
- AI友好：主题配置、组件编写
- SKILLS或者其他AI辅助信息

# 响应式
- 适配PC、平板、移动
