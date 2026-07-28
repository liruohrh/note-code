- `.github/workflows/xxx.yml`每个yml都是一个workflows
- https://docs.github.com/en/actions

# 部署github pages例子
```yml
name: build and delopy  
on:  
  push:  
    branches:  
      - main  
permissions:  
  contents: write  
jobs:  
  build:  
    name: npm构建vite项目  
    runs-on: ubuntu-latest  
    steps:  
      - name: 用git拉取项目  
        uses: actions/checkout@v4  
      - run: pwd && ls -al  
      - name: 安装node依赖&&构建node项目  
        run: npm install && npm run build  
      - name: 部署github pages  
        uses: JamesIves/github-pages-deploy-action@v4  
        with:  
          branch: gh-pages  
          folder: dist  
```
# 配置参考
```yml
name: "Upload GitHub Pages artifact"  
description: "A composite action that prepares your static assets to be deployed to GitHub Pages"  
author: "GitHub"  
​  
jobs:  
  build:  
    name: npm构建vite项目  
    runs-on: ubuntu-latest  
    steps:  
      - name: 安装node依赖&&构建node项目  
        run: npm install && npm run build  
      - name: 部署github pages  
        uses: actions/upload-pages-artifact@v3  
        with:  
          name: gh-pages  
          path: dist  
​  
inputs:  
  path:  
    description: "Path of the directory containing the static assets."  
    required: true  
    default: "_site/"  
outputs:  
  artifact_id:  
    description: "The ID of the artifact that was uploaded."  
    value: ${{ steps.upload-artifact.outputs.artifact-id }}  
runs:  
  using: composite  
  steps:  
    - name: Archive artifact  
      shell: bash  
      if: runner.os == 'Windows'  
      run: ehco 123  
      env:  
        INPUT_PATH: ${{ inputs.path }}  
    - name: Upload artifact  
      id: upload-artifact  
      uses: actions/upload-artifact@v4  
      with:  
        name: ${{ inputs.name }}  
        path: ${{ runner.temp }}/artifact.tar  
        retention-days: ${{ inputs.retention-days }}  
        if-no-files-found: error
```