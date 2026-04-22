# WebKit

- 分支
  - safari-7624.1.16.11-branch：Apple Safari 对应版本的 release branch（冻结主线 + 维护分支）

- tag

  - Safari-533.10

    - Safari浏览器

  - WebKit-7613.2.6

    - WebKit引擎

  - releases/Apple/Safari-10-iOS-10.0、releases/Apple/Safari-8.0.8-macOS-10.10.5

    - Apple 官方 release snapshot（绑定 OS + Safari 版本的源码快照）

  - releases/Apple/Safari-Technology-Preview-144

    - 新特色实验渠道

  - webkitgtk-2.36.4

    - GTK port版本、Linux 桌面浏览器（Epiphany 等）、嵌入式 GTK 应用

  - wpewebkit-2.44.4

    - WPE（嵌入式）版本、Smart TV、车载系统、IoT 浏览器

    - 📌 和 GTK 的关系：

      - 共用 WebKit core

      - 不同 UI backend（Wayland / 嵌入式设备）

# 环境

- git clone --depth 1 --branch WebKit-7624.1.16.11.4 https://github.com/webKit/webkit
- https://docs.webkit.org/Build%20%26%20Debug/BuildOptions.html#building-windows-port
- https://docs.webkit.org/Ports/WindowsPort.html

- 安装vs2022，安装c++ destop环境
  - Microsoft (R) C/C++ Optimizing Compiler Version 19.44.35214 for x64
- choco install -y xampp-81 python311 ruby git cmake gperf llvm ninja
  - 用管理员权限
  - cmake 3.27.9
    - CMake 3.20+ CMakeLists.txt:9
  - ninja 1.13.2
    - 自动探测，推荐构建功能
  - llvm 20.1.0
    - 20.1.0 报错5
    - 22.1.0 报错2、6
    - 17 不行，报错4
    - Tools/CISupport/safer-cpp-llvm-version：WebKit-7624.1.16.11.4至少要22.1.0
      - 12 20, 2025 https://github.com/llvm/llvm-project/commit/25e2480b1217eea62a386107a7e494d20452378d
      - 2 24, 2026 https://github.com/llvm/llvm-project/commits/llvmorg-22.1.0
      - 2 10, 2026 https://github.com/llvm/llvm-project/commits/llvmorg-22.1.0-rc3
      - 1 27, 2026 https://github.com/llvm/llvm-project/commits/llvmorg-22.1.0-rc2
      - 7 15, 2025 https://github.com/llvm/llvm-project/commits/llvmorg-22-init
      - 12 12, 2025 https://github.com/llvm/llvm-project/commits/llvmorg-21.1.8

- git clone https://github.com/microsoft/vcpkg
  - 执行bootstrap-vcpkg.bat
  - 设置VCPKG_ROOT=该仓库路径

- 复制并修改构建文档里的脚本到 ./build2.bat
- 执行./build2.bat

# 最终构建环境

- gperf 3.1.0
- python311 3.11.9
- ruby 3.4.9.1
- ruby.install 3.4.9.1
- vswhere 3.1.7
- XAMPP-81 8.1.6
- ninja 1.13.2
- VS2022 Desktop development with C++, Microsoft (R) C/C++ Optimizing Compiler Version 19.44.35214 for x64
- vcpkg master 296b89248a 2026-4-16


- 主要改动了以下环境
  - cmake 3.27.9
  - llvm 20.1.0
  - main 2874cfdad914 2026-4-21最新版
    - 其实webkit_5e02fd1 2026-4-15也能编译，只是需要上面的修改环境
    - 但是WebKit-7624.1.16.11.4 2026-3-4不能编译

- 环境脚本
```bash
choco install -y xampp-81 python311 ruby git gperf ninja
choco install -y cmake --version 3.27.9
choco install -y llvm --version 20.1.0
python -m pip install pywin32
git config --global core.autocrlf input
```

