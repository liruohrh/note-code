# AI

- https://huggingface.co/openbmb/MiniCPM-o-4_5
	- 视觉理解
	- 根据B站林亦做的mc实时评论，看起来很不错
## 美术
[ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/.claude/skills/ui-ux-pro-max/SKILL.md)、Taste 这种配色/字体/风格库




参考： https://pasqualepillitteri.it/zh/news/889/claude-code-18-zuijia-skill-ui-ux-sheji-zhinan

| Skill                         | Stars  | Focus        | 适用对象            |
| ----------------------------- | ------ | ------------ | --------------- |
| **Anthropic Frontend Design** | 136.6k | 独特美学         | 所有人(推荐基础)       |
| **UI/UX Pro Max**             | 101.9k | 自动设计系统       | 多平台项目           |
| **Taste Skill**               | 59.4k  | 参数化控制        | 追求精细控制者         |
| **Interface Design**          | 5.2k   | 长期一致性        | 长周期项目           |
| **Frontend Design Pro Demo**  | 240    | 11 种现成风格     | 探索不同风格          |
| **Designer Skills**           | 1.7k   | 完整流程         | 专业 UX 设计师       |
| **Bencium UX**                | 326    | UX 基础        | 追求方法论严谨者        |
| **Vercel Agent Skills**       | 28.8k  | 技术品质         | 视觉 Skill 的补充    |
| **Refactoring UI**            | 30     | 视觉审计         | 现有 UI 的快速修复     |
| **UX Heuristics**             | 1.6k   | 尼尔森启发式       | 上线前可用性审计        |
| **iOS HIG Design**            | 483    | Apple HIG 原生 | iOS/SwiftUI 开发者 |
| **Hooked UX**                 | 1.6k   | 留存与参与度       | 低留存产品           |
| **Design Sprint**             | 1.6k   | 5 天冲刺        | 新点子验证           |


- https://v0.app/pricing

## draw
- tldraw：开源免费的React绘图库
	- 提供的一些结合AI的免费服务
		- https://makereal.tldraw.com/
			- #ai/prototyping #ai/sketching_to_ui
			- 原型开发
			- 挺糟糕的，推荐用tldraw画完给可以发图片的编程AI好点
		- https://teach.tldraw.com/
			- #ai/draw/easy 
			- AI绘图，且可以借助tldraw更好地修改
		- https://computer.tldraw.com/
			- #ai/VisualProgramming
			- 类似于图形化编程
## tts
- kokoro
	- #ai/tts/en #ai/tts/cpu
	- https://huggingface.co/hexgrad/Kokoro-82M
	- https://huggingface.co/spaces/hexgrad/Kokoro-TTS
	- [TTS排名](https://huggingface.co/spaces/TTS-AGI/TTS-Arena)
	- [介绍、本地部署](https://www.bilibili.com/video/BV1BscBePE2j)
## code
- https://copycoder.ai/
	- 极强的复制能力，输出promat，让AI编辑器进行编写
	- [例子](https://www.bilibili.com/video/BV1YrfqY2Ebi/)


# Agent
- AI的输入输出优化器
- 方式：普通文本、结构化文本、代码
- [开源的smolagents -- 一个很好的理解代码agnet例子](https://www.bilibili.com/video/BV1x266YNEm8)

# MCP
- AI和 AI IDE的中间件
- [使用Claude桌面端，其支持MCP](https://www.youtube.com/watch?v=kFwE4hHbkT0)

## mcpc 提供mcp cli访问
- `npx mcpc`
- https://github.com/apify/mcpc
- 启动：`mcpc connect --stdio [configFile[:mcpName] | url]` （包括cli的mcp）
	- 默认自动发现（当前目录下的.mcp.json, 其他agent的mcp）
	- 也可以指定配置文件，可指定某个name
	- 也可以指定URL
		- 需要 `mcpc login URL`  浏览器 OAuth，存 profile
		- [connect 认证方式](https://github.com/apify/mcpc/blob/main/README.md#authentication-precedence)
	- 这些 mcpc connect --help里都有说明

### 怎么给一个项目用
- `npx skills add apify/mcpc -a zed -y -s mcpc`

- AGENTS.md （手动管理此项目的mcp会话）
```markdown
# mcp
- 本项目存在mcp，必须使用 mcpc skill 来用 mcpc cli 连接
- 目前有mcp会话
  - @sessname: desc
```


# Agent经验

- 讨论会降低注意力，会把讨论中的某个要求之类的遗忘，要么全程记录，要么在开始执行之前复盘讨论
  - claude code
- 即便使用任务列表这些方式，模型依然会虚假标记任务为完成，或者某些要求未实现，且在最后的输出中没有说明这些。
  - claude code

