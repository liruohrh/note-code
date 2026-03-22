-  task
    - [Visual Studio Code 中的任务](https://code.visualstudio.com/docs/editor/tasks)
    - [Visual Studio Code Tasks Appendix](https://code.visualstudio.com/docs/editor/tasks-appendix)
+ ${}引用的变量
    - [Visual Studio Code Variables Reference](https://code.visualstudio.com/docs/editor/variables-reference)
+ launch
    - [在 Visual Studio Code 中调试](https://code.visualstudio.com/docs/editor/debugging)

# 介绍
+ vscode是纯编辑器，不过因为其强大的插件功能而强大
+ 命令面板：Ctrl+Shift+P，执行命令（插件命令，官方命令，@就扫描当前文件进行执行）

# vscode写代码逻辑
+ vscode打开的目录叫**workplace**
    - 在下面编写代码
    - .vscode目录是vscode的配置
        * launch.json：执行启动（执行语言的可执行文件）/附加（即Debug一个进程）命令
            + 主要视图是Topbar的Run、LeftSidebar的Run And Debugger（可以选择一个配置对象运行）
        * tasks.json： 编译等命令
            + 主要视图是Topbar的Terminal
                - 运行生成任务：就是进行build，其他不是build，而是在build上操作，运行其他命令
            + 写在tasks属性外的，作用在每个task上

# 配置
## tasks.json
+ [task接口定义](https://code.visualstudio.com/docs/editor/tasks-appendix)
+ windows：windows特定命令
+ linux：linux特定命令
+ tasks：task执行一个命令（编译命令）
    - type：规定好的,比如go，java，cppbuild。。。
        * 但是实际上只有2种，shell和process（作为一个进程执行）
    - label：该任务的名字
    - command：执行的命令（可以是绝对路径，比如go，如果go的bin目录在环境变量path中，则可以直接写go）
    - args：一个数组，写命令的参数
        * 当然可以在command中写，args就不用了（args不用为参数加单引号作为字符串---防止空格，但是如果直接写在command需要加单引号如果参数有空格）
    - detail：显示任务的详细信息
    - presentation：表现形式
        * panel=new：每次都是新窗口，=shared：共享一个窗口（默认），=dedicated：不同任务使用不同窗口，但是继续使用打开的窗口
        * clear=false：每次都不会清空窗口内容（默认）
        * reveal=always：面板始终位于前面（默认）
        * close=false：表示执行完命令不关闭（默认）
    - options
        * 覆盖 the defaults for (current working directory), (environment variables), or (default shell)
        * env：添加环境变量
            + 测试：`command : "sh ./test.sh"`   写入像`echo $GOROOT`这样打印环境变量
        * cwd：命令执行路径，默认`${workspaceFolder}`
        * shell：shell程序
    - group
        * kind：有test，build，none（表示没有组，默认值）
        * `"group": { "isDefault":true, kind:"test" } /  "group": "test"`
            + group默认是default，ctrl+shift+p执行Run Test/Build Task会直接运行默认任务，不是默认的需要手动执行
    - dependsOn：数组
        * 依赖某些任务，即dependsOn先执行，再执行本任务（本任务可以什么都不做，就执行该依赖== 指定顺序执行任务）
    - dependsOrder：依赖执行顺序
        * 默认parallel，即并行执行dependsOn的任务
        * sequence，顺序执行dependsOn的任务
    - runOptions：定义什么时候如何运行任务

## launch.json
+ 每一种`type`可以配置属性有一样的，也有不一样的
    - 比如对于java就有vmArgs属性
+ [https://code.visualstudio.com/docs/editor/debugging#_run-and-debug-view](https://code.visualstudio.com/docs/editor/debugging#_run-and-debug-view)
+ `request`：`launch/attach`
+ `args`：在cmd执行的命令最后追加
+ 一般会执行所有configuration对象，相同type的，也可能不都执行（执行一下其他可以直接启动的）
    - 因此可以这配置一点，那配置一点，如下

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "java",
      "name": "Launch with Arguments Prompt",
      "request": "launch",
      "mainClass": "",
      "args": "${command:SpecifyProgramArgs}"
    },
    {
      "type": "java",
      "name": "Main",
      "request": "launch",
      "mainClass": "com.liruo.vscode.Main",
      "projectName": "java-red-hat-server_bccc830c"
    }
  ]
}

```

# 例子
## tasks.json
```json
{
    "tasks": [
      //a c++ example
        {
            "type": "process",
            "label": "cpp build",
            "command": "g++",
            "args": [
                "-fdiagnostics-color=always",
                "-g",
                "${file}",
                "-o",
                "${fileDirname}\\${fileBasenameNoExtension}.exe"
            ],
            "options": {
                "cwd": "${fileDirname}"
            },
            "problemMatcher": [
                "$gcc"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "detail": "a c++ build task"
        },
      //options
        {
            "type": "shell",
            "label": "shell cmd",
            "command": "sh ./test.sh",
            "options": {
                "env": {
                    "env1": "addtional-env1"
                },
                "cwd": "${workspaceFolder}/cwd-test"
            },
            "group": "test"
        },
      //Default task and no Default task
        {
            "type": "shell",
            "label": "test 2",
            "command": "echo 11111",
            "group": {
                "kind": "test",
                "isDefault": true
            }
        },
      //dependsOn
        {
            "type": "shell",
            "label": "dependsOn1",
            "command": "echo 1111",
        },
        {
            "type": "shell",
            "label": "dependsOn2",
            "command": "echo 2222",
        },
        {
            "type": "shell",
            "label": "dependsOn3",
            "command": "echo 3333",
            "dependsOrder": "sequence",
            "dependsOn":["dependsOn2", "dependsOn1"]
        }
    ],
    "version": "2.0.0"
}
```

## launch.json
```json
{
    "version": "0.2.0",
    "configurations": [
      //a go example
        {
            "name": "Launch Package",
            "type": "go",
            "request": "launch",
            "mode": "auto",
            "program": "${fileDirname}"
        },
      //a c++ example
        {
              //在label=build的任务之后执行
              "preLaunchTask": "build",
              "name": "cpp-run",
              "type": "cppdbg",
              "request": "launch",        
              "program": "${workspaceFolder}\\bin\\${fileBasenameNoExtension}.exe",
              "args": [],
              //命令工作的路径，默认是workspaceFolder
              "cwd": "${workspaceFolder}",
              "stopAtEntry": false,
              "environment": [],
              "MIMode": "gdb",
              "externalConsole": false,
              "miDebuggerPath": "gdb",
              "setupCommands": [
                  {
                      "description": "为 gdb 启用整齐打印",
                      "text": "-enable-pretty-printing",
                      "ignoreFailures": true
                  },
                  {
                      "description":  "将反汇编风格设置为 Intel",
                      "text": "-gdb-set disassembly-flavor intel",
                      "ignoreFailures": true
                  }
              ]
          }
    ]
}
```

# vscode变量
## 变量
+  **workspaceFolder** ：vscode 打开的目录的路径----工作目录
    - **workspaceFolderBasename** 
        * 工作目录名
+  **fileDirname** ：选中文件的路径的目录路径
    - **fileDirnameBasename**
+  **file** ：选中文件的路径
    -  **fileBasename**：选中文件的文件名（单纯只是文件名） 
        *  **fileBasenameNoExtension** ：选中文件的的无扩展名的文件名
        *  **fileExtname** ：选中文件的扩展名
+  **relativeFile** ：是相对工作目录的路径	
    - 如work\demo\c.cpp
        * relativeFile=demo\c.cpp
        * **relativeFileDirname**=demo
+ **cwd**：当前命令运行目录的路径



## 案例
Supposing that you have the following requirements:

1. A file located at /home/your-username/your-project/folder/file.ext opened in your editor;
2. The directory /home/your-username/your-project opened as your root workspace.

So you will have the following values for each variable:

+ **${userHome}** - /home/your-username
+ **${workspaceFolder}** - /home/your-username/your-project
+ **${workspaceFolderBasename}** - your-project
+ **${file}** - /home/your-username/your-project/folder/file.ext
+ **${fileWorkspaceFolder}** - /home/your-username/your-project
+ **${relativeFile}** - folder/file.ext
+ **${relativeFileDirname}** - folder
+ **${fileBasename}** - file.ext
+ **${fileBasenameNoExtension}** - file
+ **${fileDirname}** - /home/your-username/your-project/folder
+ **${fileExtname}** - .ext
+ **${lineNumber}** - line number of the cursor
+ **${selectedText}** - text selected in your code editor
+ **${execPath}** - location of Code.exe
+ **${pathSeparator}** - / on macOS or linux, \ on Windows

## 环境变量
+ `${env:envName}`

## settings.json的属性
+ `${config:configName}`
    - 也可以在settings.json中使用