- 最终构建脚本：没有改环境之类的东西，只是增加了快速编译的脚本
```bash
@echo off
cd %~dp0

path C:\xampp\apache\bin;%path%
path C:\xampp\perl\bin;%path%
@REM path %ProgramFiles%\CMake\bin;%path%
path %ProgramFiles(x86)%\Microsoft Visual Studio\Installer;%path%

path %~dp0WebKitLibraries\win\bin;%path%
set WEBKIT_TESTFONTS=%~dp0Tools\WebKitTestRunner\fonts
set DUMPRENDERTREE_TEMP=%TEMP%

set CC=clang-cl
set CXX=clang-cl

@echo on
where cmake
cmake --version
where ninja
ninja --version
where clang
clang --version
where perl
perl --version

echo "start build WebKit..."


cd D:\wk

d:
rd /s /q WebKitBuild
rd /s /q vcpkg_installed
rd /s /q CMakeFiles
del CMakeCache.txt

perl Tools/Scripts/build-webkit --release
```



# 其他坑

## Windows文件路径长度

- `Remove-Item -Path "\\?\D:\ws\lib\webkit-ws\webkit_5e02fd1\WebKitBuild" -Recurse -Forces`
- Computer Configuration → Administrative Templates → System → Filesystem → Enable Win32 long paths = Enabled
- git需要主动开启才行：`git config --global core.longpaths true`

# 错误

## 7 llvm15不行

- webkit_WebKit-7624.1.16.11.4 2026-3-4

```bash
CMake Error at Source/cmake/OptionsMSVC.cmake:64 (find_library):
  Could not find CLANG_BUILTINS_LIBRARY using the following names:
  clang_rt.builtins-x86_64
Call Stack (most recent call first):
  Source/cmake/OptionsWin.cmake:2 (include)
  Source/cmake/WebKitCommon.cmake:241 (include)
  CMakeLists.txt:21 (include)
```

## 6 llvm22 -Wno-missing-format-attribute

- webkit_WebKit-7624.1.16.11.4 2026-3-4

- llvm22(因为Tools/CISupport/safer-cpp-llvm-version尝试从20换回22), 在/CMakeLists.txt顶部加入

```bash
add_compile_options(
    -Wno-missing-format-attribute
    -Wno-error=missing-format-attribute
)
```

- 但是还是失败了

