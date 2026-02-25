"""
🐝 Alpha Hive - 实时报告生成系统
使用 realtime_metrics.json 中的数据生成优化报告
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional
from data_fetcher import DataFetcher
from crowding_detector import CrowdingDetector
from catalyst_refinement import CatalystTimeline
from thesis_breaks import ThesisBreakMonitor
from feedback_loop import BacktestAnalyzer


class RealtimeReportGenerator:
    """使用实时数据的报告生成器"""

    def __init__(self):
        self.fetcher = DataFetcher()
        self.timestamp = datetime.now()

    def load_realtime_metrics(self, ticker: str) -> Optional[Dict]:
        """从文件加载或实时采集实时数据"""
        metrics_file = "realtime_metrics.json"

        # 尝试从文件加载
        if os.path.exists(metrics_file):
            try:
                with open(metrics_file, 'r') as f:
                    all_metrics = json.load(f)
                    if ticker in all_metrics:
                        return all_metrics[ticker]
            except Exception as e:
                print(f"⚠️ 读取缓存数据失败: {e}")

        # 实时采集
        print(f"🔄 实时采集 {ticker} 的数据...")
        return self.fetcher.collect_all_metrics(ticker)

    def generate_html_report(
        self,
        ticker: str,
        metrics: Dict,
        crowding_score: float,
        crowding_scores: Dict,
    ) -> str:
        """生成完整的 HTML 报告"""

        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alpha Hive - {ticker} 实时优化报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .timestamp {{
            font-size: 0.9em;
            opacity: 0.8;
            margin-top: 10px;
        }}

        .section {{
            padding: 30px;
            border-bottom: 1px solid #eee;
        }}

        .section:last-child {{
            border-bottom: none;
        }}

        .section h2 {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }}

        .section h2::before {{
            content: '📊';
            margin-right: 10px;
            font-size: 1.2em;
        }}

        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}

        .metric-card {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 8px;
            transition: transform 0.2s;
        }}

        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}

        .metric-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }}

        .metric-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #333;
        }}

        .metric-unit {{
            font-size: 0.8em;
            color: #999;
            margin-left: 5px;
        }}

        .crowding-section {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}

        .crowding-section h3 {{
            color: #856404;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }}

        .crowding-section h3::before {{
            content: '🔴';
            margin-right: 8px;
        }}

        .dimension {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
        }}

        .dimension-item {{
            background: white;
            padding: 12px;
            border-radius: 6px;
            border-left: 3px solid #667eea;
        }}

        .dimension-name {{
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}

        .dimension-score {{
            font-size: 1.5em;
            color: #667eea;
            font-weight: bold;
        }}

        .progress-bar {{
            background: #e9ecef;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 5px;
        }}

        .progress-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            transition: width 0.3s;
        }}

        .data-sources {{
            background: #f0f4ff;
            border: 1px solid #667eea;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}

        .data-sources h4 {{
            color: #667eea;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }}

        .data-sources h4::before {{
            content: '📡';
            margin-right: 8px;
        }}

        .source-item {{
            padding: 8px 0;
            border-bottom: 1px solid #ddd;
            font-size: 0.95em;
        }}

        .source-item:last-child {{
            border-bottom: none;
        }}

        .source-name {{
            font-weight: bold;
            color: #333;
        }}

        .source-time {{
            color: #999;
            font-size: 0.9em;
            margin-left: 10px;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}

        .disclaimer {{
            background: #fee;
            border: 1px solid #fcc;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        .disclaimer::before {{
            content: '⚠️ ';
            font-weight: bold;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}

            .metric-grid {{
                grid-template-columns: 1fr;
            }}

            .dimension {{
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
            <p class="subtitle">{ticker} 实时优化报告</p>
            <p class="timestamp">
                生成时间：{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
                <br>
                <small>数据来源：实时采集 | StockTwits | Polymarket | Yahoo Finance | Google Trends</small>
            </p>
        </div>

        <!-- 免责声明 -->
        <div class="section">
            <div class="disclaimer">
                本报告基于公开信息和实时市场数据生成，不构成投资建议。
                所有数据仅供参考，投资决策需自行承担责任。
            </div>
        </div>

        <!-- 实时拥挤度分析 -->
        <div class="section">
            <h2>拥挤度分析（Crowding Detection）</h2>

            <div class="crowding-section">
                <h3>综合拥挤度评分：<span style="color: #dc3545;">{crowding_score:.1f}/100</span></h3>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(crowding_score, 100)}%"></div>
                </div>
                <p style="margin-top: 10px; color: #856404;">
                    {self._get_crowding_interpretation(crowding_score)}
                </p>
            </div>

            <h3 style="color: #333; margin-top: 20px; margin-bottom: 15px;">📊 六维度分解</h3>
            <div class="dimension">
                <div class="dimension-item">
                    <div class="dimension-name">🗣️ StockTwits 消息量</div>
                    <div class="dimension-score">{crowding_scores.get('stocktwits_volume', 0):.0f}/100</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {crowding_scores.get('stocktwits_volume', 0)}%"></div>
                    </div>
                </div>

                <div class="dimension-item">
                    <div class="dimension-name">📈 Google 趋势</div>
                    <div class="dimension-score">{crowding_scores.get('google_trends', 0):.0f}/100</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {crowding_scores.get('google_trends', 0)}%"></div>
                    </div>
                </div>

                <div class="dimension-item">
                    <div class="dimension-name">👥 Agent 共识</div>
                    <div class="dimension-score">{crowding_scores.get('consensus_strength', 0):.0f}/100</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {crowding_scores.get('consensus_strength', 0)}%"></div>
                    </div>
                </div>

                <div class="dimension-item">
                    <div class="dimension-name">💱 Polymarket 波动</div>
                    <div class="dimension-score">{crowding_scores.get('polymarket_volatility', 0):.0f}/100</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {crowding_scores.get('polymarket_volatility', 0)}%"></div>
                    </div>
                </div>

                <div class="dimension-item">
                    <div class="dimension-name">📰 Seeking Alpha</div>
                    <div class="dimension-score">{crowding_scores.get('seeking_alpha_views', 0):.0f}/100</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {crowding_scores.get('seeking_alpha_views', 0)}%"></div>
                    </div>
                </div>

                <div class="dimension-item">
                    <div class="dimension-name">🔴 做空风险</div>
                    <div class="dimension-score">{crowding_scores.get('short_squeeze_risk', 0):.0f}/100</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {crowding_scores.get('short_squeeze_risk', 0)}%"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 实时数据源 -->
        <div class="section">
            <h2>实时数据源</h2>

            <div class="data-sources">
                <h4>📡 数据采集情况</h4>
                <div class="source-item">
                    <span class="source-name">✅ StockTwits</span>
                    <span class="source-time">{metrics['sources']['stocktwits'].get('last_updated', 'N/A')}</span>
                    <br>
                    消息量：{metrics['sources']['stocktwits'].get('messages_per_day', 0):,} 条/天
                </div>

                <div class="source-item">
                    <span class="source-name">✅ Polymarket</span>
                    <span class="source-time">{metrics['sources']['polymarket'].get('last_updated', 'N/A')}</span>
                    <br>
                    YES 赔率：{metrics['sources']['polymarket'].get('yes_odds', 0):.1%}
                    | 24h 变化：{metrics['sources']['polymarket'].get('odds_change_24h', 0):.1f}%
                </div>

                <div class="source-item">
                    <span class="source-name">✅ Yahoo Finance</span>
                    <span class="source-time">{metrics['sources']['yahoo_finance'].get('last_updated', 'N/A')}</span>
                    <br>
                    价格：${metrics['sources']['yahoo_finance'].get('current_price', 0):.2f}
                    | 5日涨跌：{metrics['sources']['yahoo_finance'].get('price_change_5d', 0):.1f}%
                </div>

                <div class="source-item">
                    <span class="source-name">✅ Google Trends</span>
                    <span class="source-time">{metrics['sources']['google_trends'].get('last_updated', 'N/A')}</span>
                    <br>
                    搜索热度：{metrics['sources']['google_trends'].get('search_interest_percentile', 0):.0f} 百分位
                </div>

                <div class="source-item">
                    <span class="source-name">✅ SEC EDGAR</span>
                    <br>
                    最近文件：{metrics['sources']['sec_filings'][0].get('filing_date', 'N/A') if metrics['sources']['sec_filings'] else 'N/A'}
                </div>

                <div class="source-item">
                    <span class="source-name">✅ Seeking Alpha</span>
                    <br>
                    周浏览量：{metrics['sources']['seeking_alpha'].get('page_views_week', 0):,}
                    | 文章数：{metrics['sources']['seeking_alpha'].get('article_count_week', 0)} 篇
                </div>
            </div>
        </div>

        <!-- 核心指标 -->
        <div class="section">
            <h2>核心指标</h2>

            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">当前价格</div>
                    <div class="metric-value">
                        ${metrics['sources']['yahoo_finance'].get('current_price', 0):.2f}
                    </div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">5 日涨跌</div>
                    <div class="metric-value">
                        <span style="color: {'#28a745' if metrics['sources']['yahoo_finance'].get('price_change_5d', 0) > 0 else '#dc3545'};">
                            {metrics['sources']['yahoo_finance'].get('price_change_5d', 0):+.1f}%
                        </span>
                    </div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">Polymarket YES 赔率</div>
                    <div class="metric-value">
                        {metrics['sources']['polymarket'].get('yes_odds', 0):.1%}
                    </div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">StockTwits 消息/天</div>
                    <div class="metric-value">
                        {metrics['sources']['stocktwits'].get('messages_per_day', 0):,}
                    </div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">做空比例</div>
                    <div class="metric-value">
                        {metrics['sources']['yahoo_finance'].get('short_float_ratio', 0):.1%}
                    </div>
                </div>

                <div class="metric-card">
                    <div class="metric-label">市场热度</div>
                    <div class="metric-value">
                        {metrics['sources']['google_trends'].get('search_interest_percentile', 0):.0f}
                        <span class="metric-unit">百分位</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 页脚 -->
        <div class="footer">
            <p>🐝 Alpha Hive - 去中心化的蜂群智能投资研究平台</p>
            <p style="margin-top: 10px; color: #999;">
                本报告基于实时数据自动生成 |
                <a href="https://github.com/yourusername/hive-report" style="color: #667eea; text-decoration: none;">
                    GitHub 源码
                </a>
            </p>
        </div>
    </div>
</body>
</html>
"""
        return html

    def _get_crowding_interpretation(self, score: float) -> str:
        """获取拥挤度评分的解释"""
        if score < 30:
            return "✅ 低拥挤度 - 市场关注度不足，机会窗口可能开启"
        elif score < 50:
            return "🟡 中低拥挤度 - 市场逐渐关注，入场机会"
        elif score < 70:
            return "🟠 中高拥挤度 - 市场广泛参与，谨慎介入"
        else:
            return "🔴 高拥挤度 - 市场严重拥挤，避免追高"

    def generate_realtime_report(self, ticker: str) -> str:
        """生成完整的实时优化报告"""

        print(f"\n{'='*60}")
        print(f"🔄 正在为 {ticker} 生成实时优化报告...")
        print(f"{'='*60}")

        # 第 1 步：加载实时数据
        print(f"✓ 加载实时数据...")
        metrics = self.load_realtime_metrics(ticker)
        if not metrics:
            print(f"❌ 无法加载 {ticker} 的数据")
            return ""

        # 第 2 步：拥挤度检测
        print(f"✓ 计算拥挤度评分...")
        detector = CrowdingDetector(ticker)
        crowding_score, crowding_scores = detector.calculate_crowding_score(
            metrics["crowding_input"]
        )

        print(f"  - 综合评分：{crowding_score:.1f}/100")

        # 第 3 步：生成 HTML
        print(f"✓ 生成 HTML 报告...")
        html = self.generate_html_report(
            ticker=ticker,
            metrics=metrics,
            crowding_score=crowding_score,
            crowding_scores=crowding_scores,
        )

        return html


# ==================== 主程序 ====================
if __name__ == "__main__":
    print("🚀 启动实时报告生成系统")

    # 创建生成器
    generator = RealtimeReportGenerator()

    # 生成所有标的的报告
    tickers = ["NVDA", "VKTX", "TSLA"]

    for ticker in tickers:
        html = generator.generate_realtime_report(ticker)

        if html:
            output_file = f"alpha-hive-{ticker}-realtime-{generator.timestamp.strftime('%Y-%m-%d')}.html"
            with open(output_file, 'w') as f:
                f.write(html)

            print(f"✅ 报告已生成：{output_file}\n")

    print(f"🎉 所有报告已生成完毕！")
    print(f"\n📂 文件列表：")
    import subprocess
    subprocess.run(["ls", "-lh", "alpha-hive-*-realtime-*.html"])
