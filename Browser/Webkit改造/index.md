- https://webkit.org/contributing-code/

# 编译控制
- cmake是构建文件生成器，WebKit通常用Ninja，在windows上则是 使用cl的兼容版clang-cl
- 编译步骤
	- 生成：`perl Tools/Scripts/build-webkit --release --generate-project-only --use-ccache`
	- 编译：`ninja -C WebKitBuild/Release -j 4`
		- 最大并发编译
	- 如果不需要控制ninja
		- `perl Tools/Scripts/build-webkit --release --use-ccache`

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
- 如果不删除这2个文件，可能报错
	- `ninja: error: FindFirstFileExA(Note: including file:      C:/Program Files (x86)/Windows Kits/10/include/10.0.26100.0/shared): The filename, directory name, or volume label syntax is incorrect.  `
		- 原因：[Ninja](\WebKitBuild\Release\CMakeFiles\rules.ninja) 用 deps = msvc + /showIncludes 来做依赖跟踪，但 clang-cl 输出的 /showIncludes 路径格式是正斜杠 + 空格 +括号的组合，Windows 的 FindFirstFileExA API 无法处理。
		- 方法
		1. `set(CMAKE_NINJA_DEPTYPE msvc)` ❌
		2. `set CLANG_CL=-fmsc-version=19.44`❌
		3. `ninja -d keeprsp -C WebKitBuild\Release`❌

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




# Clang LSP

- `clangd.exe --check=D:\mwk\Tools\Playwright\win\WinMain.cpp`
	- 该命令会输出比较多的东西，包括是否使用了compile_comomands.json



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
	- 执行Tools\Scripts\build-webkit时添加--export-compile-commands就会设置环境变量EXPORT_COMPILE_COMMANDS="YES"
	- 不过，默认情况下基本都会生成


- 用时候会报错一些版本问题
	- 在clangd lsp日志里会有`Indexing c++14 standard library in the context of xxxxfile`
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
			- 除了直接添加参数"/std:c++latest"外
			- 对于.h、.mm，添加了"-std=c++2b"
				- .h、.mm仍然报错，无用：
					- 直接注释掉
					- 替换为`/std:c++2b` 、`/std:c++latest`、`/clang:-std=c++latest`、
						- **这个才行**：`/clang:-std=c++2b`
					- `Source\cmake\OptionsMSVC.cmake` 
						- 添加`MSVC_ADD_COMPILE_OPTIONS("/std:c++latest")`
						- 添加
							- `set(CMAKE_CXX23_STANDARD_COMPILE_OPTION "/std:c++latest")`
							- `set(CMAKE_CXX23_EXTENSION_COMPILE_OPTION "/std:c++latest")`
				- 但是不推荐去解决这些报错，因为编译还是正常编译的，只是开发时比较恶心人而已
					- `Source\WebKit\NetworkProcess\NetworkSessionCreationParameters.h`
						- 这个就没办法了，`#include "ResourceLoadStatisticsParameters.h"` 总是报错 `In included file: expected ')'`
					- `Tools\Playwright\win\Common.h` 在换成`/clang:-std=c++2b`也不报错了
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
