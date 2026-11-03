
x11服务器负责渲染，x客户端（虚拟桌面）发送画图指令。
x11vnc会把x11服务器放在虚拟桌面位置并渲染，vnc客户端（远程连接App）则是显示图片，
否则，客户端是使用x11服务器进行渲染，接收x客户端请求。
简单来说，就是x11vnc是服务端渲染，x11服务器是客户端渲染。

虚拟桌面->x11服务器->vnc直接在宿主机渲染->vnc客户端（用户远程控制）。

创建虚拟桌面：xvfb
启动x服务器宿主机绘图：x11vnc
Xvnc（TigerVNC） = xvfb + x11vnc
连接vnc服务器：tigervnc-viewer



- 端口转发：`ssh -L [localaddr:]port:remoteadd:port target` 
  - 注意，这个ssh终端会照常打开，可以不用管

