# Image缓存无法用ImageCache清除
- 方法：
1. 删除缓存：
2. 更新Image：由于Image是一个StatefulessWidget，根据其State类的didUpdateWidget，其使用`==`来判断2个widget是否相等，因此可以选择重写`==`，不过推荐使用key
	1. 使用ValueKey，可以根据某个值，这里使用重写时间戳（因为我这里是重写图片文件）
		1. 当然啦，根据重写参数更好，就可以用ObjectKey(argObj)（使用identical、identityHashCode，比较的是引用而不是`==`）
	2. 如果想每次不管如何都更新，就用UniqueKey，这样每次就都不一样
```dart
Image.file(
  File(controller.thumbnailPath.value!),
  key: ValueKey(controller.generateAt.value), 
),

final evictRes = imageCache.evict(FileImage(
  File(thumbnailPath.value!),
));
if(evictRes){
	print("删除成功");
}
```
