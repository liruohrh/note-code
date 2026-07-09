
# Join
- `inner join` 仅在on成立时保留左右表的行
	- 过滤条件放在on、where都无所谓
- `outer join` 在on不成立时仍然保留左或者右表的行，`left outer join`就是保留左表
	- 当需要过滤right表时，如果放在where执行，需要注意如果是`left outer join`，则right表得注意，所有字段都可能为NULL
	- 过滤left表则不能放在on，必须放在where，否则会因为左或者右保留
- on在join时执行，而where在join后才执行