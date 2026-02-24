#!/bin/bash

# Alpha Hive GitHub Pages 快速部署脚本
# 使用方法：./deploy-to-github.sh <GitHub_Username> <Repository_Name>

set -e

echo "🐝 Alpha Hive - GitHub Pages 部署助手"
echo "=========================================="
echo ""

# 检查参数
if [ $# -lt 2 ]; then
    echo "❌ 用法错误"
    echo "使用方法: ./deploy-to-github.sh <GitHub用户名> <仓库名>"
    echo ""
    echo "示例: ./deploy-to-github.sh igg_wang748 alpha-hive-report"
    echo ""
    exit 1
fi

GITHUB_USER="$1"
REPO_NAME="$2"
REPO_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"

echo "📋 部署配置："
echo "  GitHub 用户: $GITHUB_USER"
echo "  仓库名: $REPO_NAME"
echo "  仓库地址: $REPO_URL"
echo ""

# 检查 Git 是否安装
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装！"
    echo "请先安装 Git: https://git-scm.com/download/mac"
    exit 1
fi

echo "✅ Git 已安装"
echo ""

# 初始化 Git 仓库
echo "🔧 初始化 Git 仓库..."
git init

# 配置 Git（如果还未配置）
if ! git config user.name &> /dev/null; then
    echo ""
    echo "⚙️ 首次使用 Git，需要配置用户信息"
    read -p "请输入你的 Git 用户名: " git_user
    read -p "请输入你的 Git 邮箱: " git_email
    git config user.name "$git_user"
    git config user.email "$git_email"
    echo "✅ Git 用户信息已配置"
fi

echo ""
echo "📦 添加文件..."
git add -A
echo "✅ 文件已添加"

echo ""
echo "💾 创建提交..."
git commit -m "🐝 Alpha Hive 投资简报 - $(date +%Y-%m-%d)"
echo "✅ 提交已创建"

echo ""
echo "🌐 连接到 GitHub 仓库..."
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"
echo "✅ 已连接到 $REPO_URL"

echo ""
echo "🚀 推送到 GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "=========================================="
echo "✅ 部署成功！"
echo "=========================================="
echo ""
echo "你的网页链接："
echo "  🌐 https://$GITHUB_USER.github.io/$REPO_NAME/"
echo ""
echo "完整链接（直接访问简报）："
echo "  📊 https://$GITHUB_USER.github.io/$REPO_NAME/alpha-hive-nvda-2026-02-23.html"
echo ""
echo "📝 后续步骤："
echo "  1. 等待 1-3 分钟，GitHub Pages 会自动生效"
echo "  2. 访问上面的链接验证部署"
echo "  3. 复制链接分享给朋友"
echo ""
echo "💡 提示："
echo "  - 如果链接还不生效，请清除浏览器缓存"
echo "  - 可以在 GitHub 仓库 Settings → Pages 中查看部署状态"
echo "  - 每次更新文件后，重新运行此脚本即可自动更新网页"
echo ""
echo "🐝 Happy Hiving!"
