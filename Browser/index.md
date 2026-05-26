


| 功能             | chrome                                                      | firfox                                                                  | webkit                                                                              |
| -------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 浏览器运行环境        | `chrome://version`                                          | `about:config`                                                          | ❌                                                                                   |
| 远程调试           | cdp                                                         | WebDriver BiDi                                                          | inspector                                                                           |
| 远程调试方式         | `--remote-debugging-port xxx` + `chrome://inspect/#devices` | `--remote-debugger-port xxx` + `about:debugging#/ runtime/this-firefox` | `WEBKIT_INSPECTOR_SERVER =127.0.0.1:xxx` + `inspector:// {WEBKIT_INSPECTOR_SERVER}` |
| 独立的远程调试前端      | ✅                                                           | ❌                                                                       | ✅                                                                                   |
| 独立的远程调试前端含UI控制 | ✅                                                           | -                                                                       | ❌                                                                                   |
| screencast     | ✅                                                           | ❌                                                                       | ❌                                                                                   |


