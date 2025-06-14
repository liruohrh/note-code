# Channel

- 启动：ServerBootstrap， Bootstrap
- 注册事件循环组（EventLoopGroup）：可以当成线程池看待，n 个线程--Selector，默认是 2 倍的 CPU 核心数
	- NioEventLoopGroup（处理 IO），EpollEventLoopGroup，KQueueEventLoopGroup，DefaultEventLoopGroup（不处理 IO，执行普通任务）
	- EventLoopGroup 会用同一个 EventLoop 处理同一个 channel
	- 如果仅仅注册一个，那么这个 EventLoo 即负责 Accept 也负责 Write，Read
		- 所以一般最好注册 2 个 EventLoopGroup
			- 使用不同的 parentGroup 和 childGroup 可以根据不同的业务需求来对处理连接请求和处理客户端请求分别进行优化，从而提高性能。
			- 例如，对于爬虫类的应用程序，可能需要大量处理连接请求，但对于每个连接，实际上需要很少的处理时间。在这种情况下，可以使用一个只包含少量线程的 parentGroup 来处理连接请求，而使用一个包含大量线程的 childGroup 来处理客户端请求。这样可以提高服务器的并发连接数，以及处理客户端请求的吞吐量。
			- 相反，对于需要大量处理客户端请求的应用程序，可以使用一个包含大量线程的 parentGroup 来处理连接请求，而使用一个只包含少量线程的 childGroup 来处理客户端请求。这样可以保证客户端请求的快速响应，同时避免过多的连接请求线程占用系统资源。
			- 因此，Netty 允许传入不同的 parentGroup 和 childGroup，以满足不同的业务需求和性能优化要求。
- 添加 ChannelHandler

- **ChannelInitializer**：在初始化时调用
	- 一般用这个，在 initChannel 方法中向 channel 的执行链**ChannelPipeline**中加 handler（可以指定 Header or Last， Before or After）
		- **ChannelOutboundHandler**：输出处理器（输出数据时）（使用 Adapter 自定义处理事件）
		- **ChannelInboundHandler** ：输入处理器（接收到数据时）（使用 Adapter 自定义处理事件）
		- 比如**StringDecoder**，**StringEncoder，LoggingHandler**
	- **ChannelInboundHandlerAdapter**：
		- super.channelRead(ctx, msg); **唤醒下一个 handler 进行处理**，实际是调用 ChannelHandlerContext 的方法，否则不会继续下去，其他方法和**ChannelOutboundHandlerAdapter**也是，调用原方法
	- **Out 是倒序执行，In 是顺序执行，都在一个双向链表上**
		- **使用**NioSocketChannel 的 write 是从尾巴开始执行，ChannelHandlerContext 的 write 是从当前的**In**开始执行，最后一个 In 有调用 write 操作（ctx.channel().writeAndFlush ，就是 initChannel 的 channel）才会执行 Out
	- 在 ChannelPipeline 的 handler 中发送的异常会给下游 handler 捕获如果有设置的话（捕获到就不会继续传递了）
		- 而且 handler 的异常要使用 ctx.fireExceptionCaught()传递，不然就会被当前 handler 的 exceptionCaught（对方关闭会在第一个重写 exceptionCaught 方法的 hanlder 的 exceptionCaught 里捕获）捕获，并且关闭 socket
	- handler 可以使用不同的 EventLoopGroup

- 客户端的 connect 或者服务端的 bind，都会返回一个 channelFuture 即是异步操作
	- 如果客户端想等连接完成后再执行方法，得先调用 sync 阻塞，其他方法不会阻塞
	- 也可以对 channelFutrue 使用 addListener 来进行操作
- 关闭 channel 后要做什么也需要 channelFuture.closeFuture()异步操作

# Future,Promise

在异步处理时，经常用到这两个接口

首先要说明 netty 中的 Future 与 jdk 中的 Future 同名，但是是两个接口，netty 的 Future 继承自 jdk 的 Future，而 Promise 又对 netty Future 进行了扩展

