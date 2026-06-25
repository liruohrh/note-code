- 模块：admin.py
- 注册URL：`django.contrib.admin.site.urls`
# site
- `django.contrib.admin.sites.AdminSite`
	- 默认是`django.contrib.admin.sites.site`
	- 用于定义site，如首页URL、模板、admin app URL
# 注册模型到site中
- admin.site.unregister(Group)

# URL
Django 管理后台的基础 URL 通常是 `/admin/`，但可以通过配置修改。例如：
- 默认管理后台首页：`/admin/`
- 登录页面：`/admin/login/`
- 登出页面：`/admin/logout/`

对于每个注册到管理后台的模型，Django 会自动生成一组 URL，用于处理该模型的增删改查操作。URL 结构如下：

## (1) **模型列表页面（分页列表）**

- URL 格式：`/admin/<app_label>/<model_name>/`
    
    - `<app_label>`：模型所属应用的名称。
        
    - `<model_name>`：模型的名称（小写）。
        
- 示例：
    
    - 如果有一个 `Article` 模型，属于 `blog` 应用，那么列表页面的 URL 是：`/admin/blog/article/`
        
    - 分页参数：`/admin/blog/article/?p=2`（访问第二页）
        

## (2) **添加新记录页面**

- URL 格式：`/admin/<app_label>/<model_name>/add/`
    
- 示例：
    
    - 添加新文章的 URL 是：`/admin/blog/article/add/`
        

## (3) **编辑记录页面**

- URL 格式：`/admin/<app_label>/<model_name>/<object_id>/change/`
    
    - `<object_id>`：记录的主键（通常是 ID）。
        
- 示例：
    
    - 编辑 ID 为 1 的文章的 URL 是：`/admin/blog/article/1/change/`
        

## (4) **删除记录页面**

- URL 格式：`/admin/<app_label>/<model_name>/<object_id>/delete/`
    
- 示例：
    
    - 删除 ID 为 1 的文章的 URL 是：`/admin/blog/article/1/delete/`
        

## (5) **查看记录历史**

- URL 格式：`/admin/<app_label>/<model_name>/<object_id>/history/`
    
- 示例：
    
    - 查看 ID 为 1 的文章的历史记录的 URL 是：`/admin/blog/article/1/history/`

## 自定义URL
- `ModelAdmin#get_urls`
- `self.admin_site.admin_view(xxx_view)`：管理视图
	- xxx_view是ModelAdmin子类的自定义视图方法
	- 其实ModelAdmin就差不多是一个DRF的viewset