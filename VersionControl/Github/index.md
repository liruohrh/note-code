
# SSH

#git/ssh/github

---

- 无法连接时使用以下ssh配置
```conf
Host github.com
    HostName ssh.github.com
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/github
    # Port 443 #有无都可
    User git
    # 添加下面这一行，端口号为你开启代理的端口号，这里7890是Clash默认端口号
    # ProxyCommand connect -S 127.0.0.1:7890 -a none %h %p
```

