# Platform Specific Code
- https://reactnative.dev/docs/platform-specific-code

# UI
-  [tailwind](https://docs.expo.dev/guides/tailwind/)
	- 支持
		1. [nativewind](https://www.nativewind.dev/getting-started/installation)
		2. 在native可以直接用webview显示
# 插件模拟器
- https://ide.swmansion.com/
	- VSCode插件
# Build
- [metro 打包工具](https://metrobundler.dev/)


# 无框架
- `npx @react-native-community/cli init`
	- `npx react-native init`是旧的，0.76后官方推荐用@react-native-community/cli来创建项目等，react-native则用来执行编译等
- 默认有一个
	- `import { NewAppScreen } from '@react-native/new-app-screen';`
	- `<NewAppScreen templateFileName="App.tsx" />`
	- 显示React Native的一些版本、文档，templateFileName只是单纯的字符串，显示文本
- 开发模式（非常有意思）
	- `yarn android`进行启动dev服务器、编译app并安装
	- 如果没有修改原生代码，则只需要启动dev服务器即可`yarn start`
		- 但是注意要转发端口`adb reverse tcp:8081 tcp:8081`


# Expo框架 
- `npx create-expo-app@latest`
- `/scripts/reset-project.js`该脚本用于把默认代码迁移到app-example，写自己代码

## 构建方式
- expo go app：包含了expo预制环境，可以让app仅编译JS直接在设备运行
	- 推荐简单开发时用这个即可
	- `npm run start | npx expo start`
- [开发版本介绍](https://docs.expo.dev/develop/development-builds/introduction/)
	- [local development build](https://docs.expo.dev/guides/local-app-development/)：构建自己的APK，而不是上传到Expo Go app，因此可以写原生代码
		- 如何还需要调式功能，需要自己安装expo-dev-client，`npx expo install expo-dev-client`
			- 当安装了这个，就必须只能自己编译应用，无法使用Expo Go，除非uninstall这个依赖
		- `npx expo run:android`
		- `npx expo run:ios`
		- 第一次运行会生成android或者ios目录（原生代码）
			- 第一次编译巨慢无比，第二次非常快（可能是不涉及原生代码修改就会非常快）
			- 第一次编译时的第一次刷新页面也慢了一点，后面就和Expo Go开发一样了（可能和上面一样，不涉及原生代码编译）
			- 重启电脑后再次编译，又变得和第一次编译差不多（但是应该说是1/4）
		- 如果修改了一些会影响原生代码的配置，最好先删除原生代码，也可以用``npx expo prebuild --clean
	- [local production build](https://docs.expo.dev/guides/local-app-production/)：好像并没有做什么修改，只是做原生构建也需要的，没有排除expo-dev-client

## Storage
- [多种数据存储方式](https://docs.expo.dev/develop/user-interface/store-data/)
## Library
- [添加库](https://docs.expo.dev/workflow/using-libraries/)
	- react native
	- expo sdk
	- 推荐用
	- third party：如 [React Native Directory](https://reactnative.directory/) 

# pnpm
- 暂不完全支持，因此完全不推荐用