- feat
- fix
	- 因没注意到目标某些情况而修改代码（漏考虑场景），视为bug
- refactor
	- 因目标规则变化而修改，如果因此添加了功能，则用feat
- pref
- chore：构建过程或辅助工具的变动
	- 如.gitignore、仅文件位置变动、ide配置、与业务代码无关的脚本
- style：代码风格、格式化
- test
- docs：文档、代码注释
- ci：CI 工具
- build
	- 运行、编译脚本
- deps
	- 当可以分开提交依赖和功能实现时，选择先deps提交依赖变更
- 配置文件的修改：根据情况而选择适合的规范



以下是为全栈程序员设计的详细 Git Commit 提交规范模板，涵盖前端、后端、数据库、DevOps 等多领域，按技术维度分类：

---

### **一、基础规范模板**
```text
<type>(<scope>): <subject>  # 标题行（必填）
<BLANK LINE>                # 空行分隔
<body>                      # 详细说明（选填）
<BLANK LINE>
<footer>                    # 关联问题/破坏性变更（选填）
```

---

### **二、全栈分类提交示例**
#### **1. 前端相关**
| 类型                | 作用域    | 示例                                           |
| ----------------- | ------ | -------------------------------------------- |
| `feat(ui)`        | 新增界面组件 | `feat(ui): 添加用户资料卡片组件`                       |
| `fix(css)`        | 样式修复   | `fix(css): 修正移动端导航栏错位问题`                     |
| `refactor(react)` | 重构逻辑   | `refactor(react): 使用 Context API 重构全局状态管理`   |
| `perf(animation)` | 性能优化   | `perf(animation): 使用 CSS will-change 优化转场性能` |

#### **2. 后端相关**
| 类型                 | 作用域      | 示例                                 |
| ------------------ | -------- | ---------------------------------- |
| `feat(api)`        | API 接口新增 | `feat(api): 新增 /users/search 搜索接口` |
| `fix(auth)`        | 认证修复     | `fix(auth): 修复 JWT 令牌刷新逻辑漏洞`       |
| `docs(swagger)`    | API文档更新  | `docs(swagger): 添加订单创建接口的请求示例`     |
| `test(middleware)` | 中间件测试    | `test(middleware): 添加速率限制中间件的单元测试` |

#### **3. 数据库相关**
| 类型            | 作用域  | 示例                                        |
| ------------- | ---- | ----------------------------------------- |
| `migration`   | 数据迁移 | `migration: 新增产品价格历史表 (UP: 202403010823)` |
| `fix(query)`  | 查询优化 | `fix(query): 优化用户分页查询的索引使用`               |
| `feat(redis)` | 缓存新增 | `feat(redis): 为商品详情添加 LRU 缓存策略`           |

#### **4. 全栈交叉**
| 类型                | 作用域   | 示例                                       |
| ----------------- | ----- | ---------------------------------------- |
| `feat(fullstack)` | 端到端功能 | `feat(fullstack): 实现购物车同步功能（前端+API+缓存）`  |
| `refactor(types)` | 类型定义  | `refactor(types): 统一前后端用户数据模型 (UserDTO)` |

#### **5. DevOps 相关**
| 类型             | 作用域    | 示例                                       |
| -------------- | ------ | ---------------------------------------- |
| `ci(pipeline)` | CI流程更新 | `ci(pipeline): 添加多阶段 Docker 构建流程`        |
| `chore(env)`   | 环境配置   | `chore(env): 更新 .env.example 添加 SMS 配置项` |

---

### **三、完整提交示例**
#### **示例1：功能开发**
```text
feat(checkout): 实现三合一支付功能（微信+支付宝+银联）

- 前端添加支付方式选择组件
- 新增 /api/v2/payment 聚合支付接口
- 添加支付流水表 migration
- 更新 Swagger 文档

Closes #235
Related to #112
```

#### **示例2：紧急修复**
```text
fix(security)!: 紧急修复 SQL 注入漏洞

- 使用参数化查询重构用户搜索接口
- 添加 SQL 注入测试用例
- 更新 ORM 配置强制使用预处理

BREAKING CHANGE: 废弃旧版 /search 接口
```

#### **示例3：跨团队协作**
```text
refactor(analytics): 整合第三方埋点系统 [与数据团队协作]

- 前端添加 GTM 事件跟踪
- 后端添加 Kafka 埋点生产者
- 更新 docker-compose 添加 Kafka 服务

Co-authored-by: li.ruohang <li.ruohang@partner.com>
```

---

### **四、特殊场景处理**
#### **1. 大规模重构**
```text
refactor(architecture): 迁移至微服务架构

前端:
- 拆分为独立订单模块
- 使用 Module Federation 实现动态加载

后端:
- 分解用户服务为独立模块
- 添加 gRPC 通信层

BREAKING CHANGES:
- 需要更新 API Gateway 配置
- 数据库连接池配置变更
```

#### **2. 多技术栈更新**
```text
chore(stack): 升级技术栈版本

- Node.js 18 → 20
- React 17 → 18 (启用并发模式)
- Spring Boot 2.7 → 3.2
- MySQL 5.7 → 8.0

Migration Guide:
1. 更新 JDK 到 17+
2. 运行 `npm ci --legacy-peer-deps`
```

#### **3. 实验性功能**
```text
feat(ai): 实验性接入 GPT-4 客服 [WIP]

- 添加 /api/ai-chat 接口
- 前端实现聊天界面原型
- 添加限流熔断机制

TODO:
- [ ] 敏感词过滤
- [ ] 对话历史持久化
```

---

### **五、提交规范检查工具**
#### 1. Commitlint 配置示例
```json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "scope-enum": [2, "always", [
      "ui", "api", "db", "auth", "ci", 
      "docker", "migration", "fullstack"
    ]],
    "body-max-line-length": [0],
    "footer-max-line-length": [0]
  }
}
```

#### 2. 预提交钩子示例 (.husky/commit-msg)
```bash
#!/bin/sh
npx commitlint --edit "$1"
```

---

通过这种结构化提交规范，可以：
1. 自动生成技术维度清晰的 CHANGELOG
2. 提高跨模块代码审查效率
3. 精准定位技术债务
4. 支持多环境部署的版本追溯

建议根据团队技术栈特点调整作用域枚举列表，保持 15-20 个核心作用域为佳。