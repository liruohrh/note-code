- 使用环境：https://github.com/Igalia/webkit-container-sdk
- 版本查看 Source/cmake/OptionsGTK.cmake  SET_PROJECT_VERSION
- `about:minibrowser  about:data   about:itp ` 

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

