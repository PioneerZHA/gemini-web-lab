# Gemini Web Lab — 一些用 Gemini 写着玩的小网页

我用 Google Gemini 生成/协助生成了若干静态 HTML 小网站，觉得有意思就整理到一起挂在 GitHub Pages 上，方便随时访问、分享给朋友，也当作灵感和实验的存档。

这些页面主打“好玩”和“快速试验”。如果你点进来看到某些奇怪但有趣的东西，那就对了。

> 本 README 由 ChatGPT  根据仓库用途与作者描述撰写。


## 在线导航

- 主页是一个导航站，集中列出本仓库内所有页面入口。
- 每个页面都是纯静态 HTML，可直接在浏览器里打开。

访问方式：
- 导航主页：`https://pioneerzha.github.io/gemini-web-lab/`


## 仓库内容

你会在这里看到：
- `pages/`：所有具体的 HTML 页面（可能包含子目录）
- `index.html`：导航主页（列出所有页面入口）

整体特点：
- 无后端、无构建门槛，打开即用
- 每个页面相互独立，可以单独拷走或继续扩展
- 适合作为静态网页灵感集合或快速原型库


## 这些网页大概在做什么

每个页面的主题并不受限，可能包括但不限于：
- 小型交互/可视化 demo
- 轻量工具或玩具级应用
- 主题化的单页展示

它们共同点是：**由 Gemini 辅助生成、用于创意探索和个人兴趣记录**。  
如果你对某个页面的实现方式感兴趣，可以直接查看对应 HTML 源码。


## 如何使用 / 扩展（Fork 后的完整教程）

你可以：
1. 直接浏览页面并获取灵感  
2. 把其中某个页面复制走，改成你自己的版本  
3. 在此基础上新增更多页面，形成属于你的“网页合集”  

如果你也想做类似的静态页面集合，非常欢迎 Fork。以下是 Fork 之后从零开始使用的推荐流程。

### 1. Fork 到自己的 GitHub

- 右上角点击 **Fork**，把仓库复制到你自己的账号下。  
- Fork 完成后，你会得到一个新仓库：  
  `https://github.com/<your-username>/gemini-web-lab`  
- 你的仓库页面会显示 “forked from PioneerZHA/gemini-web-lab”。

### 2. 克隆你的 Fork 到本地

请务必克隆你自己的 Fork，而不是原仓库：

```bash
git clone https://github.com/<your-username>/gemini-web-lab.git
cd gemini-web-lab
```

### 3. 开启你自己的 GitHub Pages

1. 打开你 Fork 后的仓库  
2. 进入 **Settings → Pages**  
3. Source 选择 **GitHub Actions**（本仓库已内置自动部署工作流）  
4. 等待 Actions 首次运行成功后，你会得到自己的站点地址：

- 导航主页：  
  `https://<your-username>.github.io/gemini-web-lab/`

### 4. 新增你自己的页面

把新页面放到 `pages/` 目录下即可（支持子目录）：

```bash
# 示例：新增一个页面
echo "<h1>My New Page</h1>" > pages/my-new-page.html
```

然后提交并推送：

```bash
git add pages/my-new-page.html
git commit -m "Add my new page"
git push origin main
```

推送后会自动发生：
- GitHub Actions 运行 `tools/generate_index.py`
- 自动更新导航主页 `index.html`
- 自动部署到 GitHub Pages  

你无需手动修改导航主页。

### 5. 修改导航页样式（可选）

导航页由脚本自动生成，请不要手动编辑根目录的 `index.html`。  
如需改风格/布局，修改：

- `tools/generate_index.py`（模板与样式在里面）

改完后正常 commit + push，线上导航页会自动更新。

### 6. 同步上游更新（可选）

如果你 Fork 之后，还想把本仓库的新改动同步到你的版本：

1. 添加上游仓库：
   ```bash
   git remote add upstream https://github.com/PioneerZHA/gemini-web-lab.git
   ```

2. 拉取并合并：
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

3. 推送到你自己的仓库：
   ```bash
   git push origin main
   ```

这样你既保留自己的页面，也能拿到上游的脚本/结构更新。


## Fork 与贡献

欢迎任何形式的 Fork/二次创作：
- 你可以基于这个仓库结构整理你自己的页面合集
- 也可以对现有页面做改造、重混、再发布
- 如果你愿意把你的版本开源，我会很开心看到更多有趣的变体



## License

本项目采用 **MIT License**。  
你可以自由使用、修改、分发本仓库内容，只需保留原许可声明。  

---

如果你对某个页面的思路或实现细节好奇，欢迎提 Issue 交流。
