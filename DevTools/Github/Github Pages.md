+ [https://docs.github.com/en/pages](https://docs.github.com/en/pages)
+ [https://docs.github.com/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow](https://docs.github.com/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow)
+ gh-pages URL：`https://{username}.github.io/{repositoryname}/{path}`
+ 老版本：
    - 默认Github Actions（workflow是pages build and deployment）：选择一分支存放静态资源，path就是repository分支的路径
        * 记得静态资源得相对路径，即webpack的package.json`homepage`或者vite的vite.config.ts`base`的值是`./`亦或者是gh-pages URL/
        * 大概步骤jobs：工作目录`/home/runner/work/{repositoryname}/{repositoryname}`
            + build
                - 拉取docker镜像`docker pull ghcr.io/actions/jekyll-build-pages:v1.0.12`
                - 拉取代码，运行`use actions/checkout@v4`
                - 运行docker容器进行构建（因为比较复杂）`docker run`
                - 压缩构建目录`_site`为artifact且上传到blob storage，运行`actions/upload-pages-artifact@v3`
                    * 可以用`with: path: xxx`替换默认值`_site`
                - Post Checkout：还是`actions/checkout@v4`，对当前仓库push（虽然没有显示命令，但是在Github仓库文档中有提到）
            + deploy
                - 拉取artifact 运行：actions/deploy-pages@v4
+ 新版本：
    - 可以选择`/docs`目录（应该是新版本的）
    - 自定义Github Actions
        * 和默认的大概步骤差不多，不过如果比较简单，不需要docker镜像来构建



# 自定义NPM构建并部署
```yaml
name: deploy gitHub pages with npm and no push to branch

on:
  push:
    branches: ["main"]
  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# Sets permissions of the GITHUB_TOKEN to allow deployment to GitHub Pages
permissions:
  contents: read
  pages: write
  id-token: write

# Allow only one concurrent deployment, skipping runs queued between the run in-progress and latest queued.
# However, do NOT cancel in-progress runs as we want to allow these production deployments to complete.
concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: 安装node依赖&&构建node项目
        run: npm install && npm run build -- --outDir=./_site
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

```

