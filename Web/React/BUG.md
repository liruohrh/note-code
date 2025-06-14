# setState in rendering循环渲染
- 子组件渲染时触发了父组件setState，导致循环渲染
- [子组件渲染使用调用了父组件setState](https://github.com/facebook/react/issues/18178#issuecomment-602344662)
	- 我的情况：子组件是是WebView，用来收集数据的，而该数据是父组件的状态，父组件需要在收集到数据时setState，而由于子组件WebView是一个WebViewPool导致其收集到数据后也进行了渲染，因此导致了循环渲染？
“Cannot update a component (SamplesWebViewMultiScreen) while rendering a different component (WebViewPool)”。这通常是由于在渲染过程中调用了setState导致的。这可能发生在WebViewPool组件在渲染时触发了父组件SamplesWebViewMultiScreen的状态更新，从而引发重新渲染循环。
- 解决方法：缓存子组件，因为这个状态通常不需要用在子组件。