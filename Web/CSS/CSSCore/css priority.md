- 当多个选择器同时选中了同一个元件时，如果其中含有相同的属性，[CSS 层叠规范](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Cascade)定义了它们生效的优先级。 比如，通过元件上的样式属性（`style`）设置的样式会覆盖通过样式规则（style rule, 比如类选择器）匹配到的样式
- [权重（specificity）](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Specificity)高的选择器中的样式覆盖权重低的；在文档中后出现的样式规则覆盖先出现的等。

#  优先级
1. `!important`：最高，都有时仍然比优先级
2. inline. `(1,0,0,0)`
3. id. `(0,1,0,0)`
4. class、attribute、pseudo class `(0,0,1,0)`
5. element、pseudo element `(0,0,0,1)`
6. `*`、+ `(0,0,0,0)`

- 多个会进行叠加，比如
	- `.a .b = (0,0,2,0)`
	- `.b = (0,0,1,0)`
	- `#a .b = (0,1,1,0)`


# Vue Scoped CSS
- 会在规则最后添加id属性，如`.a .b[data-id-xxx]`


