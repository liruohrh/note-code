# 注意
+ 第一个Java文件最好带上package（即在package目录下创建），不然需要在底部Java Status选择Clean Workspace Cache然后重启重新分析项目

# Extension Pack for Java
+ 包括6个通用Java插件
+ Language Support for Java(TM) by Red Hat：编译、运行、编辑
    - 其他插件基本基于这个插件
+ Test Runner for Java：Test
+ Debugger for Java：Debug
+ Maven for Java：MavenUI

## Project Manager for Java：目录管理
### 功能
+ 资源管理器Java Project视图：项目结构查看
    - 开发时看这个资源管理器Item相对好点，而不是默认的项目Item
+ 创建项目：普通、maven、spring。。。
+ IntelliCode：智能提示

### 配置
```json
{
    //导出jar包路径
  "java.project.exportJar.targetPath": "${workspaceFolder}/${workspaceFolderBasename}.jar",
  //在资源管理器Java Project视图, 类中是否展示成员
  "java.dependency.showMembers": true,
  //在资源管理器Java Project视图, 展示非Java资源
  "java.project.explorer.showNonJavaResources": true
}
```

# Language Su pport for Java(TM) by Red Hat




## 配置
```json
{
  // default VSCODE_EXTENSIONS/RAD_HAT_JAVA_LANGUAGE_SERVER_EXTENSION_NAME/jre/JAVA_HOME
  //  旧name：java.home
  // "java.jdt.ls.java.home": "",d
  // 追加red hat java language server的vm启动参数, 可通过状态栏Java打开日志查看文件名含client的日志
  // "java.jdt.ls.vmargs": "-Dfile.encoding=UTF-8",

  "java.configuration.runtimes": [
    {
      "default": true,
      "name": "JavaSE-1.8",
      "path": "C:/Program Files/SDK/jdk_1.8.0_391"
    }
  ],
  "java.jdt.ls.lombokSupport.enabled": false,

  "java.project.sourcePaths": ["src/"],
  //default VSCODE_USERDATA/User/workspaceStorage/RANDOM_ID
  "java.project.outputPath": "target",
  "java.project.referencedLibraries": ["lib/**/*.jar"],
  // "java.project.referencedLibraries": {
  //   "include": ["library/**/*.jar", "/home/username/lib/foo.jar"],
  //   "exclude": ["library/sources/**"],
  //   "sources": {
  //     "library/bar.jar": "library/sources/bar-src.jar"
  //   }
  // },
  //排除文件, 加速Java Language Server
  "java.project.resourceFilters": ["node_modules", "\\.git"],
}
```



# Tomcat
+ [https://blog.csdn.net/qq_38628046/article/details/132906461](https://blog.csdn.net/qq_38628046/article/details/132906461)
+ 插件：Community  Server Connectors
+ 配置settings
    - 插件JDK`rsp-ui.rsp.java.home: "C:/Users/A814/.vscode/extensions/redhat.java-1.4.0/jre/17.0.2-win32-x86_64"`
+ 服务器配置
    - `args.override.boolean: "true"`允许覆盖
    - `args.vm.override.string`启动参数
    - `  
`

