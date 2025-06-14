- Time-Base One-Time Password：基于密钥的时间密码算法
	- 一样的参数，在同一个时间段内会生成一样的字符串
		- 密钥、HmacHash算法
		- 结果长度
		- 计数器（时间段）：比如每30s一段就是 当前秒级时间/30s
- 原理：
	- Hash(Base32(计数器转为大端序字节数组))



- 一样的参数，可以在指定的时间间隔中生成一样的字符串
- Who use？
	- Google、微软等认证器
	- Github在2024强制要求Two-factor认证，就是用这个TOTP

```xml
<dependency>  
    <groupId>dev.samstevens.totp</groupId>  
    <artifactId>totp</artifactId>  
    <version>1.7.1</version>  
</dependency>
```