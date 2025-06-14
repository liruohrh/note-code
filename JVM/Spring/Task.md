# 配置类

## TaskExecutionAutoConfiguration

## TaskSchedulingAutoConfiguration

-  默认pool.size=1，即一次只执行一个任务
  - 即便非1，同任务仍然串行执行，需要自己处理异步执行同任务

# 线程池关闭

- await-termination=true：等待任务执行完才退出程序
- await-termination-period=10s：等待10s后退出程序，不管任务是否执行完，如果任务执行完也会直接退出不再等待

# 定时任务

- `@Scheduled`，可简单写间隔、延时，也可以使用Cron表达式
- 如果要多服务器共享，应该集成quartz

# 异步

- 异步方法：`@Async`
- 多线程池：`@Async("线程池Beanname")`
  - 使用AsyncConfigurer提供默认的，或者`@Primary`标注默认线程池TaskExecutor，或者命名为taskExecutor的Executor，否则SimpleAsyncTaskExecutor
  - 可以注入TaskExecutorBuilder，基于公共配置设置特别的配置，也可以直接new ThreadPoolTaskExecutor（TaskExecutor）或者Executor
- 异步异常：AsyncUncaughtExceptionHandler或者AsyncConfigurer（同时也可以配置默认Executor）
