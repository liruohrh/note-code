


- views.py：渲染单个实体视图
- admin.py：数据的操作、分页视图
- context_processors.py：注入

# admin.py
- admin.ModelAdmin
- fields：表单字段（必须是Model字段）

- 分页展示
- list_display：表格字段，可以是一个方法
	- 如一个html字符串
		-  action：显示在每行的HTML
			- 引用admin URL：`reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])`
			- 使用返回format_html函数的返回值，`{}`占位符
- list_per_page：page size
- sortable_by：排序字段


- get_queryset
- 修改：按顺序执行
	- save_form：仅创建时执行，修改直接是form.instance
		- form.save返回instance，这是没持久化的对象
	- save_model
		- 保存到数据库
	- save_formset：model表明是哪个inline表单
		- save：返回self.save_existing_objects(commit) + self.save_new_objects(commit)
			- 相当于formset.changed_objects+formset.new_objects


- 渲染到HTML的值：
	- `django.forms.BaseForm#get_initial_for_field(field.name, field.initial)`field.initial是在定义Field时设置的，value可以是无参函数
	- `django.forms.fields.Field#prepare_value`
# forms.ModelForm

- https://blog.csdn.net/m0_66925868/article/details/136599170
- initial：初始化表单数据
- cleaned_data：校验过的数据
- instance：创建的对象（创建）或者传入的对象（修改）
- BaseForm
	- is_valid：整体校验，返回True表示valid
	- clean=cleaned_data、changed_data
	- errors->full_clean
		- full_clean：进行校验，`clean_{field_name}()  clean()  _post_clean()`（默认都是没有的）
		- ValidationError都被捕获到errors
- BaseFormSet
	- forms：所有表单（因为可能不止一个，比如内联表单）
- BaseModelFormSet：
	- model

- fieldsets：属性分类，每个一个大标题
	- None表示无标题，按顺序显示每个标题和归属属性
	- 如`('User', {'fields': ('name', 'email')} ),`
		- 会有User标题，属性name、email归属于该标题下

# inlines-内联表单
- InlineModelAdmin：仅仅是template不一样
	- admin.TabularInline：表格
	- admin.StackedInline：卡片
