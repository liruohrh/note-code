# URL

> **URL 路径看起来完全不变（如 `/xxx.html`），但服务器根据 `Accept-Language` 或 Cookie 返回不同语言版本的 HTML 内容，没有 301/302 跳转，也没有语言前缀。**

---

### ✅ 这样做的好处

- URL 简洁，用户看不到 `/en/`、`/zh/` 等“多余”路径。  
- 对前端路由、静态资源路径、缓存 key 都不用改。  
- 用户切换语言后，地址栏不会变，体验“丝滑”。

---

### ❗但 SEO 的风险也恰恰在这里：**“同一个 URL 返回不同内容”**

搜索引擎抓取时，会把 `/xxx.html` 当成**一个页面**来索引。  
它不会每次都带同样的 `Accept-Language`，也不会带你的 Cookie，于是：

| 抓取批次 | 蜘蛛实际拿到的语言 | 它以为这是“同一个页面” |
|----------|--------------------|------------------------|
| 第 1 次  | en                 | 存成英文版             |
| 第 2 次  | zh                 | 发现内容全变了，可能判为“重复/变脸” |
| 第 3 次  | ja                 | 再次变脸，可能直接丢弃或只保留最后一次 |

结果：

1. **索引库只保留最后一次抓到的语言**，其他语言等于没做。  
2. 若多次变脸，可能触发 **“cloaking”或重复内容** 审查，整站可信度下降。  
3. 用户搜索关键词时，搜索引擎不知道该把哪门语言拿去排名，**排名分散或消失**。

---

### 谷歌官方原话（2023 文档）

> “Do not serve different locale variants from the same URL;  
> each language/region combination must have its own crawlable URL.”  
> —— [Google Search Central, Managing multi-regional sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites)

---

### 实战验证（1 分钟自查）

1. 打开 Search Console → Pages → 筛选 `/xxx.html`  
2. 看“Coverage”里是否提示：  
   - “Duplicate, Google chose different canonical than user”  
   - 或 “Crawled currently not indexed”  
3. 再看“HTML 预览”是不是有时英文、有时中文——如果有，说明蜘蛛已混乱。
