- 原理：基于令牌桶算法，限制QPS
# 参考
- [流量控制算法——漏桶算法和令牌桶算法](https://zhuanlan.zhihu.com/p/165006444)
- [谷歌Guava限流工具RateLimiter](https://zhuanlan.zhihu.com/p/205266820)
# 特点
- 透支未来令牌
	- 比如QPS是10，当前有10，而请求20，那么也会立即响应，而这个缺少的10将由下一秒补充，而下一个请求就要多等这一秒
# API
- `RateLimiter.create(double permitsPerSecond, long warmupPeriod, TimeUnit unit)`
	- `permitsPerSecond`：每秒资源数量，即QPS，仅该参数创建SmoothBursty
	- `warmupPeriod`：热身时间，会创建SmoothWarmingUp
		- 初始状态是冷状态（即无请求）
		- 预热状态：在这个warmupPeriod内缓慢发放token，直到过去了，才恢复正常的QPS
			- 用于避免系统启动突然遭受大量请求而出问题
		- 热状态：正常QPS
		- 在warmupPeriod内没有请求，则恢复到冷状态，再次接收到请求则重新预热、恢复热状态
	- `unit`：warmupPeriod单位
- `double acquire(int permits)`
	- 请求资源数量，返回等待时间
- 简单描述限流
	- `RateLimiter.create(10)`
	- `rateLimiter.acquire(20)`，第一次不用等待，透支了10个token ，下一轮不会响应
	- `rateLimiter.acquire(30)`，2s后执行，透支了20个token，下两轮不会响应