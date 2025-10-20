# wsl docker部署
- 无法使用，因为21116需要udp，而wsl还不能映射udp到windows
- 如果使用 [Unix Utils ported to Windows - Browse /socat/1.7.3.2 at SourceForge.net](https://sourceforge.net/projects/unix-utils/files/socat/1.7.3.2/) 转发upd `socat UDP4-LISTEN:21116,fork UDP4:$WSL_IP:21116`
	- 则客户端连接成功，但是远程连接失败
- 在windows部署则成功[WINDOWS & PM2 或者 NSSM – RustDesk文档](https://rustdesk.com/docs/zh-cn/self-host/rustdesk-server-oss/windows/#%e4%bd%bf%e7%94%a8-nssm-%e5%ae%89%e8%a3%85)
	- 不过，不知道为什么服务端的客户端仍然没有连接成功且是正确的key，另一个客户端连接成功且是错误的key，此刻仍然可以远程连接另一个客户端成功？？？
````
## docker-compose.yml
```yml
services:
  hbbs:
    container_name: hbbs
    image: rustdesk/rustdesk-server:latest
    command: hbbs
    volumes:
      - ./data:/root
    ports:
      - "21115:21115"
      - "21116:21116/tcp"
      - "21116:21116/udp"
      - "21118:21118"
    restart: unless-stopped
    depends_on:
      - hbbr

  hbbr:
    container_name: hbbr
    image: rustdesk/rustdesk-server:latest
    command: hbbr
    volumes:
      - ./data:/root
    ports:
      - "21117:21117"
      - "21119:21119"
    restart: unless-stopped
```