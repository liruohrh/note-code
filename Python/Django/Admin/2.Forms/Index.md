- ModelAdmin

# 表单字段
- 如果 `fieldsets` 或 `fields` 选项都不存在，Django 将默认在一个单一的表单集中显示每个非 `AutoField` 且有 `editable=True` 的字段，顺序与模型中定义的字段相同。
## fields
- 表单包含字段，同时定义了显示顺序
	- 默认所有字段，定义顺序
	- 元素是`()`：元组里的元素会inline显示
## exclude
- 表单排除字段

## fieldsets
- 元素是`(标题, field_options)`
- 不像fields会inline，而是分组，可以有标题，还可以定义组的classes
- field_options
	- fields：这组的fields
	- classes（django默认提供了2个）
		- collapse：可折叠
		- wide：默认
	- description：这组的描述，显示在标题下
```python
fieldsets = [
	(
		None,
		{
			"fields": ["url", "title", "content", "sites"],
		},
	),
	(
		"Advanced options",
		{
			"classes": ["collapse"],
			"fields": ["registration_required", "template_name"],
		},
	),
]
```

## radio_fields
- 只能指定外键或者choice
- `radio_fields = {"group": admin.VERTICAL}`
## readonly_fields
- 只读字段

# ModelForm
- 可以指定form，也可以在get_form时对form进行操作
- 指定model时必须指定fields或者exclude，但是fields会被忽视，但

# formfield_overrides
- 覆盖表单字段构造器参数，key是字段类
```python
formfield_overrides = {
	models.TextField: {"widget": RichTextEditorWidget},
}
```


