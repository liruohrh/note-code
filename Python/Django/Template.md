- 注释：` {% comment %}  {% endcomment %}`，不会输出到HTML中

# context_processors
- 在`TEMPLATES`元素的`OPTIONS.context_processors`添加，按定义顺序执行
- 先执行view，在render时调用，在视图中可以直接使用 `{{ xxx }}` 获取