```bash
[3035/9712] Building CXX object Source\JavaScriptCore\CMakeFiles\...e\DerivedSources\unified-sources\UnifiedSource-6cbc989f-2.cpp.ob
FAILED: [code=1] Source/JavaScriptCore/CMakeFiles/JavaScriptCore.dir/__/__/JavaScriptCore/DerivedSources/unified-sources/UnifiedSource-6cbc989f-2.cpp.obj
...
D:\wk\WebKitBuild\Release\JavaScriptCore\DerivedSources\unified-sources\UnifiedSource-6cbc989f-2.cpp
In file included from D:\wk\WebKitBuild\Release\JavaScriptCore\DerivedSources\unified-sources\UnifiedSource-6cbc989f-2.cpp:1:
In file included from D:\wk\Source\JavaScriptCore\yarr/YarrPattern.cpp:34:
D:\wk\Source\JavaScriptCore\yarr\YarrParser.h(90,18): error: initializing pointer member 'm_data' with the stack address of parameter 'pattern' [-Werror,-Wdangling-field]
   90 |         , m_data(pattern.span<CharType>().data())
      |                  ^~~~~~~
D:\wk\Source\JavaScriptCore\yarr\YarrParser.h(2271,16): note: in instantiation of member function 'JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, unsigned char>::Parser' requested here
 2271 |         return Parser<Delegate, Latin1Character>(delegate, pattern, compileMode, backReferenceLimit, isNamedForwardReferenceAllowed).parse();
      |                ^
D:\wk\Source\JavaScriptCore\yarr/YarrPattern.cpp(2617,27): note: in instantiation of function template specialization 'JSC::Yarr::parse<JSC::Yarr::YarrPatternConstructor>' requested here
 2617 |         ErrorCode error = parse(constructor, patternString, compileMode());
      |                           ^
D:\wk\Source\JavaScriptCore\yarr\YarrParser.h(2199,21): note: pointer member declared here
 2199 |     const CharType* m_data;
      |                     ^
D:\wk\Source\JavaScriptCore\yarr\YarrParser.h(90,18): error: initializing pointer member 'm_data' with the stack address of parameter 'pattern' [-Werror,-Wdangling-field]
   90 |         , m_data(pattern.span<CharType>().data())
      |                  ^~~~~~~
D:\wk\Source\JavaScriptCore\yarr\YarrParser.h(2272,12): note: in instantiation of member function 'JSC::Yarr::Parser<JSC::Yarr::YarrPatternConstructor, char16_t>::Parser' requested here
 2272 |     return Parser<Delegate, char16_t>(delegate, pattern, compileMode, backReferenceLimit, isNamedForwardReferenceAllowed).parse();
      |            ^
D:\wk\Source\JavaScriptCore\yarr/YarrPattern.cpp(2617,27): note: in instantiation of function template specialization 'JSC::Yarr::parse<JSC::Yarr::YarrPatternConstructor>' requested here
 2617 |         ErrorCode error = parse(constructor, patternString, compileMode());
      |                           ^
D:\wk\Source\JavaScriptCore\yarr\YarrParser.h(2199,21): note: pointer member declared here
 2199 |     const CharType* m_data;
      |                     ^
D:\wk\Source\JavaScriptCore\yarr\YarrParser.h(90,18): error: initializing pointer member 'm_data' with the stack address of parameter 'pattern' [-Werror,-Wdangling-field]
   90 |         , m_data(pattern.span<CharType>().data())
      |                  ^~~~~~~
D:\wk\Source\JavaScriptCore\yarr\YarrParser.h(2271,16): note: in instantiation of member function 'JSC::Yarr::Parser<JSC::Yarr::SyntaxChecker, unsigned char>::Parser' requested here
 2271 |         return Parser<Delegate, Latin1Character>(delegate, pattern, compileMode, backReferenceLimit, isNamedForwardReferenceAllowed).parse();
      |                ^
D:\wk\Source\JavaScriptCore\yarr/YarrSyntaxChecker.cpp(75,12): note: in instantiation of function template specialization 'JSC::Yarr::parse<JSC::Yarr::SyntaxChecker>' requested here
   75 |     return parse(syntaxChecker, pattern, compileMode(parsedFlags));
      |            ^
D:\wk\Source\JavaScriptCore\yarr\YarrParser.h(2199,21): note: pointer member declared here
 2199 |     const CharType* m_data;
      |                     ^
D:\wk\Source\JavaScriptCore\yarr\YarrParser.h(90,18): error: initializing pointer member 'm_data' with the stack address of parameter 'pattern' [-Werror,-Wdangling-field]
   90 |         , m_data(pattern.span<CharType>().data())
      |                  ^~~~~~~
D:\wk\Source\JavaScriptCore\yarr\YarrParser.h(2272,12): note: in instantiation of member function 'JSC::Yarr::Parser<JSC::Yarr::SyntaxChecker, char16_t>::Parser' requested here
 2272 |     return Parser<Delegate, char16_t>(delegate, pattern, compileMode, backReferenceLimit, isNamedForwardReferenceAllowed).parse();
      |            ^
D:\wk\Source\JavaScriptCore\yarr/YarrSyntaxChecker.cpp(75,12): note: in instantiation of function template specialization 'JSC::Yarr::parse<JSC::Yarr::SyntaxChecker>' requested here
   75 |     return parse(syntaxChecker, pattern, compileMode(parsedFlags));
      |            ^
D:\wk\Source\JavaScriptCore\yarr\YarrParser.h(2199,21): note: pointer member declared here
 2199 |     const CharType* m_data;
      |                     ^
4 errors generated.
[3048/9712] Building CXX object Source\JavaScriptCore\CMakeFiles\...\DerivedSources\unified-sources\UnifiedSource-f2e18ffc-31.cpp.ob
ninja: build stopped: subcommand failed.
```

## 5 llvm20.1.0

- llvm20.1.0
- webkit_WebKit-7624.1.16.11.4 2026-3-4

