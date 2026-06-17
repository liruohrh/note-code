

# 依赖类型与检测方式

| 类别         | 怎么进二进制                     | ldd/NEEDED 能看到吗 | 例子                              |
| ---------- | -------------------------- | --------------- | ------------------------------- |
| 动态链接 (.so) | 链接期记下 soname,运行期由 ld.so 加载 | ✅ 能             | librice、libgstreamer            |
| 静态链接 (.a)  | 链接期把代码合并进二进制,运行期无痕         | ❌ 看不到           | 官方的 libwebrtc                   |
| dlopen 插件  | 程序运行中自己 dlopen()           | ❌ 看不到           | GStreamer 插件 (libgstwebrtc.so…) |

还要分三个时间点
- 配置期(决定"打算链什么"):CMakeCache.txt、pkg-config、FindXxx.cmake
- 链接期(实际链了什么命令):compile_commands.json、ninja -t commands
- 运行期(实际加载哪个文件):ldd、readelf -d、ldconfig -p、LD_DEBUG、`/proc/<pid>/maps`

## ① 它直接依赖哪些动态库?

```bash
readelf -d <file> | grep NEEDED        # 直接依赖,不递归,读元数据(最可靠)
ldd <file>                              # 递归闭包 + 当前环境下解析到的真实路径
```

实例:

libwebkitgtk-6.0.so 的 NEEDED 里有 librice-io.so.0 ← 你的构建动态链了 librice 的铁证。

---

## ② 它去哪儿找库、实际加载哪个文件?

```bash
readelf -d <file> | grep -iE 'rpath|runpath'   # 内嵌搜索路径
ldconfig -p | grep rice                         # 系统缓存把这库解析到哪
LD_DEBUG=libs <binary> 2>&1 | grep rice         # 运行期真相:实际从哪加载
cat /proc/<pid>/maps | grep rice                # 跑起来的进程到底映射了哪个
```

实例:

librice-proto.so.0 => /lib/x86_64-linux-gnu/librice-proto.so.0。

---

## ③ 静态链接的库(ldd 看不到)怎么查?

```bash
ls -lh <file>                              # 体积当旁证(官方 libwebkitgtk 99M = 含静态 libwebrtc)
file <file>                                # 看是否 stripped
strings -a <file> | grep -E 'rtc::|webrtc/'  # 找源码特征字符串(命中 500+ = 含 libwebrtc 代码)
nm <file> | grep ...                       # 没 strip 时能看内部符号(release 通常被 strip)
ar t libfoo.a ; nm libfoo.a                # 直接拆 .a 看成员/符号
```

实例:

官方 bundle 用这招才发现"虽然 ldd 没 rice,但 strings 里 rtc:: 533 次 = 静态链了 libwebrtc"。

---

## ④ dlopen 的插件(ldd 也看不到)怎么查?

```bash
ls <bundle>/sys/lib/gstreamer-1.0/          # 直接看插件目录
echo $GST_PLUGIN_PATH $GST_PLUGIN_SYSTEM_PATH
strace -f -e openat <binary> 2>&1 | grep '\.so'   # 抓运行时真正打开了哪些 .so
```

实例:

官方 bundle 的 gstreamer-1.0 目录里没有 webrtc/nice/dtls 插件 → 它不走 GStreamerWebRTC。

---

## ⑤ 符号层面:谁提供/谁需要某符号?

```bash
nm -D <file>                 # 动态符号:U=未定义(它需要别人给),T/W=导出(它提供)
nm -DC <file>                # 顺带解 C++ name mangling
nm -D <file> | grep rice_    # 实例:你的 libwebkitgtk 一堆 rice_;官方 = 0
```

---

## ⑥ 配置期:这次构建"决定"用哪套?

```bash
grep -iE 'USE_LIBRICE|USE_GSTREAMER_WEBRTC|RICE|WEBRTC' WebKitBuild/GTK/Release/CMakeCache.txt
pkg-config --modversion rice-proto      # cmake 背后就是问 pkg-config
pkg-config --libs --cflags rice-proto
```

实例:

USE_LIBRICE:BOOL=ON、Rice_PROTO_LIBRARY=/usr/lib/.../librice-proto.so —— 这是"你 vs 官方"差异的源头。

---

## ⑦ 模块级:某个 target / 编译单元链了/包含了什么?(你问的"某个模块")

