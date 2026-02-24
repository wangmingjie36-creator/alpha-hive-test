# GitHub Pages 部署指南

## 方法 1：使用命令行（最快）

### 前提：已安装 Git 并配置 GitHub

```bash
# 1. 进入报告目录
cd /Users/igg/.claude/reports

# 2. 初始化 Git 仓库
git init

# 3. 添加文件
git add alpha-hive-nvda-2026-02-23.html
git add README.md

# 4. 首次提交
git commit -m "🐝 Alpha Hive 投资简报 - NVDA 2026-02-23"

# 5. 连接到 GitHub 仓库
# （替换 USERNAME 和 REPO_NAME）
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# 6. 推送到 GitHub
git branch -M main
git push -u origin main
```

### 然后在 GitHub 仓库设置中：
1. 进入 Settings → Pages
2. Source 选择 "Deploy from a branch"
3. Branch 选择 "main"
4. 保存

**你的网页链接**：
```
https://USERNAME.github.io/REPO_NAME/alpha-hive-nvda-2026-02-23.html
```

---

## 方法 2：网页上传（无需 Git）

### 如果没有安装 Git：

1. 访问 [GitHub](https://github.com/new) 创建新仓库
2. 仓库名：`alpha-hive-report`（或任意名字）
3. Description：`Alpha Hive 投资研究简报系统`
4. 选择 "Public"
5. 创建后，点击 "Add file" → "Upload files"
6. 选择上传：
   - `alpha-hive-nvda-2026-02-23.html`
   - `README.md`
   - `index.html`（可选，为了美化URL）

7. 进入 Settings → Pages
8. 选择 "Deploy from a branch" → main 分支
9. 保存

---

## 配置 index.html（使 URL 更简洁）

如果你想让链接变成：
```
https://USERNAME.github.io/alpha-hive-report/
```

而不是：
```
https://USERNAME.github.io/alpha-hive-report/alpha-hive-nvda-2026-02-23.html
```

你可以创建 `index.html` 文件，内容为：

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=alpha-hive-nvda-2026-02-23.html">
</head>
<body>
    <p>正在跳转到简报...</p>
</body>
</html>
```

---

## 最终链接格式

部署后，你可以分享这样的链接给朋友：

- **完整链接**：`https://USERNAME.github.io/alpha-hive-report/alpha-hive-nvda-2026-02-23.html`
- **简洁链接**（如配置了 index.html）：`https://USERNAME.github.io/alpha-hive-report/`

---

## 常见问题

**Q: 链接需要多久生效？**
A: 通常 1-3 分钟生效。如果不生效，清除浏览器缓存或等待 5 分钟。

**Q: 可以修改报告内容吗？**
A: 可以！直接编辑 HTML 文件后重新推送，GitHub Pages 会自动更新。

**Q: 有人可以修改我的报告吗？**
A: 不可以。仓库是你的，只有你有编辑权限。其他人只能查看。

**Q: 支持自定义域名吗？**
A: 支持！在 Settings → Pages 中可以配置自定义域名（需要自己购买域名）。

---

## 下一步

1. 按照上面的步骤部署
2. 获得你的 GitHub Pages 链接
3. 复制链接，分享给朋友！

有任何问题随时问我 ✨
