
# 同时写入文件和输出终端
```
type nul > output.log
start powershell -NoExit -Command "Get-Content output.log -Wait"
perl Tools/Scripts/build-webkit --release >> output.log 2>&1
```