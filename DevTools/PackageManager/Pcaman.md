* `-S` = Sync：操作远程软件仓库（安装、升级、搜索等）
* `-Q` = Query：查询本地已安装的软件数据库
* `-R` = Remove：卸载软件包
* `-U` = Upgrade：安装本地软件包文件（如 `.pkg.tar.zst`）

---

* `-s` = Search / Recursive：搜索（如 `-Ss`、`-Qs`）；在 `-R` 中表示递归删除无用依赖（`-Rs`）
* `-i` = Info：查看软件包详细信息（`-Si`、`-Qi`）
* `-y` = Refresh：刷新软件仓库数据库
* `-u` = Upgrade：升级已安装的软件
* `-n` = No save：删除软件配置文件（与 `-R` 一起使用，如 `-Rns`）
