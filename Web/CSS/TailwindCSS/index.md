
# 配置
## 使用PostCSS
- `npm install -D tailwindcss postcss autoprefixer`
- `npx tailwindcss init -p`：创建tailwind.config.js、postcss.config.js（-p）
```js
module.exports = {
  plugins: {
    /*
      tailwind.config.js路径 或者 config对象，
      默认./tailwind.config.[m][js|ts]
    */
    tailwindcss: {}, 
    autoprefixer: {},
  }
}
```


## TailwindCLI
- `npm install -D tailwindcss`
- `npx tailwindcss -i ./src/input.css -o ./src/output.css --watch`

## CDN
- [Try Tailwind CSS using the Play CDN - TailwindCSS中文文档 | TailwindCSS中文网](https://www.tailwindcss.cn/docs/installation/play-cdn)


## v4 vite
- `npm install tailwindcss @tailwindcss/vite`
```js
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
})
```

## 应用编译css
- 导入input.css（使用Tailwindcss CLI时用output.css）
	- 直接在根组件中导入该文件
	- 或者在index.html`<link href="/src/input.css" rel="stylesheet">`


# 入门

- 生成类`text-2xl`，[任意值](https://v3.tailwindcss.com/docs/adding-custom-styles#using-arbitrary-values)`text-[20rem]`

# 分层设计
- [分层设计](https://v3.tailwindcss.com/docs/adding-custom-styles)：base、components、utilities
	- 特点
		- css按tailwind分层顺序进行编译输出，可覆盖（utilities（原子化css，corePlugin）可覆盖components（class），按上面顺序进行覆盖，）
		- 只有有应用过的才会输出在编译的css中
		- 只有tailwindcss分层中的类才能用modifier，普通css无法用
		- [也允许使用多css文件，不过不推荐](https://v3.tailwindcss.com/docs/adding-custom-styles#using-multiple-css-files)
		- 如Vue这样的组件内的style无法使用tailwindcss分层
- [第三方则使用Plugin来给分层添加代码](https://v3.tailwindcss.com/docs/adding-custom-styles#writing-plugins)：可以不用`@layer`，而是直接在tailwindcss.config.js中写自己的plugin
- [@xxx是指令，theme()、screen()是函数](https://v3.tailwindcss.com/docs/functions-and-directives)
```css
/* 使用tailwind指令来开启指定层（顺序无所谓），会收集所有包括tailwind、插件、自己的 */
/* 设置html元素 */
@tailwind base;
/* 添加自定义类（就是原本的css类），一般都不会这个 */
@tailwind components; 
/* 添加完全自定义的原子类，与components区别只是在components后，可以进行覆盖 */
@tailwind utilities;

/* 
以上可以直接（不过有点不太稳定）
@import "tailwindcss/tailwind.css";
或者
@import "../node_modules/tailwindcss/tailwind.css";
但是由于tailwindcss3没有index.css，因此无法@import "tailwindcss";
*/

/* 自定义modifier，仅在插件或者theme中 */
@tailwind variants;


/* 在base层添加代码 */
@layer base{
  ...
  h1{
    /* 使用@apply引用tailwind */
    @apply text-2xl;
    /* 引用自定义的theme */
    font-size: theme(fontSize.2x);
  }
  /* 媒体查询 */
  @media screen(sm) { /* ... */ }
}

@layer components{
  .xx{}
}
@layer utilities{
  .xx{}
}


/* @import必须在@config前 */
@import "tailwindcss/utilities"; 

/* 指定其他配置文件 */
@config "./tailwind.admin.config.js";
```
# modifier
- https://v3.tailwindcss.com/docs/hover-focus-and-other-states
- [自定义modifier --  variants](https://www.tailwindcss.cn/docs/plugins#static-variants)

# tailwind.config.js
- [content](https://v3.tailwindcss.com/docs/configuration#content)：扫描文件路径的glob
	- 值一般是`["./index.html", "./src/**/*.{js,ts,jsx,tsx}"]`
- [prefix](https://v3.tailwindcss.com/docs/configuration#prefix)：为tailwindcss添加前缀
- [separator](https://v3.tailwindcss.com/docs/configuration#separator)：设置分隔符，默认`:`
	- 如`focus:outline-none`
- [important](https://v3.tailwindcss.com/docs/configuration#important)：如果为true则表示所有tailwindcss都会加上`important!`
- [presets](https://v3.tailwindcss.com/docs/presets)：完全自定义tailwind.config.js
	- 项目的tailwind.config.js会与[tailwindcss/stubs/config.full.js at v3.4.17](https://github.com/tailwindlabs/tailwindcss/blob/v3.4.17/stubs/config.full.js)进行合并
- [corePlugins](https://v3.tailwindcss.com/docs/configuration#core-plugins)：完全禁用某些corePlugin
	- 里面还列出了所有corePlugin
- [theme](https://v3.tailwindcss.com/docs/theme)：自定义 [screens](https://v3.tailwindcss.com/docs/theme#screens)、[colors](https://v3.tailwindcss.com/docs/theme#colors)、[spacing](https://v3.tailwindcss.com/docs/theme#spacing)、[corePlugins](https://v3.tailwindcss.com/docs/theme#configuration-reference)
	- 可以覆盖默认、扩展默认、引用自定义theme中的其他值或者默认、禁用corePlguin
	- 如`w-2x`（自定义spacing.2x=xxx）
-  [plugins](https://v3.tailwindcss.com/docs/configuration#plugins)：应用插件，使用插件提供的base、component等