- jdk Future 只能同步等待任务结束（或成功、或失败）才能得到结果
- netty Future 可以同步等待任务结束得到结果，也可以异步方式得到结果，但都是要等任务结束
- netty Promise 不仅有 netty Future 的功能，而且脱离了任务独立存在，只作为两个线程间传递结果的容器

| **功能/名称** | **jdk Future**                 | **netty Future**                                                | **Promise**  |
| :------------ | :----------------------------- | :-------------------------------------------------------------- | :----------- |
| cancel        | 取消任务                       | -                                                               | -            |
| isCanceled    | 任务是否取消                   | -                                                               | -            |
| isDone        | 任务是否完成，不能区分成功失败 | -                                                               | -            |
| get           | 获取任务结果，阻塞等待         | -                                                               | -            |
| getNow        | -                              | 获取任务结果，非阻塞，还未产生结果时返回 null                   | -            |
| await         | -                              | 等待任务结束，如果任务失败，不会抛异常，而是通过 isSuccess 判断 | -            |
| sync          | -                              | 等待任务结束，如果任务失败，抛出异常                            | -            |
| isSuccess     | -                              | 判断任务是否成功                                                | -            |
| cause         | -                              | 获取失败信息，非阻塞，如果没有失败，返回 null                   | -            |
| addLinstener  | -                              | 添加回调，异步接收结果                                          | -            |
| setSuccess    | -                              | -                                                               | 设置成功结果 |
| setFailure    | -                              | -                                                               | 设置失败结果 |

# ByteBuf

- 有池化实现（4.1 后默认池化）和非池化（VM 参数控制：-Dio.netty.allocator.type={unpooled|pooled}）
  - 可以重用池中 ByteBuf 实例，并且采用了与 jemalloc 类似的内存分配算法提升分配效率
- 使用 ByteBufAllocator.DEFAULT 创建直接内存或者堆内存
- 优势
  - 池化 - 可以重用池中 ByteBuf 实例，更节约内存，减少内存溢出的可能
  - 读写指针分离，不需要像 ByteBuffer 一样切换读写模式
  - 可以自动扩容
  - 支持链式调用，使用更流畅
  - 很多地方体现零拷贝，例如 slice、duplicate、CompositeByteBuf

## 方法

- writeBoolean：0 或者 1
- writeInt：大端（网络传输，默认习惯是 Big Endian）
- writeIntLE：小端
-  get 开头的一系列方法，这些方法不会改变 read index

## 容量

- 默认256
- 小于512：按16的倍数扩容，16，64，128，256，512=2^9
- 大于512：按2的n次方扩容，2^10=1024，2^11=2048

## retain & release

由于 Netty 中有堆外内存的 ByteBuf 实现，堆外内存最好是手动来释放，而不是等 GC 垃圾回收。

- **UnpooledHeapByteBuf** 使用的是 JVM 内存，只需等 GC 回收内存即可
- **UnpooledDirectByteBuf** 使用的就是直接内存了，需要特殊的方法来回收内存
- **PooledByteBuf** 和它的子类使用了池化机制，需要更复杂的规则来回收内存

回收内存的源码实现，请关注下面方法的不同实现

protected abstract void deallocate()

Netty 这里采用了引用计数法来控制回收内存，每个 ByteBuf 都实现了 **ReferenceCounted** 接口**或者使用 ReferenceCountUtil**

- 每个 ByteBuf 对象的初始计数为 1
- 调用 **release** 方法计数减 1，如果计数为 0，ByteBuf 内存被回收
- 调用 **retain** 方法计数加 1，表示调用者没用完之前，其它 handler 即使调用了 release 也不会造成回收
- 当计数为 0 时，底层内存会被回收，这时即使 ByteBuf 对象还在，其各个方法均无法正常使用

谁来负责 release 呢？

不是我们想象的（一般情况下）

```java
ByteBuf buf = ...
 try {
     ...
 } finally {
     buf.release();
 }
```

请思考，因为 pipeline 的存在，一般需要将 ByteBuf 传递给下一个 ChannelHandler，如果在 finally 中 release 了，就失去了传递性（当然，如果在这个 ChannelHandler 内这个 ByteBuf 已完成了它的使命，那么便无须再传递）

基本规则是，**谁是最后使用者，谁负责 release**，详细分析如下

