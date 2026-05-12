# 增量解析
- 构建：`build/www`(html)
- 解析文件变化以git为主，否则在build/change.json记录，以便增量解析
- markdown路径：默认git忽视的`/contents`
	- 允许指定路径，可在git跟踪中
	- 允许指定git分支

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


# AI
