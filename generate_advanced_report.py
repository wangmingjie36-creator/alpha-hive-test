"""
🐝 Alpha Hive - 高级分析报告生成
整合所有高级分析功能，生成专业投资报告
"""

import json
from datetime import datetime
from advanced_analyzer import AdvancedAnalyzer


class AdvancedReportGenerator:
    """高级分析报告生成器"""

    def __init__(self):
        self.analyzer = AdvancedAnalyzer()
        self.timestamp = datetime.now()

    def generate_html_report(self, ticker: str, analysis: dict) -> str:
        """生成高级分析 HTML 报告"""

        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alpha Hive - {ticker} 高级分析报告</title>
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
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.8em;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .timestamp {{
            font-size: 0.9em;
            opacity: 0.8;
            margin-top: 15px;
        }}

        .rating-banner {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 40px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }}

        .rating-item {{
            text-align: center;
            margin: 10px 20px;
        }}

        .rating-label {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 5px;
        }}

        .rating-value {{
            font-size: 2em;
            font-weight: bold;
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 50px;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 30px;
        }}

        .section:last-child {{
            border-bottom: none;
        }}

        .section h2 {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
        }}

        .section h2::before {{
            content: '';
            display: inline-block;
            width: 5px;
            height: 30px;
            background: #667eea;
            margin-right: 15px;
            border-radius: 3px;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }}

        .card {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 25px;
            border-radius: 8px;
            transition: transform 0.2s;
        }}

        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .card h3 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 1.1em;
        }}

        .metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 10px 0;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}

        .metric-label {{
            color: #666;
            font-size: 0.95em;
        }}

        .metric-value {{
            font-weight: bold;
            color: #333;
            font-size: 1.1em;
        }}

        .positive {{
            color: #28a745;
        }}

        .negative {{
            color: #dc3545;
        }}

        .neutral {{
            color: #ffc107;
        }}

        .recommendation-box {{
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border: 2px solid #667eea;
            border-radius: 10px;
            padding: 25px;
            margin: 20px 0;
        }}

        .recommendation-rating {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}

        .recommendation-action {{
            font-size: 1.3em;
            color: #333;
            margin-bottom: 15px;
        }}

        .recommendation-rationale {{
            font-size: 1em;
            color: #666;
            line-height: 1.6;
        }}

        .table-wrapper {{
            overflow-x: auto;
            margin: 20px 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}

        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}

        tr:hover {{
            background: #f9f9f9;
        }}

        .advantage-list {{
            list-style: none;
        }}

        .advantage-list li {{
            padding: 10px 0;
            margin-left: 25px;
            position: relative;
        }}

        .advantage-list li::before {{
            content: '✓';
            position: absolute;
            left: -25px;
            color: #28a745;
            font-weight: bold;
            font-size: 1.2em;
        }}

        .threat-list {{
            list-style: none;
        }}

        .threat-list li {{
            padding: 10px 0;
            margin-left: 25px;
            position: relative;
        }}

        .threat-list li::before {{
            content: '⚠';
            position: absolute;
            left: -25px;
            color: #dc3545;
            font-size: 1.2em;
        }}

        .holding-plan {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            margin: 15px 0;
        }}

        .holding-stage {{
            padding: 20px;
            border-bottom: 1px solid #eee;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
        }}

        .holding-stage:last-child {{
            border-bottom: none;
        }}

        .stage-label {{
            font-weight: bold;
            color: #667eea;
            margin-bottom: 8px;
        }}

        .stage-value {{
            font-size: 1.3em;
            color: #333;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 25px 40px;
            text-align: center;
            color: #666;
            font-size: 0.95em;
        }}

        .footer p {{
            margin: 5px 0;
        }}

        .emoji {{
            margin-right: 8px;
        }}

        @media (max-width: 768px) {{
            .rating-banner {{
                flex-direction: column;
            }}

            .content {{
                padding: 20px;
            }}

            .section h2 {{
                font-size: 1.4em;
            }}

            .grid {{
                grid-template-columns: 1fr;
            }}

            .holding-stage {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 页头 -->
        <div class="header">
            <h1>🐝 Alpha Hive</h1>
            <p class="subtitle">{ticker} 高级分析报告</p>
            <div class="timestamp">
                生成时间：{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>

        <!-- 评级横幅 -->
        <div class="rating-banner">
            <div class="rating-item">
                <div class="rating-label">投资评级</div>
                <div class="rating-value">{analysis['recommendation']['rating']}</div>
            </div>
            <div class="rating-item">
                <div class="rating-label">赚钱概率</div>
                <div class="rating-value positive">{analysis['probability_analysis']['win_probability_pct']}%</div>
            </div>
            <div class="rating-item">
                <div class="rating-label">风险收益比</div>
                <div class="rating-value">{analysis['probability_analysis']['risk_reward_ratio']}:1</div>
            </div>
        </div>

        <!-- 内容区 -->
        <div class="content">
            <!-- 概述 -->
            <div class="section">
                <h2>📌 概述</h2>
                <p style="font-size: 1.05em; line-height: 1.8; color: #333;">
                    {analysis['overview']}
                </p>
            </div>

            <!-- 行业对标 -->
            <div class="section">
                <h2>🏆 行业对标分析</h2>
                <div class="grid">
                    <div class="card">
                        <h3>市场地位</h3>
                        <div class="metric">
                            <span class="metric-label">所属行业</span>
                            <span class="metric-value">{analysis['industry_comparison']['industry']}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">竞争地位</span>
                            <span class="metric-value">{analysis['industry_comparison']['position']}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">竞争力评分</span>
                            <span class="metric-value positive">{analysis['industry_comparison']['comparative_strength']}/100</span>
                        </div>
                    </div>

                    <div class="card">
                        <h3>竞争优势</h3>
                        <ul class="advantage-list">
                            {self._render_advantages(analysis['industry_comparison']['competitive_advantages'])}
                        </ul>
                    </div>

                    <div class="card">
                        <h3>主要威胁</h3>
                        <ul class="threat-list">
                            {self._render_threats(analysis['industry_comparison']['competitive_threats'])}
                        </ul>
                    </div>
                </div>
            </div>

            <!-- 历史回溯分析 -->
            <div class="section">
                <h2>📈 历史回溯分析</h2>

                {self._render_similar_opportunities(analysis['historical_analysis']['similar_opportunities'])}

                <h3 style="color: #333; margin-top: 25px; margin-bottom: 15px;">预期收益分析</h3>
                <div class="table-wrapper">
                    {self._render_expected_returns(analysis['historical_analysis']['expected_returns'])}
                </div>
            </div>

            <!-- 概率和风险分析 -->
            <div class="section">
                <h2>🎲 概率和风险分析</h2>
                <div class="grid">
                    <div class="card">
                        <h3>赚钱概率</h3>
                        <div style="font-size: 3em; color: #28a745; font-weight: bold; margin: 20px 0;">
                            {analysis['probability_analysis']['win_probability_pct']}%
                        </div>
                        <p style="color: #666; font-size: 0.95em;">
                            基于历史拥挤度、催化剂质量和市场情绪的综合计算
                        </p>
                    </div>

                    <div class="card">
                        <h3>风险收益比</h3>
                        <div style="font-size: 3em; color: #667eea; font-weight: bold; margin: 20px 0;">
                            {analysis['probability_analysis']['risk_reward_ratio']}:1
                        </div>
                        <p style="color: #666; font-size: 0.95em;">
                            预期收益是预期风险的 {analysis['probability_analysis']['risk_reward_ratio']} 倍
                        </p>
                    </div>
                </div>
            </div>

            <!-- 位置管理 -->
            <div class="section">
                <h2>🛑 位置管理方案</h2>

                <h3 style="color: #333; margin: 20px 0 15px 0;">止损位置设置</h3>
                <div class="grid">
                    {self._render_stop_loss(analysis['position_management']['stop_loss'])}
                </div>

                <h3 style="color: #333; margin: 30px 0 15px 0;">止盈方案（分批了结）</h3>
                <div class="holding-plan">
                    {self._render_take_profit(analysis['position_management']['take_profit'])}
                </div>

                <h3 style="color: #333; margin: 30px 0 15px 0;">最优持仓时间</h3>
                <div class="card">
                    {self._render_optimal_holding_time(analysis['position_management']['optimal_holding_time'])}
                </div>
            </div>

            <!-- 投资建议 -->
            <div class="section">
                <h2>✅ 投资建议</h2>
                <div class="recommendation-box">
                    <div class="recommendation-rating">
                        {analysis['recommendation']['rating']}
                    </div>
                    <div class="recommendation-action">
                        💡 行动：{analysis['recommendation']['action']}
                    </div>
                    <div class="recommendation-rationale">
                        <strong>理由：</strong> {analysis['recommendation']['rationale']}
                    </div>
                </div>
            </div>

            <!-- 免责声明 -->
            <div class="section" style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 20px; border-radius: 8px;">
                <h3 style="color: #856404; margin-bottom: 10px;">⚠️ 免责声明</h3>
                <p style="color: #856404; font-size: 0.95em;">
                    本报告基于公开信息和历史数据生成，不构成投资建议。高级分析使用历史相似机会进行预测，
                    但市场具有高度不确定性。过往表现不代表未来收益。投资者应独立判断，自行承担投资风险。
                </p>
            </div>
        </div>

        <!-- 页脚 -->
        <div class="footer">
            <p>🐝 Alpha Hive - 去中心化蜂群智能投资研究平台</p>
            <p style="margin-top: 15px; font-size: 0.9em; color: #999;">
                本报告由 AI 自动生成 | 高级分析引擎 v1.0
            </p>
        </div>
    </div>
</body>
</html>
"""
        return html

    def _render_advantages(self, advantages: list) -> str:
        """渲染优势列表"""
        html = ""
        for adv in advantages[:3]:
            html += f"<li>{adv}</li>"
        return html

    def _render_threats(self, threats: list) -> str:
        """渲染威胁列表"""
        html = ""
        for threat in threats[:3]:
            html += f"<li>{threat}</li>"
        return html

    def _render_similar_opportunities(self, opportunities: list) -> str:
        """渲染相似历史机会"""
        if not opportunities:
            return "<p>暂无相似历史机会</p>"

        html = "<table><thead><tr><th>日期</th><th>事件</th><th>3日收益</th><th>7日收益</th><th>30日收益</th><th>最大回撤</th></tr></thead><tbody>"

        for opp in opportunities[:3]:
            html += f"""
            <tr>
                <td>{opp['date']}</td>
                <td>{opp['event']}</td>
                <td class="positive">+{opp['gain_3d_pct']}%</td>
                <td class="positive">+{opp['gain_7d_pct']}%</td>
                <td class="positive">+{opp['gain_30d_pct']}%</td>
                <td class="negative">{opp['max_drawdown_pct']}%</td>
            </tr>
            """

        html += "</tbody></table>"
        return html

    def _render_expected_returns(self, expected_returns: dict) -> str:
        """渲染预期收益表"""
        if expected_returns.get("sample_size", 0) == 0:
            return "<p>数据不足</p>"

        html = f"""
        <table>
            <thead>
                <tr>
                    <th>时间周期</th>
                    <th>平均收益</th>
                    <th>中位数</th>
                    <th>最小值</th>
                    <th>最大值</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>3 天</td>
                    <td class="positive">+{expected_returns['expected_3d']['mean']}%</td>
                    <td>{expected_returns['expected_3d']['median']}%</td>
                    <td class="negative">{expected_returns['expected_3d']['min']}%</td>
                    <td class="positive">{expected_returns['expected_3d']['max']}%</td>
                </tr>
                <tr>
                    <td>7 天</td>
                    <td class="positive">+{expected_returns['expected_7d']['mean']}%</td>
                    <td>{expected_returns['expected_7d']['median']}%</td>
                    <td class="negative">{expected_returns['expected_7d']['min']}%</td>
                    <td class="positive">{expected_returns['expected_7d']['max']}%</td>
                </tr>
                <tr>
                    <td>30 天</td>
                    <td class="positive">+{expected_returns['expected_30d']['mean']}%</td>
                    <td>{expected_returns['expected_30d']['median']}%</td>
                    <td class="negative">{expected_returns['expected_30d']['min']}%</td>
                    <td class="positive">{expected_returns['expected_30d']['max']}%</td>
                </tr>
            </tbody>
        </table>
        <p style="font-size: 0.9em; color: #666; margin-top: 10px;">
            基于 {expected_returns['sample_size']} 次相似历史机会计算
        </p>
        """
        return html

    def _render_stop_loss(self, stop_loss: dict) -> str:
        """渲染止损位置"""
        html = ""
        levels = [
            ("保守型（-2%）", "conservative", "适合风险厌恶者"),
            ("适中型（-5%）", "moderate", "标准做法"),
            ("激进型（-8%）", "aggressive", "承受更大波动"),
        ]

        for label, key, desc in levels:
            html += f"""
            <div class="card">
                <h3>{label}</h3>
                <div style="font-size: 1.8em; color: #dc3545; font-weight: bold; margin: 15px 0;">
                    ${stop_loss[key]}
                </div>
                <p style="color: #666; font-size: 0.9em;">{desc}</p>
            </div>
            """

        return html

    def _render_take_profit(self, take_profit: dict) -> str:
        """渲染止盈方案"""
        html = ""
        for level in ["level_1", "level_2", "level_3"]:
            data = take_profit[level]
            html += f"""
            <div class="holding-stage">
                <div>
                    <div class="stage-label">第 {level[-1]} 层目标</div>
                    <div class="stage-value positive">${data['price']}</div>
                </div>
                <div>
                    <div class="stage-label">涨幅目标</div>
                    <div class="stage-value positive">+{data['gain_pct']}%</div>
                </div>
                <div>
                    <div class="stage-label">行动</div>
                    <div class="stage-value">卖 {int(data['sell_ratio']*100)}%</div>
                </div>
                <div style="grid-column: 1/-1; color: #666; font-size: 0.95em;">
                    💡 {data['reason']}
                </div>
            </div>
            """

        return html

    def _render_optimal_holding_time(self, optimal_holding: dict) -> str:
        """渲染最优持仓时间"""
        if "note" in optimal_holding and optimal_holding.get("note"):
            return f"<p style=\"color: #666;\">{optimal_holding['note']}</p>"

        html = f"""
        <div class="metric">
            <span class="metric-label">推荐持仓天数</span>
            <span class="metric-value positive">
                {optimal_holding.get('recommended_holding_days', '7')} 天
            </span>
        </div>
        <div class="metric">
            <span class="metric-label">持仓范围</span>
            <span class="metric-value">
                {optimal_holding.get('holding_time_range', {}).get('minimum', '3')}-
                {optimal_holding.get('holding_time_range', {}).get('maximum', '30')} 天
            </span>
        </div>
        """

        if optimal_holding.get('expected_gain_at_optimal_time'):
            html += f"""
            <div class="metric">
                <span class="metric-label">最优时间收益</span>
                <span class="metric-value positive">
                    +{optimal_holding['expected_gain_at_optimal_time']}%
                </span>
            </div>
            """

        return html


def main():
    """主程序"""
    import json

    # 加载实时数据
    with open("realtime_metrics.json") as f:
        metrics = json.load(f)

    # 创建生成器
    analyzer = AdvancedAnalyzer()
    report_gen = AdvancedReportGenerator()

    print("🎯 生成高级分析报告...")
    print("=" * 60)

    # 为每个标的生成报告
    for ticker in ["NVDA", "VKTX", "TSLA"]:
        if ticker in metrics:
            print(f"\n📊 生成 {ticker} 高级分析报告...")

            # 生成分析
            analysis = analyzer.generate_comprehensive_analysis(ticker, metrics[ticker])

            # 生成 HTML
            html = report_gen.generate_html_report(ticker, analysis)

            # 保存文件
            filename = f"alpha-hive-{ticker}-advanced-{report_gen.timestamp.strftime('%Y-%m-%d')}.html"
            with open(filename, "w") as f:
                f.write(html)

            print(f"   ✅ 报告已生成：{filename}")

    print("\n" + "=" * 60)
    print("✅ 所有高级分析报告已生成完毕！")
    print("=" * 60)

    # 列出生成的文件
    import subprocess

    subprocess.run(["ls", "-lh", "alpha-hive-*-advanced-*.html"])


if __name__ == "__main__":
    main()
