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

# apply+commit
git 



# 创建patch后，如果想恢复
git reset --hard HEAD
```


## clone

```bash
# 初始化
git init
git remote add upstream <url>
git fetch --depth 1 upstream <完整commit>
git checkout FETCH_HEAD
git checkout -b master

# 将这个commit之前的commit拉下来
git fetch --depth 9999999 upstream <完整commit>
# 不能下面这样，会把整个分支的commit都拉下来
# git fetch --unshallow upstream master


# 还是在这个分支，更新commit
git fetch --depth 9999999 upstream <完整commit>
git reset --hard <完整commit>
# 此时reset hard等于merge，只不过merge会提示本地修改冲突而已，但是此时的场景下是没有的，这个分支是干净的追踪分支
# git merge FETCH_HEAD



git checkout -b biz
# 更新master了，在biz中merge，只要master的新commit没有与当前冲突就没有冲突
git merge master
```