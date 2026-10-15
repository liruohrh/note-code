
# 软件索引仓库

```
#/etc/apt/sources.list.d/ubuntu.sources
Types: deb
URIs: http://tw.archive.ubuntu.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: http://security.ubuntu.com/ubuntu/
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

- Suite
	- noble：系统版本发布时的软件包仓库索引
	- noble-updates：软件的更新，版本比较新
	- noble-backports：向后移植版本，即新版本系统的软件移植到当前版本系统
	- noble-security：系统维护人员更新的安全版本软件

- 上面是2个源，分2个是为了分流
- apt默认用高版本，不主动用backports