```bash
In file included from D:\wk\WebKitBuild\Release\WebCore\DerivedSources\unified-sources\UnifiedSource-3c72abbe-39.cpp:1:
D:\wk\Source\WebCore\platform/graphics/SourceBrush.cpp(64,7): error: member access into incomplete type 'TextStream'
   64 |     ts.dumpProperty("color"_s, brush.color());
      |       ^
D:\wk\WebKitBuild\Release\WTF\Headers\wtf/Forward.h(70,7): note: forward declaration of 'WTF::TextStream'
   70 | class TextStream;
      |       ^
In file included from D:\wk\WebKitBuild\Release\WebCore\DerivedSources\unified-sources\UnifiedSource-3c72abbe-39.cpp:1:
D:\wk\Source\WebCore\platform/graphics/SourceBrush.cpp(67,11): error: member access into incomplete type 'TextStream'
   67 |         ts.dumpProperty("gradient"_s, *gradient);
      |           ^
D:\wk\WebKitBuild\Release\WTF\Headers\wtf/Forward.h(70,7): note: forward declaration of 'WTF::TextStream'
   70 | class TextStream;
      |       ^
In file included from D:\wk\WebKitBuild\Release\WebCore\DerivedSources\unified-sources\UnifiedSource-3c72abbe-39.cpp:1:
D:\wk\Source\WebCore\platform/graphics/SourceBrush.cpp(68,11): error: member access into incomplete type 'TextStream'
   68 |         ts.dumpProperty("gradient-space-transform"_s, brush.gradientSpaceTransform());
      |           ^
D:\wk\WebKitBuild\Release\WTF\Headers\wtf/Forward.h(70,7): note: forward declaration of 'WTF::TextStream'
   70 | class TextStream;
      |       ^
In file included from D:\wk\WebKitBuild\Release\WebCore\DerivedSources\unified-sources\UnifiedSource-3c72abbe-39.cpp:1:
D:\wk\Source\WebCore\platform/graphics/SourceBrush.cpp(72,11): error: member access into incomplete type 'TextStream'
   72 |         ts.dumpProperty("pattern"_s, pattern.get());
      |           ^
D:\wk\WebKitBuild\Release\WTF\Headers\wtf/Forward.h(70,7): note: forward declaration of 'WTF::TextStream'
   70 | class TextStream;
      |       ^
4 errors generated.
[8771/9712] Building CXX object Source\WebCore\CMakeFiles\WebCore...e\DerivedSources\unified-sources\UnifiedSource-be65d27a-7.cpp.ob
ninja: build stopped: subcommand failed.
```

## 4 llvm17不行，需要llvm20

- webkit_WebKit-7624.1.16.11.4 2026-3-4

````bash
[516/9712] Building CXX object Source\bmalloc\CMakeFiles\bmalloc.dir\bmalloc\AllIsoHeaps.cpp.obj
FAILED: [code=1] Source/bmalloc/CMakeFiles/bmalloc.dir/bmalloc/AllIsoHeaps.cpp.obj
...
In file included from D:\wk\Source\bmalloc\bmalloc\AllIsoHeaps.cpp:27:
In file included from D:\wk\Source\bmalloc\bmalloc/AllIsoHeaps.h:34:
In file included from D:\wk\Source\bmalloc\bmalloc/IsoHeapImpl.h:34:
In file included from D:\wk\Source\bmalloc\bmalloc/BMalloced.h:28:
In file included from D:\wk\Source\bmalloc\bmalloc/bmalloc.h:34:
In file included from D:\wk\Source\bmalloc\bmalloc/AllocationCounts.h:31:
In file included from C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\include\atomic:8:
In file included from C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\include\yvals.h:12:
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\include\yvals_core.h(908,1): error: static assertion failed: error STL1000: Unexpected compiler version, expected Clang 19.0.0 or newer.
  908 | _EMIT_STL_ERROR(STL1000, "Unexpected compiler version, expected Clang 19.0.0 or newer.");
      | ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\include\yvals_core.h(534,58): note: expanded from macro '_EMIT_STL_ERROR'
  534 | #define _EMIT_STL_ERROR(NUMBER, MESSAGE)   static_assert(false, "error " #NUMBER ": " MESSAGE)
      |                                                          ^~~~~
