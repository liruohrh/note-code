# UI框架
## Makepad
- **渲染模式**: 基于 GPU 加速的实时渲染。
- **UI 构建方式**: 代码驱动（非声明式）。
- **跨平台支持**: 
- **性能**: 高性能，适合需要高帧率和复杂图形的应用（如游戏、设计工具）。
- **特点**:
  - 自定义渲染引擎，支持 GPU 加速。
  - 实时交互和动画支持。
  - 灵活的 UI 构建方式，适合需要精细控制的场景。
- **适用场景**: 游戏、图形工具、实时可视化应用。
- **GitHub**: [Makepad](https://github.com/makepad/makepad)

---

##  Dioxus
- **渲染模式**: 基于虚拟 DOM 的声明式 UI。
- **UI 构建方式**: 声明式（类似 React）。
- **跨平台支持**: 
- **性能**: 高性能，得益于 Rust 和虚拟 DOM 的优化。
- **特点**:
  - 类似 React 的 API，适合前端开发者。
  - 支持状态管理和组件化开发。
  - 跨平台代码共享（Web 和桌面）。
- **适用场景**: 跨平台应用（Web、桌面、移动端）、需要快速开发的应用。
- **GitHub**: [Dioxus](https://github.com/dioxuslabs/dioxus)

---

## egui
- **渲染模式**: 立即模式（Immediate Mode GUI）。
- **UI 构建方式**: 立即模式，UI 逻辑在每一帧中重新构建。
- **跨平台支持**: 支持 Web（WebAssembly）、桌面（通过 `eframe`）。
- **性能**: 轻量级，适合中小型应用。
- **特点**:
  - 简单易用，适合快速原型开发。
  - 无状态 UI，适合需要动态更新的界面。
  - 内置丰富的 UI 组件（按钮、滑块、文本框等）。
- **适用场景**: 工具类应用、调试界面、快速原型开发。
- **GitHub**: [egui](https://github.com/emilk/egui)

---

## Slint
- **渲染模式**: 保留模式（Retained Mode GUI）。
- **UI 构建方式**: 声明式（基于标记语言）。
- **跨平台支持**: 支持桌面（Windows、macOS、Linux）、嵌入式设备、Web（实验性）。
- **性能**: 高性能，适合嵌入式设备和桌面应用。
- **特点**:
  - 使用自定义的标记语言（类似 QML）定义 UI。
  - 支持动态数据绑定和状态管理。
  - 专注于嵌入式设备和低资源环境。
- **适用场景**: 嵌入式设备、桌面应用、需要高性能和低资源占用的场景。
- **GitHub**: [Slint](https://github.com/slint-ui/slint)

---

## Floem
- [lapce/floem：具有细粒度反应性的原生 Rust UI 库 --- lapce/floem: A native Rust UI library with fine-grained reactivity](https://github.com/lapce/floem)
- 比较不主流的PC UI框架


# 对比总结

| 特性            | Makepad                                       | Dioxus                                         | egui                                  | Slint                                      |
| ------------- | --------------------------------------------- | ---------------------------------------------- | ------------------------------------- | ------------------------------------------ |
| **渲染模式**      | GPU 加速实时渲染                                    | 虚拟 DOM                                         | 立即模式                                  | 保留模式                                       |
| **UI 构建方式**   | 代码驱动                                          | 声明式（类似 React）                                  | 立即模式                                  | 声明式（基于标记语言）                                |
| **跨平台支持**     | Web、桌面                                        | Web、桌面、移动端（实验性）、TUI                            | Web、桌面                                | 桌面、嵌入式设备、Web（实验性）                          |
| **性能**        | 高性能，适合图形密集型应用                                 | 高性能，虚拟 DOM 优化                                  | 轻量级，适合中小型应用                           | 高性能，适合嵌入式设备                                |
| **适用场景**      | 游戏、图形工具、实时可视化                                 | 跨平台应用、快速开发                                     | 工具类应用、快速原型开发                          | 嵌入式设备、桌面应用                                 |
| **GitHub 链接** | [Makepad](https://github.com/makepad/makepad) | [Dioxus](https://github.com/dioxuslabs/dioxus) | [egui](https://github.com/emilk/egui) | [Slint](https://github.com/slint-ui/slint) |

---

# 选择建议
- 如果你需要 **高性能图形渲染** 和 **实时交互**，选择 **Makepad**。
- 如果你需要 **跨平台支持** 和 **类似 React 的开发体验**，选择 **Dioxus**。
- 如果你需要 **快速原型开发** 和 **简单易用的 UI**，选择 **egui**。
- 如果你需要 **嵌入式设备支持** 或 **低资源占用的高性能应用**，选择 **Slint**。