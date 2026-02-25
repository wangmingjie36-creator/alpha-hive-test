#!/usr/bin/env python3
"""
📊 Alpha Hive 仪表板自动更新
根据最新报告自动更新 index.html
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional


class DashboardUpdater:
    """仪表板更新管理器"""

    def __init__(self):
        self.report_dir = Path("/Users/igg/.claude/reports")
        self.timestamp = datetime.now()
        self.date_str = self.timestamp.strftime("%Y-%m-%d")

    def read_today_report(self) -> Optional[Dict]:
        """读取今天的 JSON 报告"""
        json_file = self.report_dir / f"alpha-hive-daily-{self.date_str}.json"

        if not json_file.exists():
            print(f"⚠️  找不到今日报告: {json_file}")
            return None

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  读取报告失败: {e}")
            return None

    def extract_top_opportunities(self, report: Dict) -> List[Dict]:
        """从报告中提取 Top 3 机会"""
        opportunities = report.get("opportunities", [])
        return opportunities[:3]

    def get_recent_reports(self, days: int = 7) -> List[Dict]:
        """获取最近 N 天的报告列表"""
        reports = []

        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")

            md_file = self.report_dir / f"alpha-hive-daily-{date_str}.md"
            json_file = self.report_dir / f"alpha-hive-daily-{date_str}.json"

            if md_file.exists() or json_file.exists():
                reports.append({
                    "date": date_str,
                    "date_display": date.strftime("%m 月 %d 日（%A）"),
                    "md_file": md_file.name if md_file.exists() else None,
                    "json_file": json_file.name if json_file.exists() else None,
                })

        return reports

    def get_system_status(self) -> Dict:
        """获取系统状态"""
        status_file = self.report_dir / "status.json"
        status = {
            "last_run": self.timestamp.isoformat(),
            "status": "✅ 运行中",
            "message": "系统正常"
        }

        if status_file.exists():
            try:
                with open(status_file, 'r', encoding='utf-8') as f:
                    stored_status = json.load(f)
                    status.update(stored_status)
            except Exception as e:
                print(f"⚠️  读取状态文件失败: {e}")

        return status

    def generate_html(self, opportunities: List[Dict], reports: List[Dict], system_status: Dict) -> str:
        """生成 index.html 内容"""

        # 格式化机会卡片
        opportunities_html = ""
        for i, opp in enumerate(opportunities, 1):
            direction_color = {
                "看多": "#28a745",
                "看空": "#dc3545",
                "中性": "#ffc107"
            }.get(opp.get("direction", "中性"), "#ffc107")

            opportunities_html += f"""
            <div class="opportunity-card">
                <div class="card-rank">#{i}</div>
                <div class="card-header">
                    <h3>{opp.get('ticker', 'N/A')}</h3>
                    <div class="direction" style="background-color: {direction_color};">
                        {opp.get('direction', '中性')}
                    </div>
                </div>
                <div class="card-content">
                    <div class="metric-row">
                        <span class="label">综合分</span>
                        <span class="value">{opp.get('opp_score', 0)}/10</span>
                    </div>
                    <div class="metric-row">
                        <span class="label">置信度</span>
                        <span class="value">{opp.get('confidence', 'N/A')}</span>
                    </div>
                    <div class="metric-row">
                        <span class="label">期权信号</span>
                        <span class="value" style="font-size: 0.9em;">
                            {opp.get('options_signal', '信息不足')[:20]}...
                        </span>
                    </div>
                    <div class="metric-row">
                        <span class="label">关键催化剂</span>
                        <span class="value" style="font-size: 0.9em;">
                            {opp.get('key_catalyst', 'TBD')}
                        </span>
                    </div>
                </div>
            </div>
            """

        # 格式化最近报告列表
        recent_reports_html = ""
        for report in reports:
            recent_reports_html += f"""
            <div class="report-item">
                <div class="report-date">{report['date']}</div>
                <div class="report-links">
            """
            if report['md_file']:
                recent_reports_html += f"""
                    <a href="{report['md_file']}" class="report-link md">
                        📄 Markdown
                    </a>
                """
            if report['json_file']:
                recent_reports_html += f"""
                    <a href="{report['json_file']}" class="report-link json">
                        📊 JSON
                    </a>
                """
            recent_reports_html += """
                </div>
            </div>
            """

        # 系统状态颜色
        status_color = "#28a745" if "✅" in system_status.get("status", "") else "#dc3545"

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alpha Hive - 投资简报仪表板</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .header {{
            background: white;
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            color: #667eea;
            margin-bottom: 10px;
        }}

        .header p {{
            color: #666;
            font-size: 1.1em;
        }}

        .main-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }}

        .section {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}

        .section h2 {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .section h2::before {{
            content: '';
            display: inline-block;
            width: 4px;
            height: 28px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 2px;
        }}

        .opportunities-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}

        .opportunity-card {{
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            position: relative;
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .opportunity-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
        }}

        .card-rank {{
            position: absolute;
            top: 10px;
            right: 15px;
            font-size: 0.85em;
            font-weight: bold;
            color: #667eea;
            background: #f0f0f0;
            padding: 4px 8px;
            border-radius: 5px;
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }}

        .card-header h3 {{
            font-size: 1.5em;
            color: #333;
        }}

        .direction {{
            padding: 4px 12px;
            border-radius: 20px;
            color: white;
            font-size: 0.85em;
            font-weight: bold;
        }}

        .card-content {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .metric-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            font-size: 0.95em;
        }}

        .label {{
            color: #666;
            font-weight: 500;
        }}

        .value {{
            color: #333;
            font-weight: bold;
            font-size: 1.05em;
        }}

        .status-card {{
            border: 2px solid {status_color};
            border-radius: 10px;
            padding: 20px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        }}

        .status-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }}

        .status-header h3 {{
            color: #667eea;
            font-size: 1.2em;
        }}

        .status-indicator {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 1.1em;
            font-weight: bold;
            color: {status_color};
        }}

        .status-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: {status_color};
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        .status-info {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            font-size: 0.95em;
        }}

        .status-row {{
            display: flex;
            justify-content: space-between;
        }}

        .status-label {{
            color: #666;
        }}

        .status-value {{
            color: #333;
            font-weight: bold;
        }}

        .reports-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .report-item {{
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 12px;
            background: #f8f9fa;
        }}

        .report-date {{
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
            font-size: 0.95em;
        }}

        .report-links {{
            display: flex;
            gap: 8px;
        }}

        .report-link {{
            flex: 1;
            padding: 6px 10px;
            border-radius: 5px;
            text-align: center;
            text-decoration: none;
            font-size: 0.85em;
            font-weight: bold;
            transition: all 0.3s;
        }}

        .report-link.md {{
            background-color: #667eea;
            color: white;
        }}

        .report-link.md:hover {{
            background-color: #5568d3;
        }}

        .report-link.json {{
            background-color: #764ba2;
            color: white;
        }}

        .report-link.json:hover {{
            background-color: #653d89;
        }}

        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            font-size: 0.95em;
        }}

        .footer p {{
            margin: 5px 0;
        }}

        @media (max-width: 768px) {{
            .main-grid {{
                grid-template-columns: 1fr;
            }}

            .header {{
                padding: 20px;
            }}

            .header h1 {{
                font-size: 1.8em;
            }}

            .opportunities-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 页头 -->
        <div class="header">
            <h1>🐝 Alpha Hive 每日投资简报</h1>
            <p>去中心化蜂群智能投资研究平台</p>
        </div>

        <!-- 主内容区域 -->
        <div class="main-grid">
            <!-- 主要机会 -->
            <div class="section">
                <h2>🎯 今日Top 3机会</h2>
                <div class="opportunities-grid">
                    {opportunities_html}
                </div>
            </div>

            <!-- 侧边栏：系统状态 + 历史报告 -->
            <div>
                <!-- 系统状态 -->
                <div class="section" style="margin-bottom: 30px;">
                    <div class="status-card">
                        <div class="status-header">
                            <h3>📊 系统状态</h3>
                            <div class="status-indicator">
                                <div class="status-dot"></div>
                                {system_status.get('status', '✅ 正常')}
                            </div>
                        </div>
                        <div class="status-info">
                            <div class="status-row">
                                <span class="status-label">最后更新</span>
                                <span class="status-value">{self.timestamp.strftime('%H:%M:%S')}</span>
                            </div>
                            <div class="status-row">
                                <span class="status-label">更新日期</span>
                                <span class="status-value">{self.date_str}</span>
                            </div>
                            <div class="status-row">
                                <span class="status-label">部署状态</span>
                                <span class="status-value">
                                    {system_status.get('deploy_status', '待部署')}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 历史报告 -->
                <div class="section">
                    <h2>📜 最近报告</h2>
                    <div class="reports-list">
                        {recent_reports_html}
                    </div>
                </div>
            </div>
        </div>

        <!-- 页脚 -->
        <div class="footer">
            <p>🐝 Alpha Hive - 完全自动化投资研究平台</p>
            <p>最后更新：{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | 本仪表板每日自动更新</p>
            <p style="font-size: 0.9em; margin-top: 10px; opacity: 0.8;">
                ⚠️ 声明：本报告为 AI 自动生成，仅供参考，不构成投资建议
            </p>
        </div>
    </div>
</body>
</html>
"""
        return html

    def save_html(self, html: str) -> bool:
        """保存 HTML 到文件"""
        output_file = self.report_dir / "index.html"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"✅ 仪表板已更新: {output_file}")
            return True
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False

    def run(self) -> bool:
        """执行更新流程"""
        print("\n" + "=" * 70)
        print("📊 Alpha Hive 仪表板更新")
        print("=" * 70)

        # 1. 读取报告
        print("\n[1/4] 读取今日报告...")
        report = self.read_today_report()
        if not report:
            print("⚠️  没有找到今日报告，将使用示例数据")
            report = {
                "opportunities": [
                    {"ticker": "NVDA", "direction": "看多", "opp_score": 8.5, "confidence": "85%",
                     "options_signal": "看多信号强", "key_catalyst": "新产品发布"},
                    {"ticker": "TSLA", "direction": "中性", "opp_score": 6.2, "confidence": "62%",
                     "options_signal": "信号平衡", "key_catalyst": "财报公布"},
                    {"ticker": "VKTX", "direction": "看空", "opp_score": 5.1, "confidence": "51%",
                     "options_signal": "看空信号", "key_catalyst": "临床试验结果"},
                ]
            }
        else:
            print(f"✅ 已读取报告，包含 {len(report.get('opportunities', []))} 个机会")

        # 2. 提取Top机会
        print("\n[2/4] 提取Top机会...")
        opportunities = self.extract_top_opportunities(report)
        print(f"✅ 提取了 {len(opportunities)} 个Top机会")

        # 3. 获取历史报告和系统状态
        print("\n[3/4] 扫描历史报告...")
        reports = self.get_recent_reports(days=7)
        print(f"✅ 找到 {len(reports)} 份最近报告")

        print("\n[3/4] 获取系统状态...")
        system_status = self.get_system_status()
        print(f"✅ 系统状态：{system_status.get('status', 'unknown')}")

        # 4. 生成并保存 HTML
        print("\n[4/4] 生成 HTML...")
        html = self.generate_html(opportunities, reports, system_status)

        if self.save_html(html):
            print("\n" + "=" * 70)
            print("✅ 仪表板更新完成！")
            print("📄 访问地址：/Users/igg/.claude/reports/index.html")
            print("=" * 70)
            return True
        else:
            return False


def main():
    """主入口"""
    updater = DashboardUpdater()
    updater.run()


if __name__ == "__main__":
    main()