1 error generated.
[517/9712] Building CXX object Source\bmalloc\CMakeFiles\bmalloc.dir\bmalloc\Gigacage.cpp.obj
FAILED: [code=1] Source/bmalloc/CMakeFiles/bmalloc.dir/bmalloc/Gigacage.cpp.obj
...
In file included from D:\wk\Source\bmalloc\bmalloc\Gigacage.cpp:26:
In file included from D:\wk\Source\bmalloc\bmalloc/Gigacage.h:30:
In file included from D:\wk\Source\bmalloc\bmalloc/Algorithm.h:31:
In file included from C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\include\algorithm:8:
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\include\yvals_core.h(908,1): error: static assertion failed: error STL1000: Unexpected compiler version, expected Clang 19.0.0 or newer.
  908 | _EMIT_STL_ERROR(STL1000, "Unexpected compiler version, expected Clang 19.0.0 or newer.");
      | ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\include\yvals_core.h(534,58): note: expanded from macro '_EMIT_STL_ERROR'
  534 | #define _EMIT_STL_ERROR(NUMBER, MESSAGE)   static_assert(false, "error " #NUMBER ": " MESSAGE)
      |                                                          ^~~~~
1 error generated.
ninja: build stopped: subcommand failed.
````

## 3 靠vs自带的cmake、ninja不行，必须额外下载

- 就原来choco安装即可
- webkit_5e02fd1 2026-4-15

- 和1的错误输出一样

## 2 llvm22不行，需要llvm20

- webkit_5e02fd1 2026-4-15

```bash
[442/9529] Building CXX object Source\bmalloc\CMakeFiles\bmalloc.dir\bmalloc\Logging.cpp.obj
FAILED: Source/bmalloc/CMakeFiles/bmalloc.dir/bmalloc/Logging.cpp.obj
...
D:\ws\lib\webkit-ws\webkit_5e02fd1\Source\bmalloc\bmalloc\Logging.cpp
D:\ws\lib\webkit-ws\webkit_5e02fd1\Source\bmalloc\bmalloc\Logging.cpp(41,34): error: diagnostic behavior may be improved by adding the 'format(printf, 4, 5)' attribute to the declaration of 'reportAssertionFailureWithMessage' [-Werror,-Wmissing-format-attribute]
   41 |     vfprintf(stderr, format, args);
      |                                  ^
D:\ws\lib\webkit-ws\webkit_5e02fd1\Source\bmalloc\bmalloc\Logging.h(37,6): note: 'reportAssertionFailureWithMessage' declared here
   37 | void reportAssertionFailureWithMessage(const char* file, int line, const char* function, const char* format, ...) BATTRIBUTE_PRINTF(4, 5);
      |      ^
1 error generated.
[455/9529] Building CXX object Source\bmalloc\CMakeFiles\bmalloc.dir\libpas\src\libpas\bmalloc_heap.c.obj
ninja: build stopped: subcommand failed.s
```

## 1 长路径

- webkit_5e02fd1 2026-4-15

手动在 D:/ws/lib/webkit-ws/webkit_5e02fd1/WebKitBuild/Release/vcpkg_installed/vcpkg/blds/woff2/x64-windows-webkit-rel/vcpkg-parallel-configure
执行 ninja -v，报错，警告里有路径名太长，即便启动了长路径，这个构建系统可能不支持，必须换到极短路径如 /wk

```
Make Error at CMakeLists.txt:10 (cmake_minimum_required):
  Compatibility with CMake < 3.5 has been removed from CMake.

  Update the VERSION argument <min> value.  Or, use the <min>...<max> syntax
  to tell CMake that the project requires at least <min> but has been updated
  to work with policies introduced by <max> or earlier.

  Or, add -DCMAKE_POLICY_VERSION_MINIMUM=3.5 to try configuring anyway.
```

