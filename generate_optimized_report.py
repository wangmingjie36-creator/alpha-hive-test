"""
🐝 Alpha Hive - 生成优化后的完整报告
集成 4 个优化：Thesis Breaks、Crowding、Catalyst、Feedback Loop
"""

import os
from datetime import datetime
from thesis_breaks import ThesisBreakMonitor
from catalyst_refinement import create_nvda_catalysts, create_vktx_catalysts
from crowding_detector import CrowdingDetector, get_nvda_crowding_metrics, get_vktx_crowding_metrics
from feedback_loop import ReportSnapshot


class OptimizedReportGenerator:
    """生成优化后的完整报告"""

    def __init__(self, ticker: str, date: str = None):
        self.ticker = ticker
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.html_sections = []

    def add_thesis_breaks_section(self, initial_score: float):
        """添加失效条件部分"""
        monitor = ThesisBreakMonitor(self.ticker, initial_score)
        html = monitor.generate_html_section()
        self.html_sections.append(("失效条件", html))
        print(f"✅ 添加 {self.ticker} 的失效条件部分")

    def add_catalyst_section(self, catalysts):
        """添加催化剂部分"""
        html = catalysts.generate_timeline_html()
        self.html_sections.append(("催化剂时间线", html))
        print(f"✅ 添加 {self.ticker} 的催化剂部分")

    def add_crowding_section(self, initial_score: float, metrics: dict):
        """添加拥挤度部分"""
        detector = CrowdingDetector(self.ticker)
        html = detector.generate_html_section(metrics, initial_score)
        self.html_sections.append(("拥挤度分析", html))
        print(f"✅ 添加 {self.ticker} 的拥挤度部分")

    def generate_full_html(self, title: str, base_content: str) -> str:
        """生成完整的 HTML 报告"""

        html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title} - Alpha Hive 优化分析报告</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}

                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    min-height: 100vh;
                }}

                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}

                .header {{
                    background: white;
                    border-radius: 12px;
                    padding: 40px;
                    margin-bottom: 30px;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
                    text-align: center;
                }}

                .header h1 {{
                    font-size: 36px;
                    color: #333;
                    margin-bottom: 10px;
                }}

                .header .subtitle {{
                    font-size: 16px;
                    color: #666;
                    margin-bottom: 20px;
                }}

                .update-time {{
                    font-size: 13px;
                    color: #999;
                }}

                .toc {{
                    background: white;
                    border-radius: 8px;
                    padding: 20px;
                    margin-bottom: 30px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }}

                .toc h2 {{
                    margin-bottom: 15px;
                    color: #333;
                }}

                .toc ul {{
                    list-style: none;
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 10px;
                }}

                .toc li {{
                    padding: 10px;
                    background: #f9f9f9;
                    border-radius: 4px;
                    border-left: 3px solid #667eea;
                }}

                .toc a {{
                    text-decoration: none;
                    color: #667eea;
                    font-weight: 600;
                    transition: color 0.3s;
                }}

                .toc a:hover {{
                    color: #764ba2;
                }}

                .base-content {{
                    background: white;
                    border-radius: 12px;
                    padding: 30px;
                    margin-bottom: 30px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }}

                .optimization-sections {{
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                }}

                .optimization-section {{
                    background: white;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }}

                .optimization-section-header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 20px;
                    font-size: 18px;
                    font-weight: 600;
                }}

                .optimization-section-content {{
                    padding: 20px;
                }}

                .report-section {{
                    background: #f9f9f9;
                    padding: 15px;
                    border-radius: 6px;
                    margin: 15px 0;
                }}

                .card-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 15px;
                }}

                .footer {{
                    background: white;
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    color: #666;
                    font-size: 13px;
                    margin-top: 30px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }}

                .disclaimer {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    border-radius: 4px;
                    margin: 20px 0;
                }}

                .disclaimer strong {{
                    color: #ff9800;
                }}

                @media (max-width: 768px) {{
                    .header h1 {{
                        font-size: 24px;
                    }}

                    .toc ul {{
                        grid-template-columns: 1fr;
                    }}

                    .base-content {{
                        padding: 15px;
                    }}
                }}

                @media print {{
                    body {{
                        background: white;
                    }}

                    .container {{
                        max-width: 100%;
                    }}

                    .optimization-section {{
                        page-break-inside: avoid;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <!-- 标题 -->
                <div class="header">
                    <h1>🐝 Alpha Hive 优化分析报告</h1>
                    <div class="subtitle">{title} - 多源信号融合 & 风险管理</div>
                    <div class="update-time">📅 报告日期：{self.date} | 🐝 Alpha Hive 系统自动生成</div>
                </div>

                <!-- 目录 -->
                <div class="toc">
                    <h2>📋 报告目录</h2>
                    <ul>
                        <li><a href="#base-analysis">基础分析</a></li>
                        <li><a href="#thesis-breaks">🚨 失效条件监控</a></li>
                        <li><a href="#catalyst-timeline">🎯 催化剂时间线</a></li>
                        <li><a href="#crowding-analysis">🗣️ 拥挤度分析</a></li>
                        <li><a href="#methodology">📊 方法论说明</a></li>
                    </ul>
                </div>

                <!-- 基础内容 -->
                <div class="base-content" id="base-analysis">
                    <h2>📊 基础分析</h2>
                    {base_content}
                </div>

                <!-- 优化部分 -->
                <div class="optimization-sections">
        """

        for i, (title, content) in enumerate(self.html_sections, 1):
            section_id = title.lower().replace(" ", "-").replace("：", "-")
            html += f"""
                    <div class="optimization-section">
                        <div class="optimization-section-header">
                            {i}. {title}
                        </div>
                        <div class="optimization-section-content" id="{section_id}">
                            {content}
                        </div>
                    </div>
            """

        html += """
                </div>

                <!-- 方法论说明 -->
                <div class="base-content" id="methodology">
                    <h2>📊 方法论说明</h2>

                    <h3>🎯 4 大优化创新</h3>

                    <div class="report-section">
                        <h4>✅ 优化 5：Thesis Breaks（失效条件）</h4>
                        <p>
                            明确定义每个推荐的"失效条件"。系统将持续监控这些条件，
                            一旦触发 Level 1 预警，自动降低评分 15%；
                            触发 Level 2 认输，立即反转推荐并发送警报。
                        </p>
                        <p><strong>好处：</strong> 降低风险，提前预警。</p>
                    </div>

                    <div class="report-section">
                        <h4>✅ 优化 4：Crowding Detection（拥挤度检测）</h4>
                        <p>
                            基于 StockTwits 消息量、Google Trends、Agent 共识、
                            Polymarket 赔率变化等 6 个维度，计算 0-100 的拥挤度评分。
                            拥挤度高（> 60）的标的自动打折 30%，并提供对冲建议。
                        </p>
                        <p><strong>好处：</strong> 识别过度定价，发现非共识机会。</p>
                    </div>

                    <div class="report-section">
                        <h4>✅ 优化 3：Catalyst Refinement（催化剂精细化）</h4>
                        <p>
                            从"财报发布（2周内）"精细化为"2026-03-15 美东 4PM 发布，
                            期权隐含波动率 15.2%，历史 65% Beat 概率"。
                            包含历史对标、市场预期、关键指标、后续事件、失效条件。
                        </p>
                        <p><strong>好处：</strong> 时间精确，风险清晰。</p>
                    </div>

                    <div class="report-section">
                        <h4>✅ 优化 7：Feedback Loop（反馈环路）</h4>
                        <p>
                            每份报告生成时保存快照。T+1、T+7、T+30 回溯准确度。
                            计算每个 Agent 的贡献度，每周自动建议权重调整。
                            透明的准确度看板显示历史表现。
                        </p>
                        <p><strong>好处：</strong> 自我完善，持续优化。</p>
                    </div>

                    <h3>🎯 评分公式</h3>
                    <p>
                        <strong>综合评分 = 0.30×信号 + 0.20×催化 + 0.20×情绪 + 0.15×赔率 + 0.15×风险</strong>
                    </p>
                    <p>
                        拥挤度调整：如果拥挤度 > 60，最终评分 = 综合评分 × 0.70
                    </p>

                    <h3>🚨 风险免责</h3>
                    <div class="disclaimer">
                        <strong>⚠️ 重要声明：</strong>
                        本报告基于公开信息研究和情景推演，<strong>不构成投资建议</strong>。
                        投资者应独立思考，控制仓位在账户价值的 3-5% 以内，
                        务必设置止损。本系统不承担任何投资损失责任。
                    </div>
                </div>

                <!-- 页脚 -->
                <div class="footer">
                    <p>🐝 <strong>Alpha Hive - 去中心化投资研究系统</strong></p>
                    <p>基于蜂群智能的多源信号融合平台</p>
                    <p style="margin-top: 10px; font-size: 11px; color: #999;">
                        报告自动生成 | 数据来自 SEC、Polymarket、X、财报等公开渠道 | 最后更新：{self.date}
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        return html

    def save_report(self, filename: str = None, base_content: str = "") -> str:
        """保存报告到 HTML 文件"""

        if filename is None:
            filename = f"alpha-hive-{self.ticker}-optimized-{self.date}.html"

        title = f"{self.ticker} 优化分析"

        html = self.generate_full_html(title, base_content)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        return filename


# 为 NVDA 生成优化报告
def generate_nvda_optimized_report():
    """为 NVDA 生成完整优化报告"""

    generator = OptimizedReportGenerator("NVDA", "2026-02-23")

    # 1. 添加失效条件
    generator.add_thesis_breaks_section(initial_score=8.52)

    # 2. 添加催化剂
    nvda_catalysts = create_nvda_catalysts()
    generator.add_catalyst_section(nvda_catalysts)

    # 3. 添加拥挤度
    nvda_metrics = get_nvda_crowding_metrics()
    generator.add_crowding_section(initial_score=8.52, metrics=nvda_metrics)

    # 4. 生成并保存
    base_content = """
    <div class="report-section">
        <h3>综合评分：8.52/10 🟢 强烈推荐</h3>
        <p>
            NVIDIA 是 AI 芯片的绝对龙头，市占率 80%。
            财报在即（3月15日），市场共识 100% 看多。
        </p>
        <p>
            <strong>关键数据：</strong><br>
            • 数据中心收入占比：80%+（增长引擎）<br>
            • 毛利率：72%（行业最高）<br>
            • 市占率：80%（垄断地位）<br>
            • 6 个 Agent 一致看多（100% 共识）
        </p>
        <p>
            <strong>推荐方向：</strong> 看多 | <strong>目标价：</strong> $650 | <strong>止损：</strong> $580
        </p>
    </div>
    """

    filename = generator.save_report(base_content=base_content)
    print(f"✅ NVDA 优化报告已生成：{filename}")

    return filename


# 为 VKTX 生成优化报告
def generate_vktx_optimized_report():
    """为 VKTX 生成完整优化报告"""

    generator = OptimizedReportGenerator("VKTX", "2026-02-23")

    # 1. 添加失效条件
    generator.add_thesis_breaks_section(initial_score=7.15)

    # 2. 添加催化剂
    vktx_catalysts = create_vktx_catalysts()
    generator.add_catalyst_section(vktx_catalysts)

    # 3. 添加拥挤度
    vktx_metrics = get_vktx_crowding_metrics()
    generator.add_crowding_section(initial_score=7.15, metrics=vktx_metrics)

    # 4. 生成并保存
    base_content = """
    <div class="report-section">
        <h3>综合评分：7.15/10 🟡 观察中</h3>
        <p>
            Viking Therapeutics 是一家临床阶段生物制药公司，
            高风险高收益。重点关注 Phase 3 试验结果。
        </p>
        <p>
            <strong>关键数据：</strong><br>
            • 波动率：24.29%（高风险）<br>
            • YTD 涨幅：+6.59%<br>
            • Agent 共识：67% 看好（存在分歧）<br>
            • 下一催化：Phase 3 试验结果（Q3 2026）
        </p>
        <p>
            <strong>推荐方向：</strong> 观察中 | <strong>目标价：</strong> 待定 | <strong>评估周期：</strong> 3-6 个月
        </p>
    </div>
    """

    filename = generator.save_report(base_content=base_content)
    print(f"✅ VKTX 优化报告已生成：{filename}")

    return filename


if __name__ == "__main__":
    print("🐝 Alpha Hive 优化报告生成器")
    print("=" * 50)

    # 生成 NVDA 报告
    nvda_file = generate_nvda_optimized_report()

    # 生成 VKTX 报告
    vktx_file = generate_vktx_optimized_report()

    print("\n" + "=" * 50)
    print("✅ 所有报告已生成！")
    print(f"📄 NVDA: {nvda_file}")
    print(f"📄 VKTX: {vktx_file}")
    print("\n💡 下一步：")
    print("1. 在浏览器中打开 HTML 文件查看")
    print("2. 打印或导出为 PDF")
    print("3. 分享给投资团队")
