#async/springboot


- 使用TaskExecutor#execute进行异步调用，需要配置bean=applicationTaskExecutor（askExecutionAutoConfiguration#APPLICATION_TASK_EXECUTOR_BEAN_NAME）
- 套娃式complete：ResponseBodyEmitter#complet、ResponseBodyEmitterReturnValueHandler.HttpMessageConvertingHandler#complete、ResponseBodyEmitter#complet
- `WebAsyncManager#setConcurrentResultAndDispatch`
	- 在执行异步请求时，会先结束普通请求的处理，会在WebAsyncManager设置一系列的拦截器处理如timeout等，最后会让AsyncRequest进行异步类型的dispatch
		- 就和普通的forward、include一样在ApplicationDispatcher重新执行一遍Servlet请求
		- dispatch只是创建一个Runnable，且执行`request.getCoyoteRequest().action(ActionCode.ASYNC_DISPATCH, null);`，ActionCode.ASYNC_DISPATCH：`org.apache.coyote.AbstractProcessor#processSocketEvent(SocketEvent.OPEN_READ, true)`
			- 会复用这个异步请求，但是会像新请求差不多走一遍org.apache.tomcat.util.net.AbstractEndpoint#processSocket（HTTP、Servlet容器）（使用Executor，即并发执行），但是会在原本执行filter并执行servlet的Value执行异步任务，使用异步请求进行异步dispatch。
				- 因此需要特别注意
		- 并在HandlerAdapter处理结果，创建额外的ConcurrentResultHandlerMethod处理
	- 需要特别注意一下Filter的配置，如果不支持异步又想支持，就FilterRegistrationBean#setDispatcherTypes（即便Filter是一个bean了，依然可以注册这个FilterRegistrationBean进行配置）
# 异步Dispath导致的问题--Shiro
像Shiro这逼货，包装了请求不说，还自动用SecurityManager创建Subject，而SecurityManager是线程绑定或者SecurityUtils静态变量（默认没有设置），线程绑定是肯定不能用了，因为是在其他线程执行的，使ShiroFilter支持异步（可以让认证Filter选择是否支持异步（可以避免再次解析），可以看看异步后的新请求需不需要认证信息，基本上都不需要），或者设置SecurityUtils静态变量（其实设置好像也没什么，因为Subject都是使用线程绑定的，也不知道为什么官方推出2种方式）（推荐第2种）
- 其实主要是因为调用了SecurityUtils#getSubject会在空时自动创建，在ShiroFilter创建使用的是注入的SecurityManager，而SecurityUtils#getSubject使用的是SecurityUtils#getSecurityManager