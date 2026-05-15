`ninja -C WebKitBuild/Release -j 4`
- -j：最大并发编译
- -C：指定编译路径，必须含build.ninja


# 增量编译

```bash
# 默认就是根据.ninja_log增量编译
ninja -C WebKitBuild\Release

# -j 表示并发5，否则可能会因为内存不够而失败
ninja -j 5 -C WebKitBuild\Release

# 指定库，如WebKit、WebCore、JavaScriptCore、Playwright
ninja -C WebKitBuild\Release Playwright


# 另外建议在编译前先刷新 compile_commands.json 和 symlink到根目录：
ninja -C WebKitBuild\Release RewriteCompileCommands UpdateCompileCommandsSymlink
```


## 关键文件
- `WebKitBuild\Release\.ninja_log`
	- 构建记录，文本格式。Ninja 用它判断哪些文件需要重编：
		- 内容
			- `time 输入文件时间戳 输出文件时间戳  命令`
			- `5      source.cpp        source.obj      clang-cl...`
	  - 每次编译一个文件，Ninja 记下源代码和目标文件的修改时间
	  - 下次运行，对比时间戳，没变过的文件就跳过
	  - 文件丢失 → Ninja 只能全量重编
- `WebKitBuild\Release\.ninja_deps`
	- 依赖关系数据库，二进制格式。Ninja 用它判断头文件变化后要重编哪些源文件：
	  - 编译器输出 /showIncludes 的信息解析后存入此文件
	  - 记录了每个 .obj 依赖了哪些头文件
	  - 头文件修改时间更新 → Ninja 查出所有依赖它的 .obj → 只重编这些
## 如果不删除这2个文件，可能报错
- `ninja: error: FindFirstFileExA(Note: including file:      C:/Program Files (x86)/Windows Kits/10/include/10.0.26100.0/shared): The filename, directory name, or volume label syntax is incorrect.  `
	- 原因：[Ninja](\WebKitBuild\Release\CMakeFiles\rules.ninja) 用 deps = msvc + /showIncludes 来做依赖跟踪，但 clang-cl 输出的 /showIncludes 路径格式是正斜杠 + 空格 +括号的组合，Windows 的 FindFirstFileExA API 无法处理。
	- 方法
	1. `set(CMAKE_NINJA_DEPTYPE msvc)` ❌
	2. `set CLANG_CL=-fmsc-version=19.44`❌
	3. `ninja -d keeprsp -C WebKitBuild\Release`❌
- 有时候删了.ninja_deps就可以，有时候有.ninja_deps也可以
- 参考
	- https://github.com/ninja-build/ninja/issues/2280
	- https://gitlab.kitware.com/cmake/cmake/-/work_items/25753
- 解决
	- `ninja -C WebKitBuild/Release -t deps`：里面是 `Note: including file: {filepath}` 这种诡异的内容
	- 参考cmake参考的issue，升级到3.29即可（注意删除build.ninja、.ninja_deps再重新执行生成命令）
