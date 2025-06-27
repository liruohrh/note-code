- 更新时：用`Model(&user).Updates(user)`，更新的同时还会更新user对象
	- 推荐用updates的对象ID是零值，避免生成更新ID语句

- 全量更新：Save(model)
- 非零值更新：Updates(model)
	- 更新所有指定值：Updates(map) 或者 Select().Updates()
	- Updates(dto)：用非model进行更新会导致不会触发钩子（如UpdatedAt）
- ，如此一来，设置为指针类型+Update更新会好一点
- DTO：用dto不会触发model方法，如UpdatedAt
	- 可以`Model(&user).[Create | Update](dto)`但是不能`Model(&user).Save(dto)`