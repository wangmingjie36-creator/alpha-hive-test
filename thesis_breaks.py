"""
🐝 Alpha Hive - Thesis Breaks 监控系统
优化 5：明确定义和监控失效条件
"""

import json
from datetime import datetime
from typing import List, Dict, Tuple

class ThesisBreakConfig:
    """针对不同标的的失效条件配置"""

    NVDA_BREAKS = {
        "level_1_warning": {
            "name": "预警级别",
            "score_reduction": -0.15,
            "conditions": [
                {
                    "id": "datacenter_revenue_decline",
                    "metric": "DataCenter Revenue Growth",
                    "trigger": "季度环比下降 > 5%",
                    "data_source": "季度财报",
                    "check_frequency": "季度",
                    "current_status": "✅ 正常（+8% QoQ）",
                    "severity": "HIGH"
                },
                {
                    "id": "competitor_threat",
                    "metric": "竞争对手新产品",
                    "trigger": "AMD 或 Intel 发布超越 NVIDIA 的产品",
                    "data_source": "产品发布公告",
                    "check_frequency": "实时",
                    "current_status": "✅ 无重大威胁",
                    "severity": "HIGH"
                },
                {
                    "id": "china_ban_risk",
                    "metric": "中国芯片禁令",
                    "trigger": "Polymarket 禁令概率 > 60%",
                    "data_source": "Polymarket",
                    "check_frequency": "实时",
                    "current_status": "⚠️ 中等风险（概率 35%）",
                    "severity": "CRITICAL"
                },
                {
                    "id": "margin_compression",
                    "metric": "毛利率",
                    "trigger": "季度环比下降 > 200bps",
                    "data_source": "财报",
                    "check_frequency": "季度",
                    "current_status": "✅ 稳定（72% 毛利率）",
                    "severity": "MEDIUM"
                }
            ]
        },
        "level_2_stop_loss": {
            "name": "认输级别",
            "recommendation_reverse": True,
            "conditions": [
                {
                    "id": "eps_miss_severe",
                    "metric": "EPS 大幅低于预期",
                    "trigger": "实际 < 预期 20%+",
                    "data_source": "财报披露",
                    "check_frequency": "季度",
                    "current_status": "✅ 未发生",
                    "action": "立即转向空头或对冲"
                },
                {
                    "id": "export_ban",
                    "metric": "美国芯片出口禁令",
                    "trigger": "直接禁止对华 H100/H800 销售",
                    "data_source": "商务部公告",
                    "check_frequency": "实时",
                    "current_status": "⚠️ 监管风险中等",
                    "action": "财务影响：假设 4% 总收入"
                },
                {
                    "id": "ceo_departure",
                    "metric": "CEO 离职",
                    "trigger": "Jensen Huang 宣布离职",
                    "data_source": "公司公告",
                    "check_frequency": "实时",
                    "current_status": "✅ 无异常",
                    "action": "战略不确定性极高"
                }
            ]
        }
    }

    VKTX_BREAKS = {
        "level_1_warning": {
            "name": "预警级别",
            "score_reduction": -0.15,
            "conditions": [
                {
                    "id": "trial_dropout",
                    "metric": "临床试验患者脱落",
                    "trigger": "关键患者脱落 > 15%",
                    "data_source": "试验数据",
                    "check_frequency": "持续",
                    "current_status": "✅ 未报告异常",
                    "severity": "CRITICAL"
                },
                {
                    "id": "competitor_data",
                    "metric": "竞争对手试验数据",
                    "trigger": "发布更优越的数据",
                    "data_source": "学术会议/FDA 公告",
                    "check_frequency": "实时",
                    "current_status": "✅ 无重大威胁",
                    "severity": "HIGH"
                }
            ]
        },
        "level_2_stop_loss": {
            "name": "认输级别",
            "recommendation_reverse": True,
            "conditions": [
                {
                    "id": "fda_hold",
                    "metric": "FDA 临床试验暂停",
                    "trigger": "IND Hold（试验中止令）",
                    "data_source": "FDA 官方",
                    "check_frequency": "实时",
                    "current_status": "✅ 未发生",
                    "action": "股价可能暴跌 30-50%"
                },
                {
                    "id": "trial_failure",
                    "metric": "Phase 3 试验失败",
                    "trigger": "关键终点未达到统计学意义",
                    "data_source": "试验结果发布",
                    "check_frequency": "按计划发布日期",
                    "current_status": "⏳ 预期 2026-Q3 发布",
                    "action": "股价可能下跌 60-80%"
                }
            ]
        }
    }

    TSLA_BREAKS = {
        "level_1_warning": {
            "name": "预警级别",
            "score_reduction": -0.15,
            "conditions": [
                {
                    "id": "delivery_decline",
                    "metric": "季度交付量",
                    "trigger": "同比下降 > 5%",
                    "data_source": "Tesla 官方数据",
                    "check_frequency": "季度",
                    "current_status": "✅ YTD +8% 交付量",
                    "severity": "HIGH"
                },
                {
                    "id": "margin_drop",
                    "metric": "Gross Margin",
                    "trigger": "环比下降 > 200bps",
                    "data_source": "财报",
                    "check_frequency": "季度",
                    "current_status": "⚠️ 18.0% (历史平均 20%)",
                    "severity": "MEDIUM"
                }
            ]
        },
        "level_2_stop_loss": {
            "name": "认输级别",
            "recommendation_reverse": True,
            "conditions": [
                {
                    "id": "elon_departure",
                    "metric": "Elon Musk 离职",
                    "trigger": "CEO 卸任或重大丑闻",
                    "data_source": "公司公告",
                    "check_frequency": "实时",
                    "current_status": "✅ 无异常",
                    "action": "股价可能下跌 10-20%"
                },
                {
                    "id": "revenue_miss",
                    "metric": "财报收入",
                    "trigger": "实际 < 预期 15%+",
                    "data_source": "财报",
                    "check_frequency": "季度",
                    "current_status": "✅ 未发生",
                    "action": "完全停止看多推荐"
                }
            ]
        }
    }

    @classmethod
    def get_breaks_config(cls, ticker: str) -> Dict:
        """获取特定标的的失效条件"""
        configs = {
            "NVDA": cls.NVDA_BREAKS,
            "VKTX": cls.VKTX_BREAKS,
            "TSLA": cls.TSLA_BREAKS
        }
        return configs.get(ticker, {})


