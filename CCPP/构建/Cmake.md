- 设置变量
	- 参数：-Dxxxx=xxx
	- cmake：`set()`
- 变量优先级：就近原则
- 命令
	- - init:  `cmake --preset default`  必须configure preset
	- build
	  - `cmake --build --preset default`
	  - `cmake --build --preset default --target hello_play`

# 配置文件


## 配置-CMakePresets.json
- 可以说是代替命令行参数的

## 项目配置-CmakeLists.txt