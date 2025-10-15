# go get
- `-u` 表示会讲package以及其依赖更新到最新的minor/patch
	- 这个比较坑爹，如果某个依赖进进行了API变动却没有更新major版本，导致更新到这个API不兼容版本，导致无法编译
- `package@latest`才是更新到最新版本