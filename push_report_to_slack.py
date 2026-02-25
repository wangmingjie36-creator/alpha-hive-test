#!/usr/bin/env python3
"""
📰 Alpha Hive 每日简报 → Slack 推送
自动将 Markdown 报告格式化为 Slack 消息并推送
"""

import json
import re
import urllib.request
from pathlib import Path
from datetime import datetime

def read_report(report_file):
    """读取 Markdown 报告"""
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

def extract_sections(report):
    """从报告中提取关键部分"""
    sections = {}

    # 提取标题
    title_match = re.search(r'# (.*)', report)
    sections['title'] = title_match.group(1) if title_match else "每日投资简报"

    # 提取摘要部分
    summary_match = re.search(r'## 📊 今日摘要.*?(?=##|$)', report, re.DOTALL)
    if summary_match:
        summary_text = summary_match.group(0)
        # 提取 Top 3
        items = re.findall(r'### \d+\. \*\*(.*?)\*\*.*?(?=###|$)', summary_text, re.DOTALL)
        sections['summary'] = items[:3] if items else []

    # 提取风险雷达
    risk_match = re.search(r'## ⚠️ 风险雷达\n\n(.*?)(?=##|$)', report, re.DOTALL)
    sections['risks'] = risk_match.group(1).strip() if risk_match and risk_match.group(1).strip() else "无重大风险"

    # 提取免责声明
    sections['disclaimer'] = "本报告为自动化数据分析，不构成投资建议"

    return sections

def build_slack_message(sections):
    """构建 Slack 消息"""

    # 构建摘要字段
    summary_fields = []
    if sections.get('summary'):
        for i, item in enumerate(sections['summary'][:3], 1):
            # 提取股票信息
            match = re.search(r'(.*?)[\s-]*(.*)', item)
            if match:
                ticker = match.group(1).strip()
                info = match.group(2).strip() if match.group(2) else "更新中..."
                summary_fields.append({
                    "title": f"{i}️⃣  {ticker}",
                    "value": info[:200],
                    "short": False
                })

    # 构建消息
    message = {
        "text": f"📰 {sections.get('title', '每日投资简报')}",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"📰 *{sections.get('title', '每日投资简报')}*\n\n🐝 Alpha Hive 自动化投资研究"
                }
            },
            {
                "type": "divider"
            }
        ],
        "attachments": [
            {
                "color": "#2E7D32",
                "title": "📊 今日 Top 3 机会",
                "fields": summary_fields if summary_fields else [
                    {"title": "Status", "value": "数据加载中...", "short": True}
                ],
                "footer": "🐝 Alpha Hive 智能告警系统",
                "ts": int(datetime.now().timestamp())
            },
            {
                "color": "#FFA500",
                "title": "⚠️ 风险提示",
                "text": sections.get('risks', '无重大风险'),
                "footer": sections.get('disclaimer', ''),
                "ts": int(datetime.now().timestamp())
            }
        ]
    }

    return message

def push_to_slack(message, webhook_url):
    """推送到 Slack"""
    try:
        data = json.dumps(message).encode('utf-8')
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')

        return result == 'ok'
    except Exception as e:
        print(f"❌ 推送失败: {e}")
        return False

def main():
    print("📰 Alpha Hive 每日简报推送\n")

    # 配置
    reports_dir = Path("/Users/igg/.claude/reports")
    webhook_file = Path.home() / '.alpha_hive_slack_webhook'

    # 读取 Webhook
    if not webhook_file.exists():
        print("❌ Slack Webhook 未配置")
        return False

    webhook_url = webhook_file.read_text().strip()

    # 找最新的报告
    report_files = list(reports_dir.glob("alpha-hive-daily-*.md"))
    if not report_files:
        print("❌ 未找到报告文件")
        return False

    # 排除 -FINAL 文件，选择最新的
    latest_report = sorted([f for f in report_files if '-FINAL' not in f.name])[-1]

    print(f"1️⃣  读取报告: {latest_report.name}")

    # 读取报告
    report = read_report(latest_report)
    if not report:
        print("❌ 无法读取报告")
        return False

    # 提取内容
    print("2️⃣  提取报告内容...")
    sections = extract_sections(report)

    # 构建消息
    print("3️⃣  构建 Slack 消息...")
    message = build_slack_message(sections)

    # 推送
    print("4️⃣  推送到 Slack...")
    success = push_to_slack(message, webhook_url)

    if success:
        print("\n" + "=" * 60)
        print("✅ ✅ ✅ 每日简报已推送到 Slack！✅ ✅ ✅")
        print("=" * 60)
        print(f"\n📰 报告: {latest_report.name}")
        print(f"📍 频道: {webhook_url.split('/')[-2]}")
        return True
    else:
        print("\n❌ 推送失败")
        return False

if __name__ == '__main__':
    main()
