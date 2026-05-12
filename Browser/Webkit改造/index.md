- https://webkit.org/contributing-code/

# 编译控制
- cmake + ninja为每个编译目标生成编译命令，在windows上则是 使用cl的兼容版clang-cl

## 编译 MiniBrowser & Playwright
- 编译 MiniBrowser：`Source\cmake\OptionsWin.cmake` ， ENABLE_MINIBROWSER默认ON，建议设置OFF
	- 不关闭，可能会有错误，且关闭后，编译目标没变，可能是增量编译没起效果
	- 可能会有错误：Tools\MiniBrowser\win\CMakeFiles\MiniBrowser.dir\MiniBrowserLib.rc.res Tools\MiniBrowser\win\CMakeFiles\MiniBrowser.dir\MiniBrowserLib.rc.res.pp
- 编译 Playwright：`Tools\PlatformWin.cmake` ， ENABLE_WEBKIT，即默认on
	- 也是在此处判断ENABLE_MINIBROWSER
## 增量编译
- 关键文件
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
- 如果不删除这2个文件，报错
	- `ninja: error: FindFirstFileExA(Note: including file:      C:/Program Files (x86)/Windows Kits/10/include/10.0.26100.0/shared): The filename, directory name, or volume label syntax is incorrect.  `
		- 原因：[Ninja](\WebKitBuild\Release\CMakeFiles\rules.ninja) 用 deps = msvc + /showIncludes 来做依赖跟踪，但 clang-cl 输出的 /showIncludes 路径格式是正斜杠 + 空格 +括号的组合，Windows 的 FindFirstFileExA API 无法处理。
		- 方法
		1. `set(CMAKE_NINJA_DEPTYPE msvc)` ❌
		2. `set CLANG_CL=-fmsc-version=19.44`❌
		3. `ninja -d keeprsp -C WebKitBuild\Release`❌

```bash
# 全量（只编译修改部分）

# -j 表示并发5，否则可能会因为内存不够而失败
ninja -j 5 -C WebKitBuild\Release

ninja -C WebKitBuild\Release
# 指定库，如WebKit、WebCore、JavaScriptCore、Playwright
ninja -C WebKitBuild\Release WebKit
ninja -C WebKitBuild\Release Playwright
# 另外建议在编译前先刷新 compile_commands.json 和 symlink：
ninja -C WebKitBuild\Release RewriteCompileCommands UpdateCompileCommandsSymlink

# 该命令会输出比较多的东西，包括是否使用了compile_comomands.json
clangd.exe --check=D:\mwk\Tools\Playwright\win\WinMain.cpp
```




# Clang LSP
`ninja -C WebKitBuild\Release RewriteCompileCommands UpdateCompileCommandsSymlink`
  这会执行两个步骤：
  1. RewriteCompileCommands — 读取 CMake 生成的 WebKitBuild\Release\compile_commands.json（含 UnifiedSource
  占位），展开成 DeveloperTools\compile_commands.json（~118MB，每个源文件都有独立条目）
  2. UpdateCompileCommandsSymlink — 更新根目录 symlink：D:\mwk\compile_commands.json →
  WebKitBuild\Release\DeveloperTools\compile_commands.json

  如果从零开始（比如删了 build 目录重新 CMake），需要先运行 CMake 配置：

  ```
cmake -S D:\mwk -B D:\mwk\WebKitBuild\Release -G Ninja ^
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ^
  -DCMAKE_TOOLCHAIN_FILE=D:\mwk\WebKitBuild\Release\vcpkg_installed\...\scripts\buildsystems\vcpkg.cmake
  ```


- 默认情况下，是自动生成的，查看`Source\cmake\WebKitCommon.cmake`中的CMAKE_EXPORT_COMPILE_COMMANDS

- 用时候会报错一些版本问题
	- 在`.clangd` 的编译参数添加`"/clang:-std=c++23"`，但是这样不是个好方法
		- `/clang` 传递给clang，`-std=c++23` 明确的cpp版本
	- 实际解决方法
		- 参考
			- https://github.com/clangd/clangd/issues/1850
			- https://github.com/llvm/llvm-project/issues/101818
			- https://github.com/clangd/clangd/issues/527
		- 用"/clang:-std=c++23"、"/std:c++latest"，而不是"/clang:-std:c++latest"、 "-std:c++latest"、 "-std:c++23"
		- 直接编译可以"-std:c++latest"，但是clang lsp不行
		- clang lsp只能通过`.clangd`来修改编译参数，而无法设置clangd的参数来完成
		- https://github.com/llvm/llvm-project/issues/101818#issuecomment-4429806929


# 版本
- 根目录下的CMakeLists.txt：`cmake_minimum_required(VERSION 3.20)`
- `Source\cmake\OptionsCommon.cmake`：`set(CMAKE_CXX_STANDARD 23)`


# 命令
- 代码格式化检查：`python Tools/Scripts/check-webkit-style path/to/file`
- 格式化：`python Tools\Scripts\webkit-patch format --git-commit=HEAD...`

# 代码格式化
- 代码格式化检查：`python Tools/Scripts/check-webkit-style path/to/file`
- 格式化：`python Tools\Scripts\webkit-patch format --git-commit=HEAD...

- clang-format配置文件位于.clang-format
	- .clang-format可能版本不对吧，即便用了也有问题，添加一下参数后，就没有修改了
		- SpaceBeforeParens: ControlStatements
		- SpacesInParens: Never
- zed默认不用配置文件
	- 同时还要配置remove_trailing_whitespace_on_save=false（否则会移除注释后的空白）
```json
{
  "languages": {
    "C++": {
      "formatter": {
        "external": {
          "command": "clang-format",
          "arguments": ["--style=file"]
        }
      }
    }
  },
}
```
