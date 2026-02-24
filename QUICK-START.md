# 🚀 GitHub Pages 部署 - 快速开始

> 3 分钟内完成部署，获得可分享的链接！

---

## ⚡ 最快方法（使用脚本）

### 前提条件
- ✅ 安装了 Git
- ✅ 有 GitHub 账号

### 3 个命令搞定

```bash
# 1. 赋予脚本执行权限
chmod +x /Users/igg/.claude/reports/deploy-to-github.sh

# 2. 运行部署脚本
/Users/igg/.claude/reports/deploy-to-github.sh <GitHub用户名> <仓库名>

# 示例：
/Users/igg/.claude/reports/deploy-to-github.sh igg_wang748 alpha-hive-report
```

### 脚本会自动：
- ✅ 初始化 Git 仓库
- ✅ 配置 Git 用户信息
- ✅ 添加所有文件
- ✅ 创建提交
- ✅ 推送到 GitHub
- ✅ 显示你的最终链接

**完成！** 等待 1-3 分钟，你就有可分享的链接了 🎉

---

## 📋 详细步骤（如果脚本不工作）

### Step 1: 创建 GitHub 仓库

1. 访问 [GitHub 新建仓库页面](https://github.com/new)
2. 仓库名：`alpha-hive-report`
3. 描述：`Alpha Hive 投资研究简报`
4. 选择 **Public**（这样别人才能看到）
5. 点击 **Create repository**

### Step 2: 本地推送代码

打开终端，执行：

```bash
cd /Users/igg/.claude/reports

# 初始化 Git
git init

# 配置用户信息（首次使用）
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 添加文件
git add .

# 创建提交
git commit -m "🐝 Alpha Hive 投资简报"

# 连接到 GitHub（替换 USERNAME 和 REPO_NAME）
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# 推送代码
git branch -M main
git push -u origin main
```

### Step 3: 启用 GitHub Pages

1. 进入你的 GitHub 仓库
2. 点击 **Settings**
3. 左侧菜单找到 **Pages**
4. **Source** 下拉选择 **Deploy from a branch**
5. **Branch** 选择 **main**
6. 点击 **Save**

### Step 4: 等待部署

- 等待 1-3 分钟
- 你会看到绿色的部署成功提示
- 你的网址会显示在 Pages 设置中

---

## 🔗 获取你的链接

部署完成后，你的网页链接是：

```
https://USERNAME.github.io/REPO_NAME/
```

**具体例子**（替换你的用户名和仓库名）：

- 首页（推荐分享）：
  `https://USERNAME.github.io/alpha-hive-report/`

- 直接链接简报：
  `https://USERNAME.github.io/alpha-hive-report/alpha-hive-nvda-2026-02-23.html`

---

## ✅ 验证部署

1. 打开你的链接
2. 看到 Alpha Hive 简报了吗？✅
3. 完美！可以分享给朋友了 🎉

---

## 🔄 更新简报

每次生成新简报时：

```bash
cd /Users/igg/.claude/reports

# 添加新文件
git add .

# 提交
git commit -m "🐝 Alpha Hive 投资简报 - $(date +%Y-%m-%d)"

# 推送
git push origin main
```

GitHub Pages 会自动更新！无需再配置 ✨

---

## 🆘 常见问题

### Q: 链接还不能访问？
**A:**
- 清除浏览器缓存（Cmd + Shift + Delete）
- 等待 5-10 分钟
- 检查 GitHub 仓库 Settings → Pages 中的部署状态

### Q: Push 时要求输入密码？
**A:**
GitHub 现在不再接受密码，改用 **Personal Access Token**：
1. 访问 https://github.com/settings/tokens
2. 生成新 token（勾选 `repo` 权限）
3. 复制 token
4. 当要求输入密码时，粘贴 token
5. 或使用 SSH 密钥：https://github.com/settings/keys

### Q: 部署失败？
**A:**
运行这个命令查看详细错误：
```bash
git push -u origin main -v
```

### Q: 可以使用自定义域名吗？
**A:**
可以！在 Settings → Pages 中，**Custom domain** 部分添加你的域名。需要修改域名 DNS 设置。

### Q: 有人能修改我的报告吗？
**A:**
不能。仓库是你的私产，只有你有编辑权限。其他人只能查看。

---

## 📞 需要帮助？

如果遇到问题，可以：

1. 检查 Git 是否正确安装：`git --version`
2. 检查 GitHub 账号登录状态
3. 查看 GitHub 官方文档：https://docs.github.com/pages

---

## 🎉 完成了！

现在你有：

- ✅ 一个可分享的链接
- ✅ 专业的网页版简报
- ✅ 完全免费的托管
- ✅ 自动更新的系统

**去分享给你的朋友吧！** 🚀

---

**下一步**：

```bash
# 快速部署一行命令
/Users/igg/.claude/reports/deploy-to-github.sh <你的GitHub用户名> alpha-hive-report
```

或按照上面的详细步骤手动操作。

祝你部署顺利！🐝✨
