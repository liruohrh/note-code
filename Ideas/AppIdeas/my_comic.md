
- page
	- hot comic list
	- comic detail 
	- comic chapters、comic chapter images

## 依赖分析
- dart：>=2.19.6 <3.0.0
- UI
	- cupertino_icons: ^1.0.2 - 用于在iOS风格中使用图标的Flutter插件。
	- line_icons: ^2.0.1 - 一个提供线性图标（line icons）的Flutter插件。
	- carousel_slider: ^4.2.1 - 一个用于创建轮播图效果的Flutter插件。
	- google_nav_bar: ^5.0.6 - 一个用于创建Google风格底部导航栏的Flutter插件。
	- readmore: ^2.2.0 - 用于实现文本展开/收缩功能的Flutter插件。
- 动画
	-  loading_animation_widget: ^1.2.0+4 - 用于显示加载动画的Flutter插件。
- 其他工具
	- equatable: ^2.0.5 - 用于实现值对象比较的Dart包。
	- fpdart: ^0.4.0 - 用于函数式编程的Dart包。
	- get_it: ^7.2.0 - 用于依赖注入的Dart包。
		- IOC
	- rxdart: ^0.27.7 - 用于实现响应式编程的Dart包，基于RxJava的Dart实现。
- 网络
	- http: ^0.13.5
	- dio: ^4.0.6 - 用于进行网络请求的Dart包。
	- cached_network_image: ^3.2.3 - 用于缓存网络图像的Flutter插件。
- flutter_bloc: ^8.1.1 - 用于实现业务逻辑组件（BLoC）模式的Flutter插件。

## 代码分析
- main.dart：主页面，注入blocs
- locator.dart：注入依赖
- presentation
	- bloc：写pages对应的bloc、event、state
	- pages：页面
	- widget：自定义widget
- domain：entities、repositories、usecase（类似service但是每个类一个接口）
- data：
	- datasources：数据源，remote/local
	- model：请求响应对象
	- repositories：datasource的repository