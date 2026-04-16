

## 网页内容分析机制

Browser agent并非直接将原始网页内容丢给AI，而是通过一个复杂的多层处理流程来分析和理解网页内容。
### 核心分析流程

#### 1. DOM数据获取与合并

Agent首先通过CDP获取三种不同的树结构：
- DOM文档树 (`DOM.getDocument`)
- DOM快照树 (`DOMSnapshot.captureSnapshot`) 
- 可访问性树 (`Accessibility.getFullAXTree`)

然后通过`DomService.build_enhanced_tree()`将这三棵树合并成增强的DOM树，包含完整的元素信息、布局数据和可访问性属性。

#### 2. 内容优化与过滤

通过`DOMTreeSerializer`对增强DOM树进行多阶段优化：

```python
# 从browser_use/agent/prompts.py:149-216
def _extract_page_statistics(self) -> dict[str, int]:
    """Extract high-level page statistics from DOM tree for LLM context"""
    stats = {
        'links': 0,
        'iframes': 0,
        'shadow_open': 0,
        'shadow_closed': 0,
        'scroll_containers': 0,
        'images': 0,
        'interactive_elements': 0,
        'total_elements': 0,
    }
``` 
 

#### 3. LLM可理解格式转换

将优化后的DOM转换为LLM可以理解的格式：

```python
# 从browser_use/agent/prompts.py:218-315
def _get_browser_state_description(self) -> str:
    elements_text = self.browser_state.dom_state.llm_representation(include_attributes=self.include_attributes)
```

输出格式为：
```[index]<type>text</type>```
例如：
```
[33]<div>User form</div>
	[35]<button aria-label='Submit form'>Submit</button>
```

#### 4. Markdown提取（用于内容分析）

对于需要深度内容分析的场景，使用markdown提取：

```python
# 从browser_use/dom/markdown_extractor.py:22-108
async def extract_clean_markdown(
    browser_session: 'BrowserSession | None' = None,
    dom_service: DomService | None = None,
    target_id: str | None = None,
    extract_links: bool = False,
) -> tuple[str, dict[str, Any]]:
``` 

#### 5. AI驱动的内容提取

在Tools服务中，LLM用于结构化内容提取：

```python
# 从browser_use/tools/service.py:965-1195
@self.registry.action(
    """LLM extracts structured data from page markdown. Use when: on right page, know what to extract, haven't called before on same page+query.""",
    param_model=ExtractAction,
)
async def extract(
    params: ExtractAction,
    browser_session: BrowserSession,
    page_extraction_llm: BaseChatModel,
    file_system: FileSystem,
    extraction_schema: dict | None = None,
):
``` 
### 关键优化技术

1. **交互元素索引**：只为可交互元素分配索引，减少LLM处理负担
2. **视觉层次保留**：通过缩进表示DOM层次结构
3. **噪声过滤**：移除script、style等非内容标签
4. **分块处理**：对大型页面进行结构化分块处理
5. **截图辅助**：可选地提供截图作为视觉上下文

### 系统提示词指导

Agent通过详细的系统提示词指导LLM如何理解网页状态：

```python
# 从browser_use/agent/system_prompts/system_prompt_no_thinking.md:39-55
Interactive Elements: All interactive elements will be provided in format as [index]<type>text</type> where
- index: Numeric identifier for interaction
- type: HTML element type (button, input, etc.)
- text: Element description
```  
### 总结

Browser agent的内容分析是一个精密的工程化过程，通过DOM树合并→内容优化→格式转换→AI理解的多层管道，既保证了信息的完整性，又优化了LLM的处理效率。这种设计使得agent能够准确理解复杂的现代网页结构，同时控制token使用成本。
