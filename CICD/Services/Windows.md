
# Task Schedule


# Service
- https://github.com/winsw/winsw
	- 仅XML、YAML配置文件
	- 使用方式很别扭，必须将配置文件与winsw可执行文件同名且同目录
	- 应用程序名、winsw可执行文件名、winsw文件名，有一个改变了路径都得重新安装
		- 应该是只要服务id、name有一个不变即可
		- 本质上就是winsw本身作为服务注册，应用以winsw子进程的方式启动
- https://github.com/kirillkovalenko/nssm
	- 仅GUI配置



## winsw
- 时间+大小轮转实现有bug，必须在设定时间后才会轮转，推荐仅用时间轮转
- 如果依赖其他服务，要设置depend，除非服务会尝试一定时间的自动重试
- 启动时，可能读取到错误的时间（好像只是0点），可以尝试设置delayedAutoStart，或者尝试程序手动一定延时

```xml
<service>
    <!-- 服务 ID 和显示名称 -->
    <id>ServiceId</id>
    <name>Service Name</name>
    <description>Service description</description>

    <!-- 可执行文件和工作目录 -->
    <executable>D:\path\app.exe</executable>
    <workingdirectory>D:\ws</workingdirectory>
    <stoptimeout>30 sec</stoptimeout>
    
    <delayedAutoStart>true</delayedAutoStart>  
	<depend>mysql</depend>

    <!-- 输出日志配置 -->
    <logpath>D:\path\logs\std</logpath>
    <logname>logFilename</logname> 
	<log mode="roll-by-size">  
		<sizeThreshold>10240</sizeThreshold> <!-- 单位 KB -->  
		<keepFiles>7</keepFiles>  
	</log>

    <!-- 崩溃自动重启 -->
    <onfailure action="restart" delay="5000" />
</service>
```