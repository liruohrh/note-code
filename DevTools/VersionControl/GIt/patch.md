- 用git的diff功能实现patch

# patch & apply

```bash
# 改完后
git diff > xxx.patch
# 指定文件/xxx
git diff -- xxx



# 应用patch
# 先检查是否能应用
git apply --check xxx.patch 
# 应用补丁 
git apply xxx.patch         



# 还原完整的commit信息
# 输出完整的commit以及diff
git format-patch -1 HEAD  #最近一个提交
# 应用mailbox patch
# -3=--3way, 在当前代码与patch冲突时采取尝试合并
git am -3 xxx.patch
# 表明验证者，在commit message末尾追加"Signed-off-by: Your Name <your@email.com>"
git am --signoff < xxx.patch



# 创建patch后，如果想恢复
git reset --hard HEAD
```


## clone

```bash
# 初始化
git init
git add remote origin <url>
git fetch --depth 1 origin <commit>
git checkout FETCH_HEAD
git checkout -b master

# 中途可以添加任意commit

# 升级，把从旧commit到指定commit给拉下来
git pull --rebase <commit>
```