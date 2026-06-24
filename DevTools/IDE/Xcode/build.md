- File > Workspace Settings > Advances > Custom > Relative To Workspace，将 Products、Intermediates 放在同一目录。

# target 配置
- project配置是target配置默认值
- 添加设置：project > build settings > basic > add user defined setting
	- 或者定义 /Volumes/RedmibookOrigin/ws/WebKit/Source/WTF/Configurations/{target name}.xcconfig

# 查看配置
```bash
xcodebuild \
  -workspace /Volumes/RedmibookOrigin/ws/WebKit/WebKit.xcworkspace \
  -scheme "Everything up to MiniBrowser" \
  -configuration Debug \
  -showBuildSettings 2>/dev/null \
  | grep -E "ALLOW_CXX|SWIFT_OBJC_INTEROP_MODE|WK_SWIFT_EXPLICIT|SWIFT_ENABLE_EXPLICIT" \
  | sort -u
```


# 清理缓存
```bash
rm -rf {builddir}
# Clang/Swift 预编译模块缓存
rm -rf ~/Library/Developer/Xcode/DerivedData/ModuleCache.noindex
# Xcode 26 新增的编译产物缓存（对应构建日志里的 `-cache-compile-job -cas-path`），用来跨构建复用编译结果。
rm -rf ~/Library/Developer/Xcode/DerivedData/CompilationCache.noindex
```
- builddir默认：~/Library/Developer/Xcode/DerivedData/{ProjectName}-{uniqueId}