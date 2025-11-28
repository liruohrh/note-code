```vue
<keep-alive :exclude="['BrowserPages']">
  <component :is="Component" :key="route.fullPath" />
</keep-alive>
```

- 这个keep-alive好像是根据url缓存的，包含查询参数
	- 当router传递state而不是query时，缓存的页面状态保存，但是如果是query就会不一样，因此是根据url缓存的