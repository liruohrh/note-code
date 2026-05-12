

# 添加补丁
- `git apply browser_patches\webkit\patches\bootstrap.diff`
- 复制browser_patches\webkit\embedder\Playwright到Tools\Playwright
- 6340ce0d733541ce69d28 2026-4-28的构建有问题`Source\WebKit\UIProcess/WebPageProxy.cpp(2872,55): error: no member named 'SetDeviceOrientation' in namespace 'Messages::WebPage'`
	- 修复方法：在Source\cmake\OptionsWin.cmake的`# Plawright begin`处添加`WEBKIT_OPTION_DEFAULT_PORT_VALUE(ENABLE_ORIENTATION_EVENTS PRIVATE ON)`


# 参考
- [# [Question] How does Playwright track, build and embed the open source WebKit?](https://ray.run/discord-forum/threads/200734-question-how-does-playwright-track-build-and-embed-the-open-source-webkit#:~:text=firefox%20%E9%9C%80%E8%A6%81%E5%AF%B9%E5%85%B6%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7%E5%8D%8F%E8%AE%AE(juggler)%E8%BF%9B%E8%A1%8C%E8%A1%A5%E4%B8%81%E3%80%82)
- [playwright v1.6.2 还有介绍一点补丁的开发和构建流程](https://github.com/microsoft/playwright/tree/v1.6.2/browser_patches)

- [webkit 构建平台](https://build.webkit.org/)

- [slack 交流平台](https://app.slack.com/client/T06G50708/CU84Q46JZ)