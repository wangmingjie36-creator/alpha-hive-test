#!/usr/bin/env python3
"""
🚀 Agent Workflow 演示 - 展示 Agent Toolbox 的完整集成
文件系统 + GitHub + 通知的统一工作流
"""

from agent_toolbox import AgentHelper, FilesystemTool
from alpha_hive_daily_report import AlphaHiveDailyReporter
import json


def demo_filesystem():
    """演示文件系统功能"""
    print("\n" + "=" * 70)
    print("📁 演示 1：文件系统操作")
    print("=" * 70)

    helper = AgentHelper()

    # 列出报告目录
    print("\n🔍 列出报告目录...")
    files = helper.fs.list_directory("/Users/igg/.claude/reports")
    py_files = [f for f in files if f["name"].endswith(".py")]
    print(f"✅ 找到 {len(py_files)} 个 Python 文件")
    for f in py_files[:5]:
        print(f"   - {f['name']}")

    # 搜索文件
    print("\n🔎 搜索包含 'swarm' 的文件...")
    results = helper.fs.search_files("swarm", "/Users/igg/.claude/reports")
    print(f"✅ 找到 {len(results)} 个文件")
    for f in results[:5]:
        print(f"   - {f.split('/')[-1]}")

    # 读取文件
    print("\n📖 读取 SWARM_QUICK_START.md...")
    try:
        content = helper.fs.read_file("/Users/igg/.claude/reports/SWARM_QUICK_START.md")
        lines = content.split("\n")
        print(f"✅ 成功读取 {len(lines)} 行")
        print(f"   开头: {lines[0][:60]}...")
    except Exception as e:
        print(f"⚠️ {e}")

    # 写入文件
    print("\n✍️  创建新文件...")
    test_content = f"""# 🤖 Agent Toolbox 测试报告
生成时间：{helper.notify._load_slack_webhook()}
测试内容：此文件由 agent_toolbox 自动生成
"""
    try:
        result = helper.fs.write_file(
            "/tmp/agent_test_report.md",
            test_content
        )
        print(f"✅ {result}")
    except Exception as e:
        print(f"⚠️ {e}")


def demo_github():
    """演示 GitHub 操作"""
    print("\n" + "=" * 70)
    print("🐙 演示 2：GitHub 操作")
    print("=" * 70)

    helper = AgentHelper()

    # Git 状态
    print("\n📊 检查 Git 状态...")
    status = helper.git.status()
    modified_count = len(status.get("modified_files", []))
    print(f"✅ 修改的文件数：{modified_count}")
    if modified_count > 0:
        print(f"   状态：{status.get('status')}")
        for f in status.get("modified_files", [])[:3]:
            print(f"   - {f}")

    # 列出分支
    print("\n🌿 列出所有分支...")
    branches = helper.git.list_branches()
    print(f"✅ 找到 {len(branches.get('branches', []))} 个分支")
    for b in branches.get("branches", [])[:5]:
        print(f"   {b}")

    # 查看最近的 diff
    print("\n📝 查看最近改动...")
    try:
        diff = helper.git.diff("HEAD~1", "HEAD")
        stats = diff.get("stats", {})
        print(f"✅ 最近提交统计：")
        print(f"   + {stats.get('additions', 0)} 行添加")
        print(f"   - {stats.get('deletions', 0)} 行删除")
    except Exception as e:
        print(f"⚠️ {e}")


def demo_notifications():
    """演示通知功能"""
    print("\n" + "=" * 70)
    print("🔔 演示 3：通知系统")
    print("=" * 70)

    helper = AgentHelper()

    # 发送 Slack 消息
    print("\n💬 发送 Slack 消息...")
    result = helper.notify.send_slack_message(
        "#alpha-hive",
        "🤖 Agent Toolbox 演示消息\n✅ 文件系统 + GitHub + 通知已集成"
    )
    if result.get("success"):
        print(f"✅ 消息已发送到 Slack")
    else:
        print(f"ℹ️ {result.get('error', '未配置或连接失败')}")


def demo_full_workflow():
    """演示完整的蜂群系统工作流"""
    print("\n" + "=" * 70)
    print("🐝 演示 4：完整蜂群工作流 + Agent Toolbox")
    print("=" * 70)

    reporter = AlphaHiveDailyReporter()

    print("\n1️⃣ 运行蜂群扫描...")
    print("   (使用 NVDA 单标的快速演示)")

    # 运行快速蜂群扫描
    report = reporter.run_swarm_scan(focus_tickers=["NVDA"])

    print("\n2️⃣ 保存报告...")
    report_path = reporter.save_report(report)
    print(f"✅ 报告已保存：{report_path}")

    print("\n3️⃣ 自动提交 + 通知...")
    results = reporter.auto_commit_and_notify(report)

    # 展示结果
    print("\n4️⃣ 工作流完成状态：")
    print(f"   ✅ Git 提交：{results.get('git_commit', {}).get('success', False)}")
    print(f"   ✅ Git 推送：{results.get('git_push', {}).get('success', False)}")
    print(f"   ✅ Slack 通知：{results.get('slack_notification', {}).get('success', False)}")


def print_summary():
    """打印汇总信息"""
    print("\n" + "=" * 70)
    print("✨ Agent Toolbox 集成完成")
    print("=" * 70)

    print("""
🚀 已集成的功能：

1️⃣ 文件系统操作
   - 读/写/列表/搜索本地文件
   - 自动路径安全检查
   - 支持批量操作

2️⃣ GitHub 集成
   - Git 提交/推送/查看差异
   - 分支管理
   - 状态检查

3️⃣ 通知系统
   - Slack 消息发送
   - 邮件通知
   - 多渠道支持

4️⃣ 蜂群系统增强
   - 自动 Git 提交报告
   - 自动 Slack 通知
   - 完全自动化工作流

📊 使用示例：

# 快速启动
python3 -c "
from agent_toolbox import AgentHelper
helper = AgentHelper()
files = helper.fs.list_directory('/Users/igg/.claude/reports')
status = helper.git.status()
helper.notify.send_slack_message('#alpha-hive', '🤖 自动化运行中')
"

# 完整演示
python3 demo_agent_workflow.py

# 集成到蜂群系统
python3 alpha_hive_daily_report.py --swarm --tickers NVDA --auto-notify

🎯 下一步：

✅ 已完成：Agent Toolbox（Python-native MCP）
⏳ 中期：Docker 化部分模块
⏳ 后期：升级为真正的 MCP 服务器（当 Node.js 可用时）

📚 文档：
- agent_toolbox.py - 核心实现
- SWARM_QUICK_START.md - 快速开始
- demo_agent_workflow.py - 本演示脚本
""")


def main():
    """主入口"""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " 🚀 Agent Toolbox 完整集成演示 ".center(68) + "║")
    print("╚" + "=" * 68 + "╝")

    try:
        demo_filesystem()
        demo_github()
        demo_notifications()
        demo_full_workflow()
        print_summary()

        print("\n✅ 所有演示完成！")
        print("🎉 Agent Toolbox 已准备好！\n")

    except Exception as e:
        print(f"\n❌ 演示出错：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
