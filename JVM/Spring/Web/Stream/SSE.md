#stream/sse
# ResponseBodyEmitterReturnValueHandler
- 处理ResponseBodyEmitter（SseEmitter）或者 ReactiveTypeHandler支持的Reactor的类型（如Flux）
- ReactiveTypeHandler：为不同类型实现了不同响应体的Reactor Subscription
	- 像ServerSentEvent是针对SSE的，仍然使用SseEmitter发送消息
	- 注意，在onNext（即消费）时，都会使用TaskExecutor#execute进行异步调用，需要配置bean=applicationTaskExecutor（askExecutionAutoConfiguration#APPLICATION_TASK_EXECUTOR_BEAN_NAME）
- 处理的最后一步：执行异步请求`WebAsyncUtils.getAsyncManager(webRequest).startDeferredResultProcessing()`