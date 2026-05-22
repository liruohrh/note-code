- 设置变量
	- 参数：-Dxxxx=xxx
	- cmake：`set()`
- 变量优先级：就近原则
- 命令
	- - init:  `cmake --preset default`  必须configure preset
	- build
	  - `cmake --build --preset default`
	  - `cmake --build --preset default --target hello_play`
- CMAKE_CXX_FLAGS
	- "-W" 忽视所有警告
	- "-Wno-switch"
	- 不知道为什么，这个变量无效，不知道怎么忽视warning

# 配置文件


## 配置-CMakePresets.json
- 可以说是代替命令行参数的

## 项目配置-CmakeLists.txt