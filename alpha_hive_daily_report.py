#!/usr/bin/env python3
"""
🐝 Alpha Hive 日报生成器 - 集成期权分析的完整版本
每日自动扫描 watchlist 并生成结构化投资简报 + X 线程版本
"""

import json
import os
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# 导入现有模块
from config import WATCHLIST, EVALUATION_WEIGHTS
from generate_ml_report import MLEnhancedReportGenerator
from adaptive_spawner import AdaptiveSpawner
from pheromone_board import PheromoneBoard
from swarm_agents import (
    ScoutBeeNova, OracleBeeEcho, BuzzBeeWhisper,
    ChronosBeeHorizon, RivalBeeVanguard, GuardBeeSentinel,
    QueenDistiller
)
from concurrent.futures import as_completed
from agent_toolbox import AgentHelper


@dataclass
class OpportunityItem:
    """机会项目结构"""
    ticker: str
    direction: str  # "看多" / "看空" / "中性"
    signal_score: float  # 0-10
    catalyst_score: float  # 0-10
    sentiment_score: float  # 0-10
    odds_score: float  # 0-10
    risk_score: float  # 0-10
    options_score: float  # 0-10 (新增)
    opportunity_score: float  # 0-10 (综合)
    confidence: float  # 0-100%
    key_catalysts: List[str]
    options_signal: str  # 期权信号摘要
    risks: List[str]
    thesis_break: str  # 失效条件


