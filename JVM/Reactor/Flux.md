#/nio/reactor/flux

- 操作符：就是其一系列函数
	- [reactor之操作符](https://juejin.cn/post/7197608560602824761)
# 生命周期操作符
- doOnSubscribe
- doOnRequest
- doOnEach
- doOnNext：emit一个数据（消费一个数据，消费者）
- doOnCancel、doOnError、doOnDiscard
- doOnComplete
- doOnTerminate：所有数据被消费
- doFinally：和try finally一样

- Subscriber其实仅有onSubscribe、onNext、onError、onComplete
	- onSubscribe=doOnSubscribe、doOnRequest
	- onNext=doOnEach、doOnNext
	- onError
	- onComplete
- 执行顺序
	- 生命周期操作符会在对应的生命周期之前执行
	- onSubscribe
	- 转换操作符：仅在onNext前执行
	- onNext
	- onError
	- onComplete
# subscribe
- 注册一个订阅者，可以注册多个（默认按注册顺序执行每个订阅者的所有操作），默认所有订阅者都会接收到一样的数据流
- 可以是一个类，也可以只是部分如仅consumer（在onNext执行）会自动注册一个LambdaSubscriber

# 顺序操作符
- doFirst：一定第一个先执行，比生命周期操作符还要先执行，但是在流中仅执行一次
	- 在被订阅之前执行，因此使用创建Flux所在线程
- doAfterTerminate：流Terminate后执行，在流中仅执行一次

# 转换操作符
- map：转换元素
- concatMap：合并一个由元素转换的流
# 合并
- zip/zipWith：
	- 默认combinator是Tuple2
	- 合并后长度为最短的流的长度，多余的忽视
- merge/mergeWith：交叉合并，只要有元素被emit就合并该元素，这个才算是真正的合并流
- concat/concatWith：按给的流的顺序合并所有

# 缓存
- BackpressureBuffer：当产生背压时缓存元素
	- size：默认`Queues.SMALL_BUFFER_SIZE` （256）
	- BufferOverflowStrategy：默认ERROR

# prefetch
- 对于转换等操作符，会默认提取`Queues.XS_BUFFER_SIZE | Queues.SMALL_BUFFER_SIZE`（或者其他）个进行缓存