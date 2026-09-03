
# 压缩服务器目录再解压到本地

```bash

# 压缩服务器目录再解压到本地指定路径
ssh user@host "tar -C dest -czf - targetDir" | tar -C . -xzf -

# 反过来压缩本地目录解压到服务器指定路径
tar -C dest -czf - targetDir | ssh user@host "tar -C . -xzf -"

```


# 批量ssh命令临时保存密码
```bash
TOKEN="scott@192.168.0.100"
# 定义 SSH 选项
SSH_OPTS="-o ControlMaster=auto -o ControlPath=/tmp/ssh_mux_%r@%h:%p -o ControlPersist=600"
# 先建立主连接并放入后台（首次输入密码）
ssh -N -f $SSH_OPTS $TOKEN


scp $SSH_OPTS "$TOKEN:$SERVER_ROOT/xxx" ./xxx
ssh $SSH_OPTS $TOKEN "xxx"
```