- 起点，对于 NIO 实现来讲，在 io.netty.channel.nio.AbstractNioByteChannel.NioByteUnsafe#read 方法中首次创建 ByteBuf 放入 pipeline（line 163 pipeline.fireChannelRead(byteBuf)）
- 入站 ByteBuf 处理原则
  - 对原始 ByteBuf 不做处理，调用 ctx.fireChannelRead(msg) 向后传递，这时**无须 release**
  - 将原始 ByteBuf 转换为其它类型的 Java 对象，这时 ByteBuf 就没用了，**必须 release**
    - 如果不调用 ctx.fireChannelRead(msg) 向后传递，那么也**必须 release**
  - 注意各种异常，如果 ByteBuf 没有成功传递到下一个 ChannelHandler，**必须 release**
  - 假设消息一直向后传，那么 **TailContext** 会负责释放未处理消息（原始的 ByteBuf）
- 出站 ByteBuf 处理原则
  - 出站消息最终都会转为 ByteBuf 输出，一直向前传，由 **HeadContext flush 后 release**
  - 无论是 ctx 写还是 channel 写，msg 如果没释放，都会在 HeadContext flush 后 release
- 异常处理原则
  - 有时候不清楚 ByteBuf 被引用了多少次，但又必须彻底释放，可以循环调用 release 直到返回 true

TailContext 释放未处理消息逻辑

```java
// io.netty.channel.DefaultChannelPipeline#onUnhandledInboundMessage(java.lang.Object)
 protected void onUnhandledInboundMessage(Object msg) {
     try {
         logger.debug(
             "Discarded inbound message {} that reached at the tail of the pipeline. " +
             "Please check your pipeline configuration.", msg);
     } finally {
         ReferenceCountUtil.release(msg);
     }
 }
```

具体代码

```java
// io.netty.util.ReferenceCountUtil#release(java.lang.Object)
 public static boolean release(Object msg) {
     if (msg instanceof ReferenceCounted) {
         return ((ReferenceCounted) msg).release();
     }
     return false;
 }
```

## slice

- 【零拷贝】的体现之一，对原始 ByteBuf 进行切片成多个 ByteBuf，切片后的 ByteBuf 并没有发生内存复制，还是使用原始 ByteBuf 的内存，切片后的 ByteBuf **维护独立的 read，write 指针**
- 默认的 slice 是（readIndex，writeIndex-readIndex）或者（index，len）
  - slice 可以修改，但不能添加，capacity 为 writeIndex-readIndex 或者 len
  - 原始的被释放了，slice 当然也用不了了，但是如果对 slice 对象使用 retain 方法后就不会被影响，但是需要自己释放

## duplicate

【零拷贝】的体现之一，就好比截取了原始 ByteBuf 所有内容，并且没有 max capacity 的限制，也是与原始 ByteBuf 使用同一块底层内存，只是读写指针是独立的

## copy

会将底层内存数据进行深拷贝，因此无论读写，都与原始 ByteBuf 无关

## CompositeByteBuf

【零拷贝】的体现之一，可以将多个 ByteBuf 合并为一个逻辑上的 ByteBuf，避免拷贝

- `ByteBufAllocator.DEFAULT.buffer(buf1.readableBytes()+buf2.readableBytes());//会拷贝数据`
- `CompositeByteBuf buf3 = ByteBufAllocator.DEFAULT.compositeBuffer();  buf3.addComponents(true, buf1, buf2);  // true 表示增加新的 ByteBuf 自动递增 write index, 否则 write index 会始终为 0`
- 优点，对外是一个虚拟视图，组合这些 ByteBuf 不会产生内存复制
- 缺点，复杂了很多，多次操作会带来性能的损耗

## Unpooled

- Unpooled 是一个工具类，类如其名，提供了非池化的 ByteBuf 创建、组合、复制等操作
  - 这里仅介绍其跟【零拷贝】相关的 wrappedBuffer 方法，可以用来包装 ByteBuf
- `ByteBuf buf3 = Unpooled.wrappedBuffer(buf1, buf2); // 当包装 ByteBuf 个数超过一个时, 底层使用了 CompositeByteBuf`
