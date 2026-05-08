| 参数/配置     | Windows                             | macOS                        | Linux                    | 说明                       |
| --------- | ----------------------------------- | ---------------------------- | ------------------------ | ------------------------ |
| **基础启动**  |                                     |                              |                          |                          |
| 管道通信      | `--inspector-pipe`                  | `--inspector-pipe`           | `--inspector-pipe`       | 启用 Inspector 管道通信        |
| **显示模式**  |                                     |                              |                          |                          |
| 无头模式      | `--headless`                        | `--headless`                 | `--headless`             | 启用无头模式                   |
| 禁用启动窗口    | `--no-startup-window`               | `--no-startup-window`        | `--no-startup-window`    | 非持久模式下不显示启动窗口            |
| 用户数据目录    | `--user-data-dir=<path>`            | `--user-data-dir=<path>`     | `--user-data-dir=<path>` | 持久模式下的用户数据目录             |
| **平台特定**  |                                     |                              |                          |                          |
| 硬件加速      | `--disable-accelerated-compositing` | -                            | -                        | Windows 上禁用硬件加速（WSL 除外）  |
| **代理配置**  |                                     |                              |                          |                          |
| 代理服务器     | `--curl-proxy=<url>`                | `--proxy=<url>`              | `--proxy=<url>`          | 不同平台使用不同参数名              |
| 代理绕过      | `--curl-noproxy=<list>`             | `--proxy-bypass-list=<list>` | `--ignore-host=<host>`   | 代理绕过列表格式不同               |
| **环境变量**  |                                     |                              |                          |                          |
| Cookie 存储 | `CURL_COOKIE_JAR_PATH`              | -                            | -                        | Windows 持久模式下的 Cookie 路径 |
|           |                                     |                              |                          |                          |
|           |                                     |                              |                          |                          |

### 特殊处理机制

1. **SOCKS5 代理转换**
   - Windows 平台会自动将 `socks5://` 转换为 `socks5h://` 以解决主机名解析问题

2. **WSL 路径转换**
   - 当使用 `webkit-wsl` 通道时，用户数据目录路径会通过 WSL 路径转换函数处理

# 参数
## Windows
### `--no-startup-window`
防止浏览器在非持久模式下启动时显示启动窗口。
当 Playwright 创建没有用户数据目录的临时浏览器上下文时，会使用此功能。（Playwright认为非持久化上下文基本不需要窗口）

### `--disable-accelerated-compositing`  
禁用 Windows 系统（WSL 除外）上 WebKit 的硬件加速功能。添加此标志是为了防止在 Windows 平台上运行时出现潜在的渲染问题

### `--curl-proxy` 的作用
- WebKit用curl作为网络库，因此完全支持curl代理功能

- **macOS**: 使用 `--proxy` 和 `--proxy-bypass-list`  
    **macOS** ：使用 `--proxy` 和 `--proxy-bypass-list`
- **Linux/WSL**: 使用 `--proxy` 和 `--ignore-host`  
    **Linux/WSL** ：使用 `--proxy` 和 `--ignore-host`
- **Windows**: 使用 `--curl-proxy` 和 `--curl-noproxy`  
    **Windows** ：使用 `--curl-proxy` 和 `--curl-noproxy`