```bash
C:\Users\devp\AppData\Local\vcpkg\registries\git-trees\d0e0bbbc0e52c9aeb727d03d053fc9410f15e417: info: installing from git registry git+https://github.com/microsoft/vcpkg@d0e0bbbc0e52c9aeb727d03d053fc9410f15e417
Downloading https://sqlite.org/2026/sqlite-autoconf-3510200.tar.gz -> sqlite-autoconf-3510200.tar.gz
Successfully downloaded sqlite-autoconf-3510200.tar.gz
-- Extracting source C:/Users/devp/AppData/Local/vcpkg/downloads/sqlite-autoconf-3510200.tar.gz
-- Applying patch fix-arm-uwp.patch
-- Applying patch add-config-include.patch
-- Using source at D:/ws/lib/webkit-ws/webkit_5e02fd1/WebKitBuild/Release/vcpkg_installed/vcpkg/blds/sqlite3/src/nf-3510200-ccd32d7cbc.clean
-- Found external ninja('1.12.1').
-- Configuring x64-windows-webkit
-- Building x64-windows-webkit-dbg
-- Building x64-windows-webkit-rel
-- Fixing pkgconfig file: D:/ws/lib/webkit-ws/webkit_5e02fd1/WebKitBuild/Release/vcpkg_installed/vcpkg/pkgs/sqlite3_x64-windows-webkit/lib/pkgconfig/sqlite3.pc
-- Using cached msys2-mingw-w64-x86_64-pkgconf-1~2.3.0-1-any.pkg.tar.zst
-- Using cached msys2-msys2-runtime-3.5.4-2-x86_64.pkg.tar.zst
-- Using msys root at C:/Users/devp/AppData/Local/vcpkg/downloads/tools/msys2/21caed2f81ec917b
-- Fixing pkgconfig file: D:/ws/lib/webkit-ws/webkit_5e02fd1/WebKitBuild/Release/vcpkg_installed/vcpkg/pkgs/sqlite3_x64-windows-webkit/debug/lib/pkgconfig/sqlite3.pc
-- Installing: D:/ws/lib/webkit-ws/webkit_5e02fd1/WebKitBuild/Release/vcpkg_installed/vcpkg/pkgs/sqlite3_x64-windows-webkit/share/sqlite3/usage
-- Performing post-build validation
Starting submission of sqlite3[core,fts3,json1,rtree]:x64-windows-webkit@3.51.2 to 1 binary cache(s) in the background
Elapsed time to handle sqlite3:x64-windows-webkit: 18 s
sqlite3:x64-windows-webkit package ABI: bfd0514fc619ef8137d83fde126e49dde7f0433081c294cfb536995c95af0d8f
Completed submission of libxslt[core,profiler,thread]:x64-windows-webkit@1.1.45 to 1 binary cache(s) in 11 s
Installing 26/26 woff2:x64-windows-webkit@1.0.2#5...
Building woff2:x64-windows-webkit@1.0.2#5...
D:\ws\lib\webkit-ws\webkit_5e02fd1\WebKitLibraries\triplets\x64-windows-webkit.cmake: info: loaded overlay triplet from here
C:\Users\devp\AppData\Local\vcpkg\registries\git-trees\5a12f112e02313670c8e24d72d72a83ce74521b4: info: installing from git registry git+https://github.com/microsoft/vcpkg@5a12f112e02313670c8e24d72d72a83ce74521b4
-- Note: woff2 only supports static library linkage. Building static library.
Downloading https://github.com/google/woff2/archive/v1.0.2.tar.gz -> google-woff2-v1.0.2.tar.gz
Successfully downloaded google-woff2-v1.0.2.tar.gz
-- Extracting source C:/Users/devp/AppData/Local/vcpkg/downloads/google-woff2-v1.0.2.tar.gz
-- Applying patch 0001-unofficial-brotli.patch
-- Applying patch 0002-stdint-include.patch
-- Using source at D:/ws/lib/webkit-ws/webkit_5e02fd1/WebKitBuild/Release/vcpkg_installed/vcpkg/blds/woff2/src/v1.0.2-69d515c840.clean
-- Found external ninja('1.12.1').
-- Configuring x64-windows-webkit
CMake Error at scripts/cmake/vcpkg_execute_required_process.cmake:127 (message):
Command failed: "C:/Program Files/Microsoft Visual Studio/2022/Community/Common7/IDE/CommonExtensions/Microsoft/CMake/Ninja/ninja.exe" -v
Working Directory: D:/ws/lib/webkit-ws/webkit_5e02fd1/WebKitBuild/Release/vcpkg_installed/vcpkg/blds/woff2/x64-windows-webkit-rel/vcpkg-parallel-configure
Error code: 1
See logs for more information:
D:\ws\lib\webkit-ws\webkit_5e02fd1\WebKitBuild\Release\vcpkg_installed\vcpkg\blds\woff2\config-x64-windows-webkit-dbg-CMakeCache.txt.log
D:\ws\lib\webkit-ws\webkit_5e02fd1\WebKitBuild\Release\vcpkg_installed\vcpkg\blds\woff2\config-x64-windows-webkit-rel-CMakeCache.txt.log
D:\ws\lib\webkit-ws\webkit_5e02fd1\WebKitBuild\Release\vcpkg_installed\vcpkg\blds\woff2\config-x64-windows-webkit-out.log

Call Stack (most recent call first):
D:/ws/lib/webkit-ws/webkit_5e02fd1/WebKitBuild/Release/vcpkg_installed/x64-windows/share/vcpkg-cmake/vcpkg_cmake_configure.cmake:269 (vcpkg_execute_required_process)
C:/Users/devp/AppData/Local/vcpkg/registries/git-trees/5a12f112e02313670c8e24d72d72a83ce74521b4/portfile.cmake:16 (vcpkg_cmake_configure)
scripts/ports.cmake:203 (include)

error: building woff2:x64-windows-webkit failed with: BUILD_FAILED
See https://learn.microsoft.com/vcpkg/troubleshoot/build-failures?WT.mc_id=vcpkg_inproduct_cli for more information.
Elapsed time to handle woff2:x64-windows-webkit: 3.3 s
Please ensure you're using the latest port files with `git pull` and `vcpkg update`.
Then check for known issues at:
https://github.com/microsoft/vcpkg/issues?q=is%3Aissue+is%3Aopen+in%3Atitle+woff2
You can submit a new issue at:
https://github.com/microsoft/vcpkg/issues/new?title=[woff2]+Build+error+on+x64-windows-webkit&body=Copy%20issue%20body%20from%20D%3A%2Fws%2Flib%2Fwebkit-ws%2Fwebkit_5e02fd1%2FWebKitBuild%2FRelease%2Fvcpkg_installed%2Fvcpkg%2Fissue_body.md

Waiting for 1 remaining binary cache submissions...
Completed submission of sqlite3[core,fts3,json1,rtree]:x64-windows-webkit@3.51.2 to 1 binary cache(s) in 12 s (1/1)
-- Running vcpkg install - failed
CMake Error at C:/Program Files/Microsoft Visual Studio/2022/Community/VC/vcpkg/scripts/buildsystems/vcpkg.cmake:938 (message):
vcpkg install failed. See logs for more information:
D:\ws\lib\webkit-ws\webkit_5e02fd1\WebKitBuild\Release\vcpkg-manifest-install.log
Call Stack (most recent call first):
C:/Program Files/CMake/share/cmake-4.3/Modules/CMakeDetermineSystem.cmake:146 (include)
CMakeLists.txt:10 (project)

CMake Error: CMake was unable to find a build program corresponding to "Ninja". CMAKE_MAKE_PROGRAM is not set. You probably need to select a different build tool.
CMake Error: CMAKE_C_COMPILER not set, after EnableLanguage
CMake Error: CMAKE_CXX_COMPILER not set, after EnableLanguage
-- Configuring incomplete, errors occurred!
Run Visual Studio installation vcvars.bat before build-webkit when using ninja at Tools/Scripts/build-webkit line 326.
```
