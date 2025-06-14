```java
@Component
public class NettyBootsrapRunner implements ApplicationRunner, ApplicationListener<ContextClosedEvent>, ApplicationContextAware {

	private static final Logger LOGGER = LoggerFactory.getLogger(NettyBootsrapRunner.class);
	
	@Value("${netty.websocket.port}")
	private int port;

	@Value("${netty.websocket.ip}")
	private String ip;
	
	@Value("${netty.websocket.path}")
	private String path;
	
	@Value("${netty.websocket.max-frame-size}")
	private long maxFrameSize;
	
	private ApplicationContext applicationContext;
	
	private Channel serverChannel;
	
	public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
		this.applicationContext = applicationContext;
	}
	
	public void run(ApplicationArguments args) throws Exception {
		
		EventLoopGroup bossGroup = new NioEventLoopGroup();
		EventLoopGroup workerGroup = new NioEventLoopGroup();
		try {
			ServerBootstrap serverBootstrap = new ServerBootstrap();
			serverBootstrap.group(bossGroup, workerGroup);
			serverBootstrap.channel(NioServerSocketChannel.class);
			serverBootstrap.localAddress(new InetSocketAddress(this.ip, this.port));
			serverBootstrap.childHandler(new ChannelInitializer<SocketChannel>() {
				@Override
				protected void initChannel(SocketChannel socketChannel) throws Exception {
					ChannelPipeline pipeline = socketChannel.pipeline();
					pipeline.addLast(new HttpServerCodec());
					pipeline.addLast(new ChunkedWriteHandler());
					pipeline.addLast(new HttpObjectAggregator(65536));
					pipeline.addLast(new ChannelInboundHandlerAdapter() {
						@Override
						public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
							if(msg instanceof FullHttpRequest) {
								FullHttpRequest fullHttpRequest = (FullHttpRequest) msg;
								String uri = fullHttpRequest.uri();
								if (!uri.equals(path)) {
									// 访问的路径不是 websocket的端点地址，响应404
									ctx.channel().writeAndFlush(new DefaultFullHttpResponse(HttpVersion.HTTP_1_1, HttpResponseStatus.NOT_FOUND))
										.addListener(ChannelFutureListener.CLOSE);
									return ;
								}
							}
							super.channelRead(ctx, msg);
						}
					});
					pipeline.addLast(new WebSocketServerCompressionHandler());
					pipeline.addLast(new WebSocketServerProtocolHandler(path, null, true, maxFrameSize));

					/**
					 * 从IOC中获取到Handler
					 */
					pipeline.addLast(applicationContext.getBean(WebsocketMessageHandler.class));
				}
			});
			Channel channel = serverBootstrap.bind().sync().channel();	
			this.serverChannel = channel;
			LOGGER.info("websocket 服务启动，ip={},port={}", this.ip, this.port);
			channel.closeFuture().sync();
		} finally {
			bossGroup.shutdownGracefully();
			workerGroup.shutdownGracefully();
		}
	}

	public void onApplicationEvent(ContextClosedEvent event) {
		if (this.serverChannel != null) {
			this.serverChannel.close();
		}
		LOGGER.info("websocket 服务停止");
	}
}
```