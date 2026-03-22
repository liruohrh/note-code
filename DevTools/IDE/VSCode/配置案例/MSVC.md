+ 以下是因为使用VS安装Windows Kits时安装出错，或者有问题
    - 这个情况甚至VS写C/C++都会报错
    - 先看Visual Studio的基本看看怎么解决出错
    - 然后就不需要自己设置LIB和INCLUDE了，直接用VS提供的命令行环境运行C/C++

# c_cpp_properties.json
```json
{
  "configurations": [
    {
      "name": "Win32",
      "includePath": [
        "${workspaceFolder}/**",
        "${config:WIN10_INCLUDES}ucrt/",
        "${config:WIN10_INCLUDES}um/",
        "${config:WIN10_INCLUDES}shared/",
        "${config:WIN10_INCLUDES}winrt/",
        "${config:WIN10_INCLUDES}cppwinrt/",
        "${config:MSVC_HOME}include/"
      ],
      "defines": ["_DEBUG", "UNICODE", "_UNICODE"],
      "cStandard": "c17",
      "cppStandard": "c++17",
      "intelliSenseMode": "windows-msvc-x64",
      "compilerPath": "cl.exe"
    }
  ],
  "version": 4
}

```

# settings.json
```json
{
  "WIN10_INCLUDES": "A:/Windows Kits/10/Include/10.0.22000.0/",
  "WIN10_LIBS": "A:/Windows Kits/10/LIB/10.0.22000.0/",
  "MSVC_HOME": "A:/ide/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.37.32822/",
  // 也可以在这里面直接配置环境变量, vscode的所有终端(任务也使用终端)
  "terminal.integrated.env.windows": {
    "VSCODE_SETTINGS1": "v"
  }
}

```

# 
# lanuch.json
```json
{
  // 使用 IntelliSense 了解相关属性。
  // 悬停以查看现有属性的描述。
  // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "type": "lldb",
      "request": "launch",
      "name": "Debug",
      "program": "${workspaceFolder}/${fileBasenameNoExtension}.exe",
      "args": ["v1", "v2", "v3"],
      "cwd": "${workspaceFolder}"
    }
  ]
}

```



# tasks.json
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "shell",
      "label": "MSVC cl(open vscode from VsDevCmd)",
      "detail": "MSVC Complie Task(open vscode from VsDevCmd)",
      "command": "cl.exe",
      "args": [
        "/Zi",
        "/EHsc",
        "/nologo",
        "/Fe${fileBasenameNoExtension}.exe",
        "${file}"
      ],
      "options": {
        "cwd": "${fileDirname}"
      },
      "problemMatcher": ["$msCompile"],
      "group": {
        "kind": "build",
        "isDefault": true
      }
    },
    {
      "type": "shell",
      "label": "MSVC cl(abs cl and set env by myself)",
      "detail": "MSVC Complie Task(use abs cl path to compile)",
      "command": "${config:MSVC_HOME}/bin/Hostx64/x64/cl.exe",
      "args": [
        "/Zi",
        "/EHsc",
        "/nologo",
        "/Fe${fileDirname}\\${fileBasenameNoExtension}.exe",
        "${file}"
      ],
      "options": {
        "env": {
          "INCLUDE": "${config:WIN10_INCLUDES}ucrt/;${config:WIN10_INCLUDES}um/;${config:WIN10_INCLUDES}shared/;${config:MSVC_HOME}include/;",
          "LIB": "${config:WIN10_LIBS}ucrt/x64/;${config:WIN10_LIBS}um/x64/;${config:MSVC_HOME}lib/x64/;"
        }
      },
      "problemMatcher": ["$msCompile"],
      "group": {
        "kind": "build",
        "isDefault": false
      }
    },
    {
      "type": "shell",
      "label": "MSVC cl(cmd open VsDevCmd)",
      "detail": "MSVC Complie Task(Not open vscode from VsDevCmd)",
      "command": "cl",
      "args": [
        "/Zi",
        "/EHsc",
        "/nologo",
        "/Fe${fileDirname}\\${fileBasenameNoExtension}.exe",
        "${file}"
      ],
      "options": {
        "shell": {
          "executable": "cmd.exe",
          "args": [
            "/c",
            "\"A:/ide/Microsoft Visual Studio/2022/Community/Common7/Tools/VsDevCmd.bat\"",
            "-startdir=none",
            "-arch=x64",
            "-host_arch=x64",
            "&&"
          ]
        }
      },
      "problemMatcher": ["$msCompile"],
      "group": {
        "kind": "build",
        "isDefault": false
      }
    },
    {
      "type": "shell",
      "label": "del middle",
      "detail": "del mvsc middle production, invoke in some active file to make dir some",
      "command": "del",
      "args": ["*.ilk", "*.obj", "*.pdb", "*.pdb"],
      "options": {
        "cwd": "${workspaceFolder}"
      }
    },
    {
      "type": "shell",
      "label": "del middle and exe",
      "detail": "del middle and exe file",
      "command": "del",
      "args": ["*.ilk", "*.obj", "*.pdb", "*.pdb", "*.exe"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": []
    }
  ]
}

```

