- https://juejin.cn/post/7287914073315360823
- 拉跨的玩意，不能卸载指定版本，安装不同版本有问题（特别是本地manifest，指定了本地的manifest居然还用bucket中的），全用ps脚本写

# 安装

```ps1
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
irm get.scoop.sh -outfile 'install.ps1'
.\install.ps1 -ScoopDir 'D:\software\scoop' -ScoopGlobalDir 'D:\software\scoopg
```

```
--apps
----$appname
------$version 版本号
------current  当前使用版本的链接
--buckets 仓库目录
--cache 安装后的压缩包等缓存
--modules ps的模块
--persist 保留目录，让app的指定persist目录链接到这个目录下的$appname目录下，以便共享目录
--shims
--workspace 安装指定版本时会根据app的manifest创建这个版本的manifest
```

# 下载app
- `scoop install appname`
- 安装的目录中会自动含一个manifest.json文件，就是针对这个版本的manifest文件
- 默认不会自动删除压缩包等缓存，删除缓存命令：`scoop cache rm *`
```ps1
Usage: scoop install <app> [options]

e.g. The usual way to install an app (uses your local 'buckets'):
     scoop install git

To install a different version of the app
(note that this will auto-generate the manifest using current version):
     scoop install gh@2.7.0
#会自动创建或者更新`$SCOOP/workspace/$appname.json`


#json文件名就是软件名，即appname，如果指定app的manifest文件进行安装，更新时仍然使用这个

To install an app from a manifest at a URL:
     scoop install https://raw.githubusercontent.com/ScoopInstaller/Main/master/bucket/runat.json

To install a different version of the app from a URL:
      scoop install https://raw.githubusercontent.com/ScoopInstaller/Main/master/bucket/neovim.json@0.9.0

To install an app from a manifest on your computer
     scoop install \path\to\app.json

To install an app from a manifest on your computer
     scoop install \path\to\app.json@version

Options:
  -g, --global                    Install the app globally
  -i, --independent               Don't install dependencies automatically
  -k, --no-cache                  Don't use the download cache
  -s, --skip-hash-check           Skip hash validation (use with caution!)
  -u, --no-update-scoop           Don't update Scoop before installing if it's outdated
  -a, --arch <32bit|64bit|arm64>  Use the specified architecture, if the app supports it
```

# 卸载、清理
-  `scoop uninstall`卸载所有版本、`scoop cleanup`保留最新下载的版本（不是通过版本号）

# 版本切换
- `scoop reset app@version`
- `scoop reset app`切换到最新

# Bucket
- 就是一个软件包，必须为git仓库
- 默认官方的main，还可以添加versions（含更多版本的仓库）
- https://scoop.sh/#/buckets

## 创建app的manifest文件
- `scoop create <url>`
- 无arch检查的manifest直接用url、hash、extract_dir等属性，有则写在architecture

### nodejs的manifest
```json
{
    "version": "22.15.0",
    "description": "An asynchronous event driven JavaScript runtime designed to build scalable network applications.",
    "homepage": "https://nodejs.org",
    "license": "MIT",
    "architecture": {
        "64bit": {
            "url": "https://nodejs.org/dist/v22.15.0/node-v22.15.0-win-x64.7z",
            "hash": "45471a4f77cdaacce971ab7a6698659ed872606f7b4b0aecdfe5689627134cb2",
            "extract_dir": "node-v22.15.0-win-x64"
        },
        "arm64": {
            "url": "https://nodejs.org/dist/v22.15.0/node-v22.15.0-win-arm64.7z",
            "hash": "d0615f16a280f4660a6c83d472a0b2e72122e47f4c82754a5ed950d54d0cbe3d",
            "extract_dir": "node-v22.15.0-win-arm64"
        }
    },
    //在reset时保留目录bin、cache
    "persist": [
        "bin",
        "cache"
    ],
    //添加到PATH变量的目录，bin属性则是文件
    "env_add_path": [
        "bin",
        "."
    ],
    //安装前执行，以下命令是在安装后更新npmrc，指定npm的prefix和cahce
    "post_install": [
        "# Set npm prefix to install modules inside bin and npm cache so they persist",
        "Set-Content -Value \"prefix=$persist_dir\\bin`ncache=$persist_dir\\cache\" -Path \"$dir\\node_modules\\npm\\npmrc\""
    ],
    //版本检查，nodejs的网站通常不包含比较旧的，如14.x.x
    "checkver": {
        "url": "https://nodejs.org/dist/index.json",
        "jsonpath": "$[0].version",
        "regex": "v([\\d.]+)"
    },
    //支持自动更新，支持app@version安装app，会自动创建或者更新`$SCOOP/workspace/$appname.json`
    "autoupdate": {
        "architecture": {
            "64bit": {
                "url": "https://nodejs.org/dist/v$version/node-v$version-win-x64.7z",
                "extract_dir": "node-v$version-win-x64"
            },
            "arm64": {
                "url": "https://nodejs.org/dist/v$version/node-v$version-win-arm64.7z",
                "extract_dir": "node-v$version-win-arm64"
            }
        },
        "hash": {
            "url": "$baseurl/SHASUMS256.txt.asc"
        }
    }
}
```

### 使用本地安装的仿nodejs
```json
{
    "version": "20.10.0",
    "description": "An asynchronous event driven JavaScript runtime designed to build scalable network applications.",
    "homepage": "https://nodejs.org",
    "license": "MIT",
    "url": "file:///D:/software/dev/SDK/nodejs-v20.10.0-win-x64.7z",
    "extract_dir": "nodejs-v20.10.0-win-x64",
    "persist": [
        "bin",
        "cache"
    ],
    "env_add_path": [
        "bin",
        "."
    ],
    "post_install": [
        "# Set npm prefix to install modules inside bin and npm cache so they persist",
        "Set-Content -Value \"prefix=$persist_dir\\bin`ncache=$persist_dir\\cache\" -Path \"$dir\\node_modules\\npm\\npmrc\""
    ],
    "checkver": {
        "url": "file:///D:/software/scoop/mylocal/bucket/nodejs.version.json",
        "jsonpath": "$[0].version"
    },
    "autoupdate": {
        "url": "file:///D:/software/dev/SDK/nodejs-v$version-win-x64.7z",
        "extract_dir": "nodejs-v$version-win-x64"
    }
}
```

```json
[
    {
        "version": "14.21.3"
    },
    {
        "version": "16.20.2"
    },
    {
        "version": "20.10.0"
    }
]
```