# git init
- `git init <directory>`
- `<directory>`默认当前目录
- `--bare`创建bare仓库
- `-b,initial-branch=<branch-name>`：默认master

# git clone
- `git clone <repository> [<directory>]`
- `<directory>`默认仓库名
- `--bare`创建bare仓库
- `-o <reponame>`替换默认的track upstream的name=origin
- `-b | --branch <branchname | commit | tag>`指定分支或者commit或者tag
- `--single-branch`仅克隆一条分支
- `-n, --no-checkout`参数是为了告诉 Git 不要立即检出工作目录，以免下载所有文件。
- `--filter=blob:none` 表示过滤所有blob（文本文件）
- `filter=blob:limit=<size>`过滤大小为size的blob
	- 更多看`git rev-list`
	- 可能会失效，据说2.19.1才行，还不如用`--sparse`
- `--sparse`
	- `git sparse-checkout init`
	- 详细看sparse checkout
- `--depth n` 表示只下载最近的n次提交

# git status
- 显示
	- 未跟踪（untracked）：Untracked files
	- 暂存未提交（staged &&unCommit）：Changes to be committed
		- 只在暂存区，不在版本库
	- 修改未暂存（modified && unStaged）：Changes not staged for commit
		- 对staged/commited的文件modified
	- 被忽视的（Ignored）：Ignored files
- option
	- `-s`：显示文件状态标识
		- ??：untracked
		- A：new File
		- M：modified
		- U: untracked

# git add
- `git add <pathspec>...`
- 暂存文件，`.`表示所有
# git rm 
- `git rm <file>...`
	- 无法对未跟踪的文件操作
	- 默认删除工作区、暂存文件（文件是最新状态，未被修改）
	- 等于`rm xxx && git add xxx`
- `--cached`：只删除在暂存文件的，如果没有该选项，则会和工作区的一起删了
- `-r`：递归删除目录
- `-f`： `override the up-to-date check`，即modifed的文件也能删除（强制删除）
## 彻底删除的方法
- 

# git restore

- `-S, --staged`：暂存区恢复HEAD
- `-W, --worktree`：工作区恢复HEAD（默认）

# git mv
- 移动文件，或者，重命名文件
- 相当于
	- mv a b
	- git rm a
	- git add b
- 最后，commit即可，工作区也会rename

# git commit
- `git commit <path-spec>`
- 进行commit，
- -m：指定message
- --amend：用新commit覆盖当前commit
	- 如果之前推送过远程，再推送远程时需要-f，因为远程的头commit和当前不一样了
# git log
- --graph：类图形化显示commit合并情况
- --oneline：一行显示（简化提交信息）
- --all：所有commit
# git checkout
- `git checkout`切换分支或者恢复修改（这里只看恢复修改，类似于`git reset`）

- checkout 本意是检出的意思，也就是将某次commit的状态检出到工作区；所以它的过程是先将HEAD指向某个分支的最近一次commit，然后从commit恢复index，最后从index恢复工作区。
- 恢复修改
	- 如果不指定切换到哪个分支，那就是切换到当前分支，虽然HEAD的指向没有变化，但是后面的两个恢复过程依然会执行，于是就可以理解为放弃index和工作区的变动。但是出于安全考虑 git 会保持 index 的变动不被覆盖。
	- `git checkout .`恢复工作区（只是把index恢复到工作区，比如会让修改未重新暂存变回原来内容）
		- `git checkout -- f1 f2`指定文件恢复
		- 等于`git restore .` `git restore f1 f2`
	- `git checkout -f`恢复工作区和index即和正常的切换分支一样恢复到该分支最新提交


# git diff
- 比较的是工作目录中当前文件和暂存区域快照之间的差异（如果修改了就是修改之后还没有暂存起来的变化内容）
	- 注意：commied后的文件在暂存区还存在
	- 变化
		- 绿色表示增加的，红色表示删除的
		- @@@@里表示 减了多少行，加了多少行，目前这个改变的有多少行
	- 如果指定文件，就把工作区的所有文件都拿出来比较
- option
	- --staged，或者，--cached
		- 比对已暂存文件与最后一次提交的文件差异
	- git diff HEAD
		- 和HEAD版本对比

