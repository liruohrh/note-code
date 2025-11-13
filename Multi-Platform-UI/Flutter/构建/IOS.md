# 最低IOS版本设置
- https://blog.csdn.net/wsyx768/article/details/136319899
- 在ios目录搜索，替换IPHONEOS_DEPLOYMENT_TARGET的值
- 也许还需要`/ios/Runner/Info.plist`
```xml
<key>MinimumOSVersion</key>
<string>13.0</string>
```