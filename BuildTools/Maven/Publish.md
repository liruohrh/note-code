# Github
## Publish
- 根项目下，根标签下

```xml
<distributionManagement>
	<repository>
		<id>github</id>
		<name>GitHub OWNER Apache Maven Packages</name>
		<url>https://maven.pkg.github.com/liruohrh/spigot</url>
	</repository>
</distributionManagement>
```


- settings.xml
```xml
<servers>  
 <server>  
    <id>github</id>  
    <username>liruohrh</username>  
    <password>xxx</password>  
  </server>  
</servers>
```


## Install

```xml
<dependencies>  
  <dependency>  
    <groupId>io.github.stream29</groupId>  
    <artifactId>streamlin</artifactId>  
    <version>2.5.1</version>  
  </dependency>  
</dependencies>


<repository>  
  <id>github</id>  
  <url>https://maven.pkg.github.com/liruohrh/spigot</url>  
  <snapshots>  
    <enabled>true</enabled>  
  </snapshots>  
</repository>
```