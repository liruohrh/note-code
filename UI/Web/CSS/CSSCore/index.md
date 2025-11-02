# 100%
- 设置html的width、height为100%只是设置为视口的宽高

# overflow
- hidden: 隐藏
	- 比如
		- 层叠多个元素时都需要一样的圆角，给父亲元素设置圆角再设置overflow:hidden就完成了

# Icon图标与文本高度不一致
```css
.icon-text > span,.icon-text > svg{
	vertical-align: middle;
}
```