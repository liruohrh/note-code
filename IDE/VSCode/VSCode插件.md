

# 注释相关
- Better Comments：`*`、!、?、TODO，还允许自定义tag、颜色，新增更多
- Todo Tree：在文件下展示TODO
- Todo+：全局管理TODO，罗列所有TODO

# Prettier
- JS、TS、HTML、CSS格式化

- 配置
- webstorm的reformtter code不是prettier，prettier需要安装所有依赖后才能右键菜单出现使用prettier进行格式化

```json
{
//在vscode的配置前缀是prettier，使用prettier配置文件只是没有这个前缀而已
//es5会自动加逗号
"trailingComma": "es5",
"singleQuote": false,  
"tabWidth": 2,  
"printWidth": 120  //这个非常重要，决定了一行的宽度、换行
}
```


# Format Files
#vscode/ext/format

- 一键格式化一个目录

# CodeSnap
#vscode/ext/tool
- 代码截图，对长代码非常好
- 使用：选择代码，右键菜单选CodeSnap，跳出右边框显示截图结果
# Color Manager
#vscode/ext/color
- 配色板，有模板配色板
- 使用：右键选择一个菜单
# vscode-faker

#vscode/ext/fake_data
- 生成常见的假数据
- 使用：打开命令面板，输入Faker执行其中命令

# HTML CSS Support
 #vscode/ext/css/in_any #vscode/ext/css/cdn 
- 在任意语言中智能感知CSS文件CSS、style标签
- 指定css文件、CDN：`"css.styleSheets": ["css/*.css"]` glob匹配，默认无
- 指定语言：`"css.enabledLanguages": ["html", "javascript"]`
	- 对于javascript，需要在html字符串中，写class、id属性，或者js操作元素的className、id属性
# HTML to CSS autocompletion
  #vscode/ext/css/incss
- html的class属性在css文件中自动提示，但是id不行
- 配合[HTML CSS Support](#HTML CSS Support)使用很舒服

# CSS-in-JS
  #vscode/ext/css/injs
- 在JS的CSS snippets
# 关于 JS Intellisence
#vscode/ext/js/inline

- 默认情况下，Inline JS无法感知 External JS
	- https://github.com/microsoft/vscode/issues/26338
- 一个HTML的Inline JS之间可以相互补全，不同External JS也可以相互补全
	- 但是无法补全打包编译后的JS文件，只能通过下载，不过在`C:\Users\LYM\AppData\Local\Microsoft\TypeScript\5.8\`的node_modules有@type就可以使用这些TS进行补全
- Html Embedded Javascript：让Inline JS感知 External JS，但是External JS仍然补全不了Inline JS

# Inline HTML
#vscode/ext/js/str
- 用``` html`<div></div>`   ```的方式在标签模板字符串中智能提示、格式化HTML

# Auto Rename Tag
#vscode/ext/html/tag
- 修改标签名时，同步修改开始或者结束标签
