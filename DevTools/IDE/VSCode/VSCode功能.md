# 配置文件
+ 可以导出导入
+ 默认使用默认配置文件，可以创建新的配置文件，并在几个配置文件之间进行切换
+ 对象：用户（所有/当前用户（安装方式）），所有工作区，当前工作区

# 用户代码片段
+ snippets
    - 保存在`/C:/Users/LYM/AppData/Roaming/Code/User/snippets/xxx.json`
+ `$0`是最终光标位置，`$n`是第n个参数位置（从1开始）
    - 按tab会到下一个参数位置

```json
"snippetsName": {
  "prefix":"",
  "body":[
    "printf(\"$1\",$2);"
  ],
  "description": ""
}
```



# workspace
+ Single Folder Workspace：就是一个工作目录
    - 目录名就是Workspace名
+ Multi-Root Workspace：一个工作目录包含多个不同的目录，每个目录相互隔离
    - 把配置保存为`{name}.code-workspace` （JSON文件）
        * 文件名就是Workspace名
        * folders中的每个folder：
            + path指定folder（项目）的路径（相对于该.code-workspace文件或者绝对路径）
            + name指定folder（项目）的名字（显示的是name，而不是目录名）
        * settings：这个workspace的配置
+ [launch、task、git等](https://code.visualstudio.com/docs/editor/multi-root-workspaces#_workspace-launch-configurations)







