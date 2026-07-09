- [https://developer.chrome.com/docs/extensions/mv3/manifest/](https://developer.chrome.com/docs/extensions/mv3/manifest/)
- 如果没有在manifest.json注册功能，就不能使用（比如没有comands就不能用chrome.commands）

```json
{
  //安装扩展的最低chrome版本
  "minimum_chrome_version": "107.0.5304.87",
  "name": "扩展名",
  "description": "扩展描述",
  "version": "版本",
  "manifest_version": 3,//最新是3
	//适配icon, 可以和default_icon一样, ???不理解有什么区别
  "icons": {
    "16": "images/icon-16.png",
    "32": "images/icon-32.png",
    "48": "images/icon-48.png",
    "128": "images/icon-128.png"
  },

  //action
  "action": {
    "default_title": "提示词, 当悬停在扩展按钮上时会显示",
    "default_popup": "点击右上角扩展图片, 会加载的html/js",
    "default_icon": "右上角扩展显示图标,必须是png"
  },

  //content_scripts
  "content_scripts": [
    {
      "js": [
        "scripts/cs1-show-cur-datetime.js"
      ],
      "matches": [
        "https://developer.chrome.com/docs/extensions/*"
      ]
    }
  ],

  //service_worker
  "background": {
    "service_worker": "service-worker.js"
  },
  //权限
  "permissions":[
    //比如chrome.tabs就需要
    "activeTab"
  ],
  //仅在匹配到的host中批准permissions, 或者允许service_worker访问的url
  "host_permissions": ["https://developer.chrome.com/*"],
  
  "commands":{
    //启动popup命令, 等同于chrome.action.onClick事件
    "_execute_action": {
      "suggested_key": {
        "default": "Ctrl+Shift+F",
        "mac": "Command+Shift+F"
      },
      "description": "Opens popup.html"
    },
    //自定义命令 需要注册background.service_worker, 使用chrome.commands.onCommand.addListener监听该命令(按下快捷键会发出命令, 用户无法监听_execute_action)
    "log-foo": {
      "suggested_key": {
        "default": "Ctrl+Shift+Y",
        "mac": "Command+Shift+Y"
      },
      "description": "log \"foo\" on the current page."
    }
  },
  
}
```

# 匹配规则

- `*`：通配符，比如`https://a.*/*`表示权威域名是a的任意路径，第一个*从a.通配到/，第二个从/通配剩余的 w

# permissions

- [https://developer.chrome.com/docs/extensions/mv3/declare_permissions/](https://developer.chrome.com/docs/extensions/mv3/declare_permissions/)
- `activeTab`如果没有，就不能访问属于某个tab的数据，只能访问共享的


