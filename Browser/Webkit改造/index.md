- https://webkit.org/contributing-code/

# 标准输出标准错误

- 重新分配
```c++

// 分配Console，且将标准输出和标准错误重定向到该窗口
// 该console将输出所有进程的标准输出和错误
AllocConsole();
freopen("CONOUT$", "w", stderr);
freopen("CONOUT$", "w", stdout);
```

- 重定向
```c++
// 不能用AllocConsole，否则标准输出和错误无法重定向
// 只能重定向当前进程，特殊情况如在Source\WebCore\page\Navigator.cpp就没办法，只能AllocConsole来查看终端
class FileStreamBuf : public std::streambuf {
public:
    FileStreamBuf(FILE* f) : m_file(f) {}
protected:
    int overflow(int c) override {
        if (c != EOF) fputc(c, m_file);
        return c;
    }
    std::streamsize xsputn(const char* s, std::streamsize n) override {
        fwrite(s, 1, n, m_file);
        return n;
    }
private:
    FILE* m_file;
};

// 初始化时调用
void redirectToLog(FILE* logFile) {
    static FileStreamBuf buf(logFile);
    std::cerr.rdbuf(&buf);
    std::cout.rdbuf(&buf);
}
```
# 环境
- 参考 [WebKit_Windows11编译](../WebKit_Windows11编译)
- 并修改环境
	- cmake 3.29.9（3.29即可），解决cmake生成后手动ninja无法编译的问题（参考 [增量编译](#增量编译)）

# 编译控制
- 编译步骤
	- 生成：`perl Tools/Scripts/build-webkit --release --generate-project-only --use-ccache`
		- use-ccache开启后编译速度才极度提升，仅编译部分修改文件+连接对应的部分库和可执行文件
	- 编译：`ninja -C WebKitBuild/Release -j 4`
		- -j：最大并发编译
		- -C：指定编译路径，必须含build.ninja
	- 如果不需要控制ninja
		- `perl Tools/Scripts/build-webkit --release --use-ccache`
- [增量编译](/CCPP/构建/Ninja)
- `DCURL_DISABLE_DOH=OFF`

## 编译 MiniBrowser & Playwright
- 编译 MiniBrowser：`Source\cmake\OptionsWin.cmake` ， ENABLE_MINIBROWSER默认ON，建议设置OFF
	- 不关闭，可能会有错误，且关闭后，编译目标没变，可能是增量编译没起效果
	- 可能会有错误：Tools\MiniBrowser\win\CMakeFiles\MiniBrowser.dir\MiniBrowserLib.rc.res Tools\MiniBrowser\win\CMakeFiles\MiniBrowser.dir\MiniBrowserLib.rc.res.pp
- 编译 Playwright：`Tools\PlatformWin.cmake` ， ENABLE_WEBKIT，即默认on
	- 也是在此处判断ENABLE_MINIBROWSER


## 修改注意事项
- 尽可能不要修改代码生成部分，一旦修改将重新编译大量文件（可能有900多）

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
