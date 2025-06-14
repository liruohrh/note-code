# 基础
## 增强型for循环

#bug/java/iterator #bug/java/concurrent

---
● 对实现Iterator的类用增强型for循环，如果容器元素的数量发生变化，Iterator感知不到，而Iterator里会有修改计数等判断，就会抛出ConcurrentModificationException

# IO
## 数据的读取

#bug/java/socket

---
- 读取Socket的流不能readall什么的，因为如果对方没有关闭该流或者通道未关闭是读不完的
	- 想不关闭又想读取对方发送的一次全部信息  
		- 因为流的方法会返回读取了多少字节，因此如果读的字节数>0就说明读到了，<=0就没有数据了
    