```bash
# 哪些源文件用到了某库(看 -I 头路径)
grep -i rice WebKitBuild/GTK/Release/compile_commands.json

# 某个 target 实际的链接命令(Ninja 正确姿势,不是 link.txt)
ninja -C WebKitBuild/GTK/Release -t commands WebKit | tr ' ' '\n' | grep -E 'rice|\.a$|\.so'

# cmake 生成 target 依赖图
cmake --graphviz=dep.dot -S . -B WebKitBuild/GTK/Release && grep -i rice dep.dot
```

## 我具体怎么对比"你的 vs Playwright 的"

- 你的:有源码 + 构建目录 → 配置期查 CMakeCache.txt,产物查 readelf/nm,系统查 pkg-config/ldconfig。三层都能看。
- Playwright 的:我手里只有你下载的 bundle 二进制(没源码、没 CMakeCache)→ 只能对产物"验尸",多证据交叉:
  - a. readelf -d → 无 rice NEEDED(不是动态依赖)
  - b. nm -D → rice_ = 0(没这套符号)
  - c. strings → rtc::/webrtc/ 命中 500+(静态链了 libwebrtc),webrtcbin/GStreamerIceAgent = 0(没走 GStreamerWebRTC)
  - d. ls sys/lib + gstreamer-1.0/ → 无 librice、无 webrtc/nice/dtls 插件(dlopen 层也没有)
  - e. ls -lh 99M → 静态 libwebrtc 的旁证

五条独立证据指向同一结论:

> 官方 = 静态 libwebrtc;你 = 动态 librice + GStreamerWebRTC。

单看 ldd 会得出"官方没 WebRTC"的错误结论 —— 这就是为什么要三类工具一起上。



# pkg-config

## 查看包信息查找位置
- PKG_CONFIG_PATH：pkg-confi搜索路径变量

pkg-config --variable pc_path pkg-config

/usr/local/lib/x86_64-linux-gnu/pkgconfig 
/usr/local/lib/pkgconfig
/usr/local/share/pkgconfig 
/usr/lib/x86_64-linux-gnu/pkgconfig 
/usr/lib/pkgconfig 
/usr/share/pkgconfig

- 通常大多数在/usr/lib/x86_64-linux-gnu/pkgconfig
	- 小部分在/usr/share/pkgconfig

## 查看系统有哪些包
`pkg-config --list-all`

## 获取编译参数

`pkg-config --cflags gtk+-3.0`
`-I/usr/include/gtk-3.0 -I/usr/include/pango-1.0 -I/jhbuild/install/include/glib-2.0 -I/jhbuild/install/lib/glib-2.0/include -I/jhbuild/install/include/sysprof-6 -I/jhbuild/install/include/harfbuzz -I/usr/include/freetype2 -I/usr/include/libpng16 -I/usr/include/fribidi -I/usr/include/cairo -I/usr/include/pixman-1 -I/usr/include/gdk-pixbuf-2.0 -I/usr/include/x86_64-linux-gnu -I/usr/include/webp -I/jhbuild/install/include/gio-unix-2.0 -I/usr/include/atk-1.0 -I/usr/include/at-spi2-atk/2.0 -I/usr/include/at-spi-2.0 -I/usr/include/dbus-1.0 -I/usr/lib/x86_64-linux-gnu/dbus-1.0/include -pthread`

`pkg-config --cflags rice-io`
`-I/usr/include/rice`

--- 

`pkg-config --libs gtk+-3.0`
`-lgtk-3 -lgdk-3 -lz -L/jhbuild/install/lib -lpangocairo-1.0 -lpango-1.0 -lharfbuzz -latk-1.0 -lcairo-gobject -lcairo -lgdk_pixbuf-2.0 -lgio-2.0 -lgobject-2.0 -lglib-2.0`

`pkg-config --libs rice-io` 
`-lrice-io -lrice-proto`

静态依赖
`pkg-config --static --libs` 


## 查看版本

`pkg-config --modversion gtk+-3.0`  3.24.41

`pkg-config --modversion rice-io`   0.2.1


## 判断是否存在
`pkg-config --exists gtk+-3.0`
`echo $?`  0/1

## 查看依赖关系
`pkg-config --print-requires gtk+-3.0`
`gdk-3.0 atk >= 2.35.1 cairo >= 1.14.0 cairo-gobject >= 1.14.0 gdk-pixbuf-2.0 >= 2.30.0 gio-2.0 >= 2.57.2`