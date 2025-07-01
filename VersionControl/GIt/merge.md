任何merge都会发生冲突，冲突都是一样的问题。
# git merge
- merge mode
	- 
- 将自己的追加到目标分支后面：`git pull --rebase | git fetch && git rebase origin/branchNmae`
	- 可以rebase到远程分支，然后修改冲突，最后类似于amend，可以修改message。自己的commit仍然是最新的
	- 或者 `git stash -u`（将staged缓存，`-u`表示untrack也缓存）
		- 然后`git pull --rebase`进行pull，再`git stash pop`（弹出最新stash，可能会导致冲突需要解决）

# git cherry-pick
- 只提起指定commit范围追加到当前分支后面，不过一定要在本地，远程要先拉到本地。
- `git cherry-pick <commit>`
- `git cherry-pick <start-commit>^..<end-commit>`