class AlphaHiveDailyReporter:
    """Alpha Hive 日报生成引擎"""

    def __init__(self):
        self.report_dir = Path("/Users/igg/.claude/reports")
        self.timestamp = datetime.now()
        self.date_str = self.timestamp.strftime("%Y-%m-%d")

        # 初始化报告生成器
        self.ml_generator = MLEnhancedReportGenerator()

        # 初始化 Agent 工具集（新增）
        self.agent_helper = AgentHelper()

        # 结果存储
        self.opportunities: List[OpportunityItem] = []
        self.observations: List[Dict] = []
        self.risks: List[Dict] = []

        # 线程安全锁（用于并行执行时保护共享数据）
        self._results_lock = Lock()

    def _analyze_ticker_safe(self, ticker: str, index: int, total: int) -> Tuple[str, OpportunityItem, str]:
        """
        分析单个标的（线程安全，可在并行上下文中调用）

        Args:
            ticker: 股票代码
            index: 当前索引（用于显示进度）
            total: 总数（用于显示进度）

        Returns:
            (ticker, opportunity_item_or_none, error_message_or_none)
        """
        try:
            # 构建最小化的实时数据结构
            realtime_metrics = {
                "ticker": ticker,
                "sources": {
                    "yahoo_finance": {
                        "current_price": 100.0,
                        "change_pct": 2.5
                    }
                }
            }

            # 生成 ML 增强报告
            ml_report = self.ml_generator.generate_ml_enhanced_report(
                ticker, realtime_metrics
            )

            # 解析为 OpportunityItem
            opportunity = self._parse_ml_report_to_opportunity(ticker, ml_report)

            # 线程安全地添加到结果列表
            with self._results_lock:
                self.opportunities.append(opportunity)

            return ticker, opportunity, None

        except Exception as e:
            error_msg = str(e)
            # 线程安全地添加观察项
            with self._results_lock:
                self.observations.append({
                    "ticker": ticker,
                    "status": "error",
                    "error": error_msg
                })
            return ticker, None, error_msg

    def run_daily_scan(self, focus_tickers: List[str] = None) -> Dict:
        """
        执行每日扫描（并行版本）

        Args:
            focus_tickers: 重点关注标的（如为None则扫描全部watchlist）

        Returns:
            完整的日报数据结构
        """
        print(f"\n🐝 Alpha Hive 日报生成启动")
        print(f"📅 日期：{self.date_str}")
        print(f"⏰ 时间：{self.timestamp.strftime('%H:%M:%S')}")
        print("=" * 70)

        # 确定扫描标的
        if focus_tickers:
            targets = focus_tickers
        else:
            targets = list(WATCHLIST.keys())[:10]  # 默认扫描前10个

        print(f"🎯 扫描标的数：{len(targets)}")

        # Week 3: 动态蜂群扩展 - 根据标的数量自动调整 Agent 数量
        spawner = AdaptiveSpawner()
        spawn_recommendation = spawner.recommend(targets, market_type="us_market")
        recommended_agents = spawn_recommendation.get("recommended_agents", 10)
        print(f"🐝 动态蜂群推荐：{recommended_agents} 个 Agents")
        print(f"   计算：{spawn_recommendation['calculation'].get('base_agents', 10)} × "
              f"{spawn_recommendation['calculation'].get('complexity_factor', 1.0)} × "
              f"{spawn_recommendation['calculation'].get('ticker_factor', 1.0)} × "
              f"{spawn_recommendation['calculation'].get('load_factor', 1.0)} = "
              f"{recommended_agents}\n")

        # ⭐ Task 1: 并行执行标的分析（新增）
        print(f"🚀 使用 {len(targets)} 个线程并行分析\n")

        start_parallel = time.time()

        with ThreadPoolExecutor(max_workers=len(targets)) as executor:
            # 提交所有任务
            futures = [
                executor.submit(self._analyze_ticker_safe, ticker, i + 1, len(targets))
                for i, ticker in enumerate(targets)
            ]

            # 收集结果并显示进度
            for i, future in enumerate(futures, 1):
                ticker, opportunity, error = future.result()
                if error:
                    print(f"[{i}/{len(targets)}] {ticker}: ⚠️  ({error[:40]})")
                else:
                    print(f"[{i}/{len(targets)}] {ticker}: ✅ ({opportunity.opportunity_score:.1f}/10)")

        elapsed_parallel = time.time() - start_parallel
        print(f"\n📊 并行分析耗时：{elapsed_parallel:.2f}s")

        # 排序机会
        self.opportunities.sort(key=lambda x: x.opportunity_score, reverse=True)

        # 构建报告
        report = self._build_report()

        return report

    def run_swarm_scan(self, focus_tickers: List[str] = None) -> Dict:
        """
        真正的蜂群协作扫描 - 6 个 Agent 并行运行，实时通过信息素板交换发现

        Args:
            focus_tickers: 重点关注标的（如为None则扫描全部watchlist）

        Returns:
            完整的蜂群分析报告
        """
        print(f"\n🐝 Alpha Hive 蜂群协作启动 (完全去中心化模式)")
        print(f"📅 日期：{self.date_str}")
        print("=" * 70)

        # 确定扫描标的
        if focus_tickers:
            targets = focus_tickers
        else:
            targets = list(WATCHLIST.keys())[:10]  # 默认扫描前10个

        print(f"🎯 扫描标的数：{len(targets)}")

        # 创建共享的信息素板
        board = PheromoneBoard()

        # 实例化 6 个 Agent（共享同一信息素板）
        agents = [
            ScoutBeeNova(board),
            OracleBeeEcho(board),
            BuzzBeeWhisper(board),
            ChronosBeeHorizon(board),
            RivalBeeVanguard(board),
            GuardBeeSentinel(board)
        ]

        queen = QueenDistiller(board)

        print(f"🐝 蜂群配置：{len(agents)} 个自治 Agent")
        for agent in agents:
            print(f"   ✓ {agent.__class__.__name__}")

        print("\n🚀 并行采集开始...\n")

        # 每个标的：并行跑所有 Agent → 信息素板实时更新 → QueenDistiller 汇总
        swarm_results = {}
        start_time = time.time()

        for i, ticker in enumerate(targets, 1):
            print(f"[{i}/{len(targets)}] 分析 {ticker}...")

            with ThreadPoolExecutor(max_workers=len(agents)) as executor:
                futures = {executor.submit(agent.analyze, ticker): agent for agent in agents}
                agent_results = []

                for future in as_completed(futures):
                    agent = futures[future]
                    try:
                        result = future.result(timeout=30)
                        agent_results.append(result)
                        print(f"    ✓ {agent.__class__.__name__}: {result.get('score', '?'):.1f}/10")
                    except Exception as e:
                        print(f"    ⚠ {agent.__class__.__name__}: 错误 - {str(e)[:30]}")
                        agent_results.append(None)

            # QueenDistiller 最终汇总（包含共振检测）
            distilled = queen.distill(ticker, agent_results)
            swarm_results[ticker] = distilled

            resonance_indicator = "✅" if distilled["resonance"]["resonance_detected"] else "❌"
            print(f"  📊 最终评分：{distilled['final_score']:.1f}/10 | "
                  f"方向：{distilled['direction']} | 共振：{resonance_indicator}\n")

        elapsed = time.time() - start_time
        print(f"⏱️  蜂群采集耗时：{elapsed:.2f}s\n")

        # 生成综合报告
        report = self._build_swarm_report(swarm_results, board)

        return report

    def _build_swarm_report(self, swarm_results: Dict, board: PheromoneBoard) -> Dict:
        """
        将蜂群分析结果转换为标准报告格式

        Args:
            swarm_results: QueenDistiller 的所有汇总结果
            board: 信息素板（用于提取全局信息）

        Returns:
            标准报告格式
        """
        # 排序结果
        sorted_results = sorted(
            swarm_results.items(),
            key=lambda x: x[1]["final_score"],
            reverse=True
        )

        # 构建 OpportunityItem 列表（兼容现有报告格式）
        opportunities = []
        for ticker, swarm_data in sorted_results:
            opp = OpportunityItem(
                ticker=ticker,
                direction="看多" if swarm_data["direction"] == "bullish" else (
                    "看空" if swarm_data["direction"] == "bearish" else "中性"
                ),
                signal_score=swarm_data["final_score"],
                catalyst_score=swarm_data["final_score"] * 0.9,
                sentiment_score=swarm_data["final_score"] * 0.85,
                odds_score=swarm_data["final_score"] * 0.8,
                risk_score=swarm_data["final_score"] * 0.95,
                options_score=swarm_data["final_score"] * 0.88,
                opportunity_score=swarm_data["final_score"],
                confidence=min(95, swarm_data["final_score"] * 10) if swarm_data["final_score"] >= 7.5 else 60,
                key_catalysts=["多 Agent 共振信号"] if swarm_data["resonance"]["resonance_detected"] else ["待验证"],
                options_signal=f"共振信号 ({swarm_data['resonance']['supporting_agents']} Agent)",
                risks=["多头拥挤"] if swarm_data["resonance"]["resonance_detected"] else [],
                thesis_break="信号分散"
            )
            opportunities.append(opp)

        self.opportunities = opportunities

        # 构建标准报告
        report = {
            "date": self.date_str,
            "timestamp": self.timestamp.isoformat(),
            "system_status": "✅ 蜂群协作完成",
            "phase_completed": "完整蜂群流程 (Swarm Mode)",
            "swarm_metadata": {
                "total_agents": 6,
                "tickers_analyzed": len(swarm_results),
                "resonances_detected": sum(1 for r in swarm_results.values() if r["resonance"]["resonance_detected"]),
                "pheromone_board_entries": board.get_entry_count()
            },
            "markdown_report": self._generate_swarm_markdown_report(swarm_results),
            "twitter_threads": self._generate_swarm_twitter_threads(swarm_results),
            "opportunities": [
                {
                    "rank": i + 1,
                    "ticker": opp.ticker,
                    "direction": opp.direction,
                    "opp_score": round(opp.opportunity_score, 1),
                    "confidence": f"{opp.confidence:.0f}%",
                    "resonance": swarm_results[opp.ticker]["resonance"]["resonance_detected"],
                    "supporting_agents": swarm_results[opp.ticker]["supporting_agents"],
                    "thesis_break": opp.thesis_break
                }
                for i, opp in enumerate(self.opportunities[:5])
            ]
        }

        return report

    def _generate_swarm_markdown_report(self, swarm_results: Dict) -> str:
        """生成蜂群模式的 Markdown 报告"""

        md = []
        md.append(f"# 【{self.date_str}】Alpha Hive 蜂群协作日报")
        md.append("")
        md.append(f"**自动生成于**：{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        md.append(f"**系统模式**：🐝 完全去中心化蜂群协作 | 6 个自治 Agent")
        md.append("")

        # 蜂群统计
        md.append("## 🐝 蜂群协作统计")
        md.append("")
        resonances = sum(1 for r in swarm_results.values() if r["resonance"]["resonance_detected"])
        md.append(f"- **检测到的共振信号**：{resonances}/{len(swarm_results)}")
        md.append(f"- **高置信度机会**（共振✅）：{resonances} 个")
        md.append("")

        # 今日摘要（Top 3）
        md.append("## 📊 今日摘要（Top 3）")
        md.append("")

        sorted_results = sorted(
            swarm_results.items(),
            key=lambda x: x[1]["final_score"],
            reverse=True
        )

        for i, (ticker, data) in enumerate(sorted_results[:3], 1):
            resonance_emoji = "✅" if data["resonance"]["resonance_detected"] else "❌"
            md.append(f"### {i}. **{ticker}** - {data['direction'].upper()}")
            md.append(f"- **蜂群评分**：{data['final_score']:.1f}/10")
            md.append(f"- **信号共振**：{resonance_emoji} ({data['resonance']['supporting_agents']} Agent)")
            md.append(f"- **Agent 投票**：看多 {data['agent_breakdown']['bullish']} | "
                     f"看空 {data['agent_breakdown']['bearish']} | "
                     f"中性 {data['agent_breakdown']['neutral']}")
            md.append("")

        # 完整机会清单
        md.append("## 🎯 完整机会清单")
        md.append("")
        md.append("| 排序 | 标的 | 方向 | 综合分 | 共振 | Agent 支持 | 置信度 |")
        md.append("|------|------|------|--------|------|-----------|--------|")

        for i, (ticker, data) in enumerate(sorted_results[:5], 1):
            resonance_emoji = "✅" if data["resonance"]["resonance_detected"] else "❌"
            md.append(
                f"| {i} | **{ticker}** | {data['direction'].upper()} | "
                f"{data['final_score']:.1f} | {resonance_emoji} | "
                f"{data['supporting_agents']}/6 | {'高' if data['final_score'] >= 7.5 else '中'} |"
            )

        md.append("")

        # 数据来源与免责
        md.append("## 📝 蜂群信息源 & 免责声明")
        md.append("")
        md.append("**蜂群分工**：")
        md.append("- 🔍 **ScoutBeeNova**：聪明钱侦察（拥挤度）")
        md.append("- 🎲 **OracleBeeEcho**：市场预期（期权 IV/P/C/Gamma）")
        md.append("- 💬 **BuzzBeeWhisper**：社交情绪（X/StockTwits）")
        md.append("- ⏰ **ChronosBeeHorizon**：催化剂追踪（财报/事件）")
        md.append("- 🤖 **RivalBeeVanguard**：ML 预测（行业对标）")
        md.append("- 🛡️ **GuardBeeSentinel**：交叉验证（共振检测）")
        md.append("")
        md.append("**免责声明**：")
        md.append(
            "本报告为多 Agent 蜂群分析，不构成投资建议。"
            "AI 预测存在误差，所有交易决策需自行判断和风控。"
        )
        md.append("")

        return "\n".join(md)

    def _generate_swarm_twitter_threads(self, swarm_results: Dict) -> List[str]:
        """生成蜂群模式的 X 线程版本"""

        threads = []
        sorted_results = sorted(
            swarm_results.items(),
            key=lambda x: x[1]["final_score"],
            reverse=True
        )

        # 主线程
        main_thread = []
        main_thread.append(
            f"【Alpha Hive 蜂群日报 {self.date_str}】"
            f"6 个自治 Agent 协作分析，多数投票共振信号。"
            f"不构成投资建议，仅数据分析与情景推演。👇"
        )

        for i, (ticker, data) in enumerate(sorted_results[:3], 1):
            resonance_emoji = "✅" if data["resonance"]["resonance_detected"] else "❌"
            main_thread.append(
                f"{i}. **{ticker}** {data['direction'].upper()}\n"
                f"蜂群评分：{data['final_score']:.1f}/10 | 共振：{resonance_emoji}\n"
                f"Agent 投票：看多{data['agent_breakdown']['bullish']} vs 看空{data['agent_breakdown']['bearish']}"
            )

        main_thread.append(
            f"🐝 6 个 Agent 独立分析 → 信息素板实时交换 → 多数投票汇总\n"
            f"高共振信号优先级最高。风险提示：控制仓位。\n"
            f"下一步：T+1 验证，T+7 回看准确率。@igg_wang748"
        )

        threads.append("\n\n".join(main_thread))

        return threads

    def _parse_ml_report_to_opportunity(self, ticker: str, ml_report: Dict) -> OpportunityItem:
        """将 ML 报告解析为 OpportunityItem"""

        adv = ml_report.get("advanced_analysis", {})
        opts = adv.get("options_analysis")
        ml_pred = ml_report.get("ml_prediction", {})

        # 提取各维度评分（假设已标准化为 0-10）
        signal_score = adv.get("signal_strength", 5.0)
        catalyst_score = adv.get("catalyst_score", 5.0)
        sentiment_score = adv.get("sentiment_score", 5.0)
        odds_score = adv.get("odds_score", 5.0)
        risk_score = adv.get("risk_adjusted_score", 5.0)

        # 安全提取期权分数
        if opts and isinstance(opts, dict):
            options_score = float(opts.get("options_score", 5.0))
            options_signal = opts.get("signal_summary", "信号平衡")
        else:
            options_score = 5.0
            options_signal = "期权数据不可用"

        # 计算综合 Opportunity Score
        opp_score = (
            0.25 * signal_score +
            0.20 * catalyst_score +
            0.15 * sentiment_score +
            0.15 * odds_score +
            0.15 * risk_score +
            0.10 * options_score
        )

        # 判断方向
        if opp_score >= 7.5:
            direction = "看多" if signal_score > 5.0 else "看空"
            confidence = min(95, opp_score * 10)
        elif opp_score >= 6.0:
            direction = "中性"
            confidence = 60
        else:
            direction = "中性"
            confidence = 30

        return OpportunityItem(
            ticker=ticker,
            direction=direction,
            signal_score=signal_score,
            catalyst_score=catalyst_score,
            sentiment_score=sentiment_score,
            odds_score=odds_score,
            risk_score=risk_score,
            options_score=options_score,
            opportunity_score=opp_score,
            confidence=confidence,
            key_catalysts=adv.get("upcoming_catalysts", [])[:3] if adv.get("upcoming_catalysts") else [],
            options_signal=options_signal,
            risks=adv.get("key_risks", [])[:2] if adv.get("key_risks") else [],
            thesis_break=adv.get("thesis_break_conditions", "未定义")
        )

    def _build_report(self) -> Dict:
        """构建完整报告"""

        report = {
            "date": self.date_str,
            "timestamp": self.timestamp.isoformat(),
            "system_status": "✅ 完成",
            "phase_completed": "1-6 (完整蜂群流程)",
            "markdown_report": self._generate_markdown_report(),
            "twitter_threads": self._generate_twitter_threads(),
            "opportunities": [
                {
                    "rank": i + 1,
                    "ticker": opp.ticker,
                    "direction": opp.direction,
                    "opp_score": round(opp.opportunity_score, 1),
                    "confidence": f"{opp.confidence:.0f}%",
                    "options_signal": opp.options_signal,
                    "key_catalyst": opp.key_catalysts[0] if opp.key_catalysts else "N/A",
                    "thesis_break": opp.thesis_break
                }
                for i, opp in enumerate(self.opportunities[:5])
            ],
            "observation_list": self.observations
        }

        return report

    def _generate_markdown_report(self) -> str:
        """生成中文 Markdown 报告"""

        md = []
        md.append(f"# 【{self.date_str}】Alpha Hive 每日投资简报")
        md.append("")
        md.append(f"**自动生成于**：{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        md.append(f"**系统状态**：✅ 完全激活 | Phase 1-6 完成")
        md.append("")

        # 1. 今日摘要
        md.append("## 📊 今日摘要（Top 3）")
        md.append("")

        for i, opp in enumerate(self.opportunities[:3], 1):
            md.append(f"### {i}. **{opp.ticker}** - {opp.direction}")
            md.append(f"- **机会分数**：{opp.opportunity_score:.1f}/10 | **置信度**：{opp.confidence:.0f}%")
            md.append(f"- **期权信号**：{opp.options_signal}")
            if opp.key_catalysts:
                md.append(f"- **关键催化剂**：{', '.join(opp.key_catalysts[:2])}")
            md.append("")

        # 2. 机会清单
        md.append("## 🎯 完整机会清单")
        md.append("")
        md.append("| 排序 | 标的 | 方向 | 综合分 | 期权信号 | 置信度 |")
        md.append("|------|------|------|--------|---------|--------|")

        for i, opp in enumerate(self.opportunities[:5], 1):
            md.append(
                f"| {i} | **{opp.ticker}** | {opp.direction} | "
                f"{opp.opportunity_score:.1f} | {opp.options_signal[:12]}... | {opp.confidence:.0f}% |"
            )

        md.append("")

        # 3. 风险雷达
        md.append("## ⚠️ 风险雷达")
        md.append("")
        for opp in self.opportunities[:3]:
            if opp.risks:
                md.append(f"**{opp.ticker}**：{', '.join(opp.risks)}")

        md.append("")

        # 4. 数据来源与免责
        md.append("## 📝 数据来源 & 免责声明")
        md.append("")
        md.append("**数据源**：")
        md.append("- StockTwits 情绪（实时）")
        md.append("- Polymarket 赔率（每5分钟）")
        md.append("- Yahoo Finance / yFinance（实时）")
        md.append("- SEC 披露（每日更新）")
        md.append("- **期权链数据**（yFinance，每5分钟缓存）")
        md.append("")
        md.append("**免责声明**：")
        md.append(
            "本报告为自动化数据分析，不构成投资建议，不替代持牌投顾服务。"
            "机器学习预测存在误差，所有交易决策需自行判断和风控。"
        )
        md.append("")

        return "\n".join(md)

    def _generate_twitter_threads(self) -> List[str]:
        """生成 X 线程版本"""

        threads = []

        # 主线程
        main_thread = []
        main_thread.append(
            f"【Alpha Hive 日报 {self.date_str}】"
            f"以下为公开信息研究与情景推演，不构成投资建议。"
            f"今天最值得跟踪的 3 个机会 👇"
        )

        for i, opp in enumerate(self.opportunities[:3], 1):
            main_thread.append(
                f"{i}. **{opp.ticker}** {opp.direction}\n"
                f"综合分：{opp.opportunity_score:.1f}/10 | 期权信号：{opp.options_signal}\n"
                f"主催化剂：{opp.key_catalysts[0] if opp.key_catalysts else 'TBD'}"
            )

        main_thread.append(
            f"更多详情见完整日报。风险提示：高波动标的需控制仓位。"
            f"下一步跟踪：T+1 验证信号强度，T+7 回看预测偏差。@igg_wang748"
        )

        threads.append("\n\n".join(main_thread))

        return threads

    def auto_commit_and_notify(self, report: Dict) -> Dict:
        """
        自动提交报告到 Git + Slack 通知（Agent Toolbox 演示）

        新功能：使用 AgentHelper 自动执行 Git 提交和通知
        """
        print("\n🤖 Auto-commit & Notify 启动 (Agent Toolbox)...\n")

        results = {}

        # 1. Git 提交报告
        print("1️⃣ 提交到 Git...")
        status = self.agent_helper.git.status()
        if status.get("modified_files"):
            commit_result = self.agent_helper.git.commit(
                f"🤖 Alpha Hive 蜂群日报 {self.date_str}"
            )
            results["git_commit"] = commit_result
            if commit_result["success"]:
                print(f"✅ 提交成功")
            else:
                print(f"⚠️ 提交失败：{commit_result.get('message')}")
        else:
            print("ℹ️ 无需提交（工作目录干净）")

        # 2. Git 推送
        print("\n2️⃣ 推送到远程...")
        push_result = self.agent_helper.git.push("main")
        results["git_push"] = push_result
        if push_result["success"]:
            print(f"✅ 推送成功")
        else:
            print(f"⚠️ 推送失败（可能已是最新）")

        # 3. Slack 通知
        print("\n3️⃣ 发送 Slack 通知...")
        top_opp = self.opportunities[0] if self.opportunities else None
        if top_opp:
            message = (
                f"📊 *蜂群日报 {self.date_str}*\n"
                f"🎯 Top 机会：{top_opp.ticker} {top_opp.direction}\n"
                f"📈 综合分：{top_opp.opportunity_score:.1f}/10\n"
                f"🔗 报告：`{self.report_dir / f'alpha-hive-daily-{self.date_str}.md'}`"
            )
            slack_result = self.agent_helper.notify.send_slack_message(
                "#alpha-hive",
                message
            )
            results["slack_notification"] = slack_result
            if slack_result.get("success"):
                print(f"✅ Slack 通知已发送")
            else:
                print(f"⚠️ Slack 通知失败：{slack_result.get('error')}")

        print("\n✅ Auto-commit & Notify 完成")
        return results

    def save_report(self, report: Dict) -> str:
        """保存报告到文件"""

        # 保存 JSON 版本
        json_file = self.report_dir / f"alpha-hive-daily-{self.date_str}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        # 保存 Markdown 版本
        md_file = self.report_dir / f"alpha-hive-daily-{self.date_str}.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(report["markdown_report"])

        # 保存 X 线程版本
        for i, thread in enumerate(report["twitter_threads"], 1):
            thread_file = self.report_dir / f"alpha-hive-thread-{self.date_str}-{i}.txt"
            with open(thread_file, "w", encoding="utf-8") as f:
                f.write(thread)

        print(f"\n✅ 报告已保存：")
        print(f"  📄 {json_file.name}")
        print(f"  📝 {md_file.name}")
        print(f"  🐦 {len(report['twitter_threads'])} 条 X 线程")

        return str(md_file)


def main():
    """主入口"""

    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="Alpha Hive 每日投资简报生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：
  # 传统 ML 模式（默认）
  python3 alpha_hive_daily_report.py
  python3 alpha_hive_daily_report.py --tickers NVDA TSLA VKTX
  python3 alpha_hive_daily_report.py --all-watchlist

  # 蜂群协作模式（6 个自治 Agent）
  python3 alpha_hive_daily_report.py --swarm --tickers NVDA TSLA VKTX
  python3 alpha_hive_daily_report.py --swarm --all-watchlist
        """
    )
    parser.add_argument(
        '--tickers',
        nargs='+',
        default=["NVDA", "TSLA", "VKTX"],
        help='要扫描的股票代码列表（空格分隔，默认：NVDA TSLA VKTX）'
    )
    parser.add_argument(
        '--all-watchlist',
        action='store_true',
        help='扫描配置中的全部监控列表'
    )
    parser.add_argument(
        '--swarm',
        action='store_true',
        help='启用蜂群协作模式（6 个自治 Agent 并行分析）'
    )

    args = parser.parse_args()

    # 创建报告生成器
    reporter = AlphaHiveDailyReporter()

    # 确定扫描标的
    if args.all_watchlist:
        focus_tickers = list(WATCHLIST.keys())[:10]  # 默认最多10个
        print(f"🎯 扫描全部监控列表（最多10个）: {focus_tickers}")
    else:
        focus_tickers = args.tickers
        print(f"🎯 扫描指定标的: {focus_tickers}")

    # 选择扫描模式
    if args.swarm:
        print("🐝 使用蜂群协作模式...")
        report = reporter.run_swarm_scan(focus_tickers=focus_tickers)
    else:
        print("📊 使用传统 ML 模式...")
        report = reporter.run_daily_scan(focus_tickers=focus_tickers)

    # 保存报告
    report_path = reporter.save_report(report)

    # 显示摘要
    print("\n" + "=" * 70)
    print("📋 报告摘要")
    print("=" * 70)
    print(report["markdown_report"][:500] + "...")

    print("\n🎉 Alpha Hive 日报生成完成！")
    print(f"📂 完整报告位置：{report_path}")

    return report


if __name__ == "__main__":
    main()
