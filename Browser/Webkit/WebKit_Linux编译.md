- 使用环境：https://github.com/Igalia/webkit-container-sdk
- 版本查看 Source/cmake/OptionsGTK.cmake  SET_PROJECT_VERSION
- `about:minibrowser  about:data   about:itp ` 

# webkitgtk官方编译的
https://web-platform-tests.org/running-tests/webkitgtk_minibrowser.html
https://webkitgtk.org/built-products/x86_64/release/beta/MiniBrowser
- sudo apt install webkit2gtk-driver
- /usr/lib/x86_64-linux-gnu/webkit2gtk-4.1/MiniBrowser
- 其实下载libwebkit2gtk-4.1-0即可，此包才是MiniBrowser


```
Package: webkit2gtk-driver
Version: 2.52.3-0ubuntu0.24.04.1
Priority: optional
Section: universe/web
Source: webkit2gtk
Origin: Ubuntu
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Original-Maintainer: Debian WebKit Maintainers <pkg-webkit-maintainers@lists.alioth.debian.org>
Bugs: https://bugs.launchpad.net/ubuntu/+filebug
Installed-Size: 2,031 kB
Depends: libwebkit2gtk-4.1-0 (= 2.52.3-0ubuntu0.24.04.1), libatomic1 (>= 4.8), libc6 (>= 2.38), libgcc-s1 (>= 3.0), libglib2.0-0t64 (>= 2.40.0), libicu74 (>= 74.1-1~), libsoup-3.0-0 (>= 3.0.3), libstdc++6 (>= 12), libsystemd0, zlib1g (>= 1:1.1.4)
Conflicts: webkitgtk-webdriver
Homepage: https://webkitgtk.org/
Download-Size: 562 kB
APT-Manual-Installed: yes
APT-Sources: http://security.ubuntu.com/ubuntu noble-security/universe amd64 Packages
Description: WebKitGTK WebDriver support
 WebKit is a web content engine, derived from KHTML and KJS from KDE, and
 used primarily in Apple's Safari browser.  It is made to be embedded in
 other applications, such as mail readers, or web browsers.
 .
 It is able to display content such as HTML, SVG, XML, and others. It also
 supports DOM, XMLHttpRequest, XSLT, CSS, JavaScript/ECMAScript and more.
 .
 WebKitGTK is a WebKit port designed to be used in GTK applications.
 .
 This package provides the WebDriver service implementation for
 WebKitGTK.
```


# Feb 13, 2026 webkit 6b34ac51510516bd6a3ec2f5edc97413758d3ab1

---

webkit-container-sdk：May 30, 2026 be706e12c64766031de783b11219026c2c2b93c6

---
修改
- 将librice 改为v0.2.1

手动更新环境的方法
```bash
git clone https://github.com/ystreet/librice
cd librice
git checkout v0.2.1

TRIPLE=$(gcc -dumpmachine)
SUDO_ENV='sudo env PATH=/opt/rust/bin:/usr/local/bin:/usr/bin:/bin RUSTUP_HOME=/opt/rust CARGO_HOME=/opt/rust RUSTUP_TOOLCHAIN=1.94.0'
$SUDO_ENV cargo cinstall -p rice-proto --release --prefix=/usr --libdir=lib/$TRIPLE --library-type=cdylib
$SUDO_ENV cargo cinstall -p rice-io   --release --prefix=/usr --libdir=lib/$TRIPLE --library-type=cdylib

# 清旧版残留 + 刷链接缓存   
# 因为webkit不指定库的版本，要避免用到其他版本
sudo rm -f /usr/lib/$TRIPLE/librice-*.so.0.4.3
sudo ldconfig
# 验证
pkg-config --modversion rice-proto          # 应为 0.2.1
grep -n rice_turn_config_ref /usr/include/rice/rice-proto.h   # 应能找到
```