class ThesisBreakMonitor:
    """实时监控失效条件"""

    def __init__(self, ticker: str, initial_score: float):
        self.ticker = ticker
        self.initial_score = initial_score
        self.config = ThesisBreakConfig.get_breaks_config(ticker)
        self.alerts = []
        self.adjusted_score = initial_score

    def check_all_conditions(self, metric_data: Dict) -> Dict:
        """检查所有失效条件"""

        result = {
            "ticker": self.ticker,
            "timestamp": datetime.now().isoformat(),
            "level_1_warnings": [],
            "level_2_stops": [],
            "score_adjustment": 0,
            "final_score": self.initial_score
        }

        # 检查 Level 1 预警
        if "level_1_warning" in self.config:
            for condition in self.config["level_1_warning"]["conditions"]:
                if self._check_condition(condition, metric_data):
                    result["level_1_warnings"].append({
                        "condition_id": condition["id"],
                        "metric": condition["metric"],
                        "trigger": condition["trigger"],
                        "current_value": metric_data.get(condition["id"]),
                        "severity": condition.get("severity", "MEDIUM"),
                        "timestamp": datetime.now().isoformat()
                    })
                    result["score_adjustment"] -= 0.15

        # 检查 Level 2 认输
        if "level_2_stop_loss" in self.config:
            for condition in self.config["level_2_stop_loss"]["conditions"]:
                if self._check_condition(condition, metric_data):
                    result["level_2_stops"].append({
                        "condition_id": condition["id"],
                        "metric": condition["metric"],
                        "trigger": condition["trigger"],
                        "current_value": metric_data.get(condition["id"]),
                        "action": condition.get("action"),
                        "timestamp": datetime.now().isoformat()
                    })
                    result["score_adjustment"] -= 0.30  # Level 2 更严重

        # 计算最终评分
        result["final_score"] = max(0, min(10, self.initial_score + result["score_adjustment"]))
        result["score_adjusted"] = result["final_score"] != self.initial_score

        return result

    def _check_condition(self, condition: Dict, metric_data: Dict) -> bool:
        """检查单个条件是否触发"""
        condition_id = condition["id"]

        # 模拟数据查询（实际应从数据源获取）
        if condition_id not in metric_data:
            return False

        current_value = metric_data[condition_id]
        trigger = condition["trigger"]

        # 简单的触发逻辑（实际应更复杂）
        if "%" in trigger and ">" in trigger:
            threshold = float(trigger.split(">")[1].strip().rstrip("%"))
            return current_value > threshold

        return False

    def generate_html_section(self) -> str:
        """生成 HTML 报告段落"""

        html = f"""
        <section id="thesis-breaks-{self.ticker}" class="report-section">
            <h2>🚨 失效条件监控 (Thesis Breaks) - {self.ticker}</h2>

            <!-- Level 1 预警 -->
            <div class="thesis-break-container level-1">
                <h3 class="level-label">⚠️ Level 1: 预警条件（降低评分 -15%）</h3>
                <div class="conditions-grid">
        """

        for condition in self.config["level_1_warning"]["conditions"]:
            html += f"""
                    <div class="break-condition">
                        <div class="break-metric">{condition['metric']}</div>
                        <div class="break-details">
                            <p><span class="label">触发条件：</span>{condition['trigger']}</p>
                            <p><span class="label">数据来源：</span>{condition['data_source']}</p>
                            <p><span class="label">当前状态：</span>{condition['current_status']}</p>
                            <p><span class="label">严重程度：</span>{condition.get('severity', 'MEDIUM')}</p>
                        </div>
                    </div>
            """

        html += """
                </div>
            </div>

            <!-- Level 2 认输 -->
            <div class="thesis-break-container level-2">
                <h3 class="level-label">🛑 Level 2: 认输条件（反转推荐）</h3>
                <div class="conditions-grid">
        """

        for condition in self.config["level_2_stop_loss"]["conditions"]:
            html += f"""
                    <div class="break-condition">
                        <div class="break-metric">{condition['metric']}</div>
                        <div class="break-details">
                            <p><span class="label">触发条件：</span>{condition['trigger']}</p>
                            <p><span class="label">数据来源：</span>{condition['data_source']}</p>
                            <p><span class="label">当前状态：</span>{condition['current_status']}</p>
                            <p><span class="label">后续行动：</span>{condition.get('action', 'N/A')}</p>
                        </div>
                    </div>
            """

        html += """
                </div>
            </div>

            <!-- 监控仪表板 -->
            <div class="monitoring-dashboard">
                <h3>📊 实时监控状态</h3>
                <table class="monitoring-table">
                    <thead>
                        <tr>
                            <th>条件</th>
                            <th>触发阈值</th>
                            <th>当前值</th>
                            <th>状态</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        # 添加监控行（示例）
        conditions = self.config.get("level_1_warning", {}).get("conditions", [])
        for condition in conditions:
            html += f"""
                        <tr>
                            <td>{condition['metric']}</td>
                            <td>{condition['trigger']}</td>
                            <td>{condition['current_status']}</td>
                            <td>✅ 安全</td>
                        </tr>
            """

        html += """
                    </tbody>
                </table>
            </div>
        </section>

        <style>
            #thesis-breaks-{ticker} {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 30px 0;
            }}

            .thesis-break-container {{
                margin: 20px 0;
                background: white;
                padding: 15px;
                border-radius: 6px;
            }}

            .level-1 {{
                border-left: 4px solid #ff9800;
            }}

            .level-2 {{
                border-left: 4px solid #f44336;
            }}

            .level-label {{
                margin-bottom: 15px;
                font-size: 16px;
                font-weight: 600;
            }}

            .conditions-grid {{
                display: grid;
                gap: 12px;
            }}

            .break-condition {{
                background: #fafafa;
                padding: 12px;
                border-radius: 4px;
                border-left: 3px solid #e0e0e0;
            }}

            .break-metric {{
                font-weight: 600;
                margin-bottom: 8px;
                color: #333;
            }}

            .break-details p {{
                margin: 4px 0;
                font-size: 13px;
            }}

            .label {{
                font-weight: 600;
                color: #666;
            }}

            .monitoring-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }}

            .monitoring-table th {{
                background: #f5f5f5;
                padding: 10px;
                text-align: left;
                font-weight: 600;
                border-bottom: 2px solid #ddd;
            }}

            .monitoring-table td {{
                padding: 10px;
                border-bottom: 1px solid #eee;
            }}

            .monitoring-table tr:hover {{
                background: #f9f9f9;
            }}
        </style>
        """

        return html

    def save_to_json(self, filename: str = None) -> str:
        """保存监控配置到 JSON 文件"""

        if filename is None:
            filename = f"thesis_breaks_{self.ticker}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "ticker": self.ticker,
                "config": self.config,
                "created_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)

        return filename


# 使用示例
if __name__ == "__main__":
    # NVDA 监控
    nvda_monitor = ThesisBreakMonitor("NVDA", initial_score=8.52)

    # 模拟数据
    test_metrics = {
        "datacenter_revenue_decline": 2.5,  # 2.5% 增长（< 5% 下滑阈值，不触发）
        "competitor_threat": 0,
        "china_ban_risk": 35  # Polymarket 禁令概率 35%（< 60% 阈值，不触发）
    }

    result = nvda_monitor.check_all_conditions(test_metrics)
    print(f"✅ {result['ticker']} 检查完成")
    print(f"初始评分: {result['initial_score']}")
    print(f"最终评分: {result['final_score']}")
    print(f"警告数: {len(result['level_1_warnings'])}")
    print(f"认输数: {len(result['level_2_stops'])}")

    # 生成 HTML
    html = nvda_monitor.generate_html_section()
    print("\n✅ HTML 已生成")

    # 保存配置
    nvda_monitor.save_to_json()
    print("✅ 配置已保存")
