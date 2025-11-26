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


