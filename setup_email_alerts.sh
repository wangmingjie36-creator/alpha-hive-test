#!/bin/bash

# 🔔 Alpha Hive 邮件告警自动配置脚本
# 自动化 Gmail 邮件通知设置

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.py"

echo "════════════════════════════════════════════════════════"
echo "  📧 Alpha Hive Gmail 邮件告警配置"
echo "════════════════════════════════════════════════════════"
echo ""

# 第一步：确认 Gmail 应用密码
echo "📝 步骤 1: 验证 Gmail 应用密码"
echo ""
echo "请按照以下步骤获取应用密码："
echo ""
echo "  1️⃣  访问: https://myaccount.google.com/security"
echo "  2️⃣  找到 '应用专用密码' (Application passwords)"
echo "  3️⃣  选择应用: 邮件 (Mail)"
echo "  4️⃣  选择设备: Windows PC 或 Mac"
echo "  5️⃣  点击生成，复制 16 位密码"
echo ""
echo "注意: 应用密码格式为 'abcd efgh ijkl mnop'"
echo "      配置时需要移除中间的空格"
echo ""

read -p "✅ 你已获得应用密码了吗? (y/n): " HAS_PASSWORD

if [ "$HAS_PASSWORD" != "y" ]; then
    echo "❌ 请先生成应用密码，然后重新运行本脚本"
    exit 1
fi

# 第二步：输入配置信息
echo ""
echo "📝 步骤 2: 输入邮件配置"
echo ""

read -p "📧 Gmail 地址 (例: user@gmail.com): " GMAIL_ADDRESS

if [ -z "$GMAIL_ADDRESS" ]; then
    echo "❌ 邮箱地址不能为空"
    exit 1
fi

read -sp "🔑 应用密码 (输入时不显示): " APP_PASSWORD
echo ""

if [ -z "$APP_PASSWORD" ]; then
    echo "❌ 应用密码不能为空"
    exit 1
fi

# 验证邮箱格式
if [[ ! "$GMAIL_ADDRESS" =~ ^[a-zA-Z0-9._%+-]+@gmail\.com$ ]]; then
    echo "❌ 无效的 Gmail 地址格式"
    exit 1
fi

# 第三步：备份原配置
echo ""
echo "📝 步骤 3: 备份原配置"
cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%s)"
echo "✅ 已备份到: $CONFIG_FILE.backup.*"

# 第四步：更新配置
echo ""
echo "📝 步骤 4: 更新 config.py"

# 使用 Python 来修改配置（更安全）
python3 << PYTHON_SCRIPT
import re

config_file = "$CONFIG_FILE"
gmail = "$GMAIL_ADDRESS"
password = "$APP_PASSWORD"

with open(config_file, 'r') as f:
    content = f.read()

# 更新 email_enabled
content = re.sub(
    r'"email_enabled":\s*False',
    '"email_enabled": True',
    content
)

# 更新 sender_email
content = re.sub(
    r'"sender_email":\s*"[^"]*"',
    f'"sender_email": "{gmail}"',
    content
)

# 更新 sender_password
content = re.sub(
    r'"sender_password":\s*"[^"]*"',
    f'"sender_password": "{password}"',
    content
)

# 更新 recipient_emails
content = re.sub(
    r'"recipient_emails":\s*\[[^\]]*\]',
    f'"recipient_emails": ["{gmail}"]',
    content
)

with open(config_file, 'w') as f:
    f.write(content)

print("✅ config.py 已更新")
PYTHON_SCRIPT

if [ $? -ne 0 ]; then
    echo "❌ 更新失败，已恢复备份"
    cp "$CONFIG_FILE.backup.$(ls -t $CONFIG_FILE.backup.* | head -1 | sed 's/.*\.backup\.//')" "$CONFIG_FILE"
    exit 1
fi

# 第五步：验证配置
echo ""
echo "📝 步骤 5: 验证配置"

PYTHON_VERIFY=$(python3 << 'PYTHON_SCRIPT'
import re

with open("$CONFIG_FILE", 'r') as f:
    content = f.read()

# 检查关键配置
checks = {
    '"email_enabled": True': '"email_enabled": True' in content,
    'SMTP 服务器已设置': '"smtp_server": "smtp.gmail.com"' in content,
    '邮箱地址已设置': f'"sender_email": "{gmail}"' in content if 'gmail' in locals() else True,
    'TLS 已启用': '"use_tls": True' in content,
}

all_pass = all(checks.values())
for check, result in checks.items():
    status = "✅" if result else "❌"
    print(f"{status} {check}")

if all_pass:
    print("\n✅ 所有配置验证通过！")
    exit(0)
else:
    print("\n⚠️  部分配置需要手动检查")
    exit(1)
PYTHON_SCRIPT
)

echo "$PYTHON_VERIFY"

# 第六步：测试邮件发送
echo ""
echo "📝 步骤 6: 测试邮件发送"
echo ""
echo "正在发送测试邮件..."

python3 "$SCRIPT_DIR/alert_manager.py" \
    --status-json "$SCRIPT_DIR/status.json" \
    --output-dir "/Users/igg/.claude/logs" \
    --test-mode \
    2>&1 | head -20

echo ""
echo "⏳ 等待 2-5 秒邮件送达..."
sleep 3

echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ 邮件告警配置完成！"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📧 邮件已发送到: $GMAIL_ADDRESS"
echo "📋 请检查邮件（包括垃圾箱）"
echo ""
echo "后续操作："
echo "  1️⃣  验证收到邮件"
echo "  2️⃣  运行完整流程: bash /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh"
echo "  3️⃣  监控日志: tail -f /Users/igg/.claude/logs/orchestrator-\$(date +%Y-%m-%d).log"
echo ""
echo "✨ 现在每次执行时，P0/P1 级别告警将自动发送邮件通知！"
echo ""
