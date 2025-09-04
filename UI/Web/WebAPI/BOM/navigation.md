# clipboard

```js
      (async () => {
        try {
          /* 1. 把你想粘出去的 Markdown 先渲染成 HTML（这里硬编码了） */
          const html = `
        <meta charset='utf-8'>
        <h1>标题</h1>
        <p>这是 <strong>粗体</strong> 和 <em>斜体</em>。</p>
        <pre><code>console.log('Hello, world!');</code></pre>
      `;

          /* 2. 构造一个 Blob（text/html） */
          const htmlBlob = new Blob([html], { type: "text/html" });

          /* 3. 再补一份纯文本，避免纯文本环境一片空白 */
          const plainBlob = new Blob(
            ["标题\n这是 粗体 和 斜体。\nconsole.log('Hello, world!');"],
            { type: "text/plain" }
          );

          /* 4. 写入剪贴板 */
          const clipboardItem = new ClipboardItem({
            "text/html": htmlBlob,
            "text/plain": plainBlob,
          });

          await navigator.clipboard.write([clipboardItem]);
          console.log("已写入剪贴板！去 Medium 里粘贴试试。");
        } catch (e) {
          console.error("写入剪切板失败", e);
        }
      })();
```