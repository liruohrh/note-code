
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
