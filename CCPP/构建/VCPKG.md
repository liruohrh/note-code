- https://github.com/microsoft/vcpkg
- 需要设置VCPKG_ROOT
- 仓库=package=port
- `vcpkg install <port>`
- `vcpkg install curl:x64-windows-webkit --recurse`
- manifest mode即使用vcpkg.json的情况下只能vcpkg install，其他都得修改vcpkg.json
- 查看库的构建信息：`buildtrees\{port}`

# 替换别人的仓库配置
- vcpkg-configuration.json的 overlay-ports 或者 overlay-triplets


# 配置
- 在cmake里使用，设置变量`CMAKE_TOOLCHAIN_FILE=$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake`
- 配置文件放项目根目录下
### 依赖：vcpkg.json（manifest mode）
```json
{
  "name": "playccpp",
  "version": "0.1.0",
  // 依赖
  "dependencies": [
    "fmt",
    {
      "name": "spdlog",
      "version>=": "1.12.0",
      // 仅编译features
      "features": [
        "cuda",
        "contrib"
      ]
    }
  ],
  // 本库的feature
  "features": {
    "c-ares": {
      "description": "Enable c-ares for asynchronous DNS requests.",
      "dependencies": [
        "c-ares"
      ]
    }
  },
  // 固定版本
  "overrides": [
    {
      "name": "ngtcp2",
      "version": "1.12.0"
    }
  ]
}
```

### 仓库：vcpkg-configuration.json
```json
{
  "default-registry": {
    "kind": "git",
    "baseline": "071f676f662b8d36a2f1762c63516e60b99d375b",
    "repository": "https://github.com/microsoft/vcpkg"
  },
  "registries": [
    {
      "kind": "git",
      "baseline": "a8c7798b3751d63d6b160df431031cd5e5c940d9",
      "repository": "https://github.com/WebKitForWindows/WebKitRequirements",
      "packages": [
        "cairo",
        "curl",
        "icu",
        "openssl",
        "zlib"
      ]
    }
  ],
  // 替换/新增“依赖源码构建规则”
  "overlay-ports": [
	  "./WebKitLibraries/triplets"
  ],
  // 替换“编译参数/ABI规则”
  "overlay-triplets": [
    "./WebKitLibraries/triplets"
  ]
}
```

---

# Port

- ports/zlib/
	- portfile.cmake  
	- vcpkg.json
里面定义：
- 下载地址
- patch
- CMake 参数
- install 规则

# 介绍
`vcpkg` 本质上是一个 **C/C++ 依赖包管理器**，它解决的是：
* 下载源码
* 配置编译参数
* 编译库
* 安装头文件 / lib / dll
* 处理依赖链
* 告诉 CMake 怎么找到这些库

它和 JS 的 npm、Rust 的 cargo、Go modules 有点像，但因为 C/C++ 没有统一 ABI、编译器、运行时，所以它复杂得多。

---

## 一、vcpkg 的核心工作原理

先看最核心的一句话：

> vcpkg 本质上是在“当前平台 + 当前编译器 + 当前 triplet”下构建一套独立依赖树。

例如：

```txt
x64-windows
x64-windows-static
x64-linux
arm64-osx
```

这些叫： Triplet（目标构建配置）

triplet 决定：

* 架构
* 动态/静态链接
* CRT
* 编译器 ABI
* 平台

例如：

| triplet            | 含义                  |
| ------------------ | ------------------- |
| x64-windows        | MSVC + 动态 CRT + 动态库 |
| x64-windows-static | MSVC + 静态 CRT + 静态库 |
| x64-linux          | gcc/clang           |
| arm64-osx          | Apple Silicon       |

---

## 二、vcpkg 内部结构

典型目录：

```txt
vcpkg/
├── ports/
├── installed/
├── packages/
├── buildtrees/
├── downloads/
├── scripts/
```

---

### 1. ports/

这是“配方”。

类似：

```txt
ports/zlib/
    portfile.cmake
    vcpkg.json
```

这里描述：

* 去哪里下载源码
* 如何 patch
* 如何 cmake configure
* 如何 install

---

### 2. downloads/

缓存源码压缩包：

```txt
downloads/zlib-1.3.tar.gz
```

避免重复下载。

---

### 3. buildtrees/

实际构建目录。

例如：

```txt
buildtrees/zlib/
```

里面会：

```txt
src/
build-x64-windows/
```

这里是真正执行：

```bash
cmake ..
ninja
```

的地方。

---

### 4. packages/

临时安装目录。

构建完成后先安装到这里：

```txt
packages/zlib_x64-windows/
```

然后再复制到：

---

### 5. installed/

最终给用户使用的目录。

例如：

```txt
installed/x64-windows/
    include/
    lib/
    bin/
    share/
```

真正项目链接的是这里。

---

## 三、vcpkg 安装库时到底发生了什么

例如：

```bash
vcpkg install zlib
```

内部流程：

---

### 第一步：解析 port

找到：

```txt
ports/zlib/portfile.cmake
```

---

### 第二步：解析依赖

例如：

```txt
zlib -> cmake helpers
```

递归安装。

---

### 第三步：下载源码

到：

```txt
downloads/
```

---

### 第四步：创建 buildtree

例如：

```txt
buildtrees/zlib/src/xxxxx.clean/
```

---

### 第五步：调用 CMake

本质是：

```bash
cmake -DCMAKE_TOOLCHAIN_FILE=...
```

然后：

```bash
ninja
```

或者：

```bash
msbuild
```

---

### 第六步：安装

执行：

```bash
cmake --install
```

到：

```txt
packages/zlib_x64-windows/
```

---

### 第七步：复制到 installed/

最终：

```txt
installed/x64-windows/include/zlib.h
installed/x64-windows/lib/zlib.lib
```

---

## 四、vcpkg 为什么能和 CMake 自动联动

核心：toolchain file

也就是：

```txt
scripts/buildsystems/vcpkg.cmake
```

这是最核心的东西。

---

## 五、CMake 的工作原理

正常情况下：

```cmake
find_package(ZLIB REQUIRED)
```

CMake 根本不知道：

```txt
zlib 在哪
```

因为：

* 不在系统路径
* 不在 `/usr/lib`
* 不在 Program Files

---

## 六、vcpkg toolchain 做了什么

当你：

```bash
cmake -DCMAKE_TOOLCHAIN_FILE=xxx/vcpkg.cmake
```

时。

vcpkg 会：

---

### 1. 修改 CMAKE_PREFIX_PATH

添加：

```txt
vcpkg/installed/x64-windows/
```

于是：

```cmake
find_package()
```

能找到：

```txt
share/zlib/zlib-config.cmake
```

---

### 2. 修改 find_library 路径

让：

```cmake
find_library()
```

搜索：

```txt
installed/x64-windows/lib
```

---

### 3. 修改 find_path

让：

```cmake
find_path()
```

搜索：

```txt
installed/x64-windows/include
```

---

### 4. 注入 triplet

例如：

```txt
VCPKG_TARGET_TRIPLET=x64-windows
```

---

### 5. 自动处理 Debug/Release

例如：

```txt
debug/lib/
lib/
```

自动切换。

---

## 七、为什么现代 CMake + vcpkg 很强

现代库会提供：

```txt
xxx-config.cmake
```

例如：

```txt
fmt-config.cmake
spdlogConfig.cmake
```

于是：

```cmake
find_package(fmt CONFIG REQUIRED)
target_link_libraries(app PRIVATE fmt::fmt)
```

即可。

完全不需要：

```cmake
include_directories()
link_directories()
```

这是现代 CMake 的核心思想： 一切通过 target 传播

包括：

* include path
* compile definitions
* link libs
* compile options

---

## 八、完整项目示例

---

### 安装

```bash
vcpkg install fmt
```

---

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.20)

project(test)

find_package(fmt CONFIG REQUIRED)

add_executable(test main.cpp)

target_link_libraries(test PRIVATE fmt::fmt)
```

---

### 配置

```bash
cmake -B build ^
  -DCMAKE_TOOLCHAIN_FILE=D:/vcpkg/scripts/buildsystems/vcpkg.cmake
```

---

### 编译

```bash
cmake --build build
```

---

## 九、Manifest Mode（现代推荐）

现代 vcpkg 推荐：

## vcpkg.json

例如：

```json
{
  "name": "myapp",
  "version": "1.0",
  "dependencies": [
    "fmt",
    "spdlog"
  ]
}
```

然后：

```bash
cmake ..
```

vcpkg 自动安装依赖。

这类似：

* npm package.json
* cargo.toml

---

## 十、Classic Mode vs Manifest Mode

| 模式       | 特点    |
| -------- | ----- |
| classic  | 全局安装  |
| manifest | 项目隔离  |
| manifest | 更现代   |
| manifest | CI友好  |
| manifest | 依赖可复现 |

现在基本推荐 manifest。

---

## 十一、ABI 哈希机制（vcpkg 很关键的设计）

vcpkg 会计算：

```txt
编译器
triplet
feature
cmake options
port version
依赖版本
```

生成 ABI hash。

如果 hash 不同：

重新编译。

这是它能缓存 binary package 的基础。

---

## 十二、为什么 WebKit / Chromium 不怎么用 vcpkg

因为：

* 它们依赖规模太大
* 需要深度 patch
* 强依赖特定编译参数
* 有自己的构建系统
* ABI 极其敏感

所以：

* Chromium -> DEPS + GN
* WebKit -> Tools/Scripts + CMake

而不是通用包管理器。

---

## 十三、vcpkg + Ninja + CMake 的真实关系

很多人误解：

```txt
vcpkg = 构建系统
```

其实不是。

关系：

```txt
CMake
  ↓ 生成
Ninja/MSBuild
  ↓ 编译

vcpkg
  ↓ 提供依赖
  ↓ 提供 toolchain
```

所以：

```txt
vcpkg ≠ build system
```

它只是： dependency provider

---

## 十四、最重要的现代最佳实践

推荐：

```txt
CMake + Ninja + vcpkg manifest
```

不要：

```txt
include_directories(...)
link_directories(...)
手写 lib 路径
复制 dll
```

现代写法：

```cmake
find_package()
target_link_libraries()
```

让 target 自动传播依赖。
