#!/usr/bin/env python3
"""
🐝 Alpha Hive 蜂群 Agent 系统 - 6 个自治工蜂 + QueenDistiller
实现真正的多 Agent 并行协作与信息素驱动决策
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from pheromone_board import PheromoneBoard, PheromoneEntry
import json


class BeeAgent(ABC):
    """Agent 基类：所有 Agent 必须继承此类"""

    def __init__(self, board: PheromoneBoard):
        self.board = board

    @abstractmethod
    def analyze(self, ticker: str) -> Dict:
        """
        分析单个标的

        Args:
            ticker: 股票代码

        Returns:
            分析结果字典，包含：
            - score: 0-10 的评分
            - direction: "bullish" / "bearish" / "neutral"
            - discovery: 一句话摘要
            - source: 数据来源
            - details: 详细信息（可选）
        """
        pass

    def _publish(self, ticker: str, discovery: str, source: str, score: float, direction: str):
        """发布发现到信息素板"""
        entry = PheromoneEntry(
            agent_id=self.__class__.__name__,
            ticker=ticker,
            discovery=discovery,
            source=source,
            self_score=score,
            direction=direction
        )
        self.board.publish(entry)


class ScoutBeeNova(BeeAgent):
    """聪明钱侦察蜂 - 监控机构持仓与拥挤度"""

    def analyze(self, ticker: str) -> Dict:
        """分析机构持仓与市场拥挤度"""
        try:
            from crowding_detector import CrowdingDetector
            detector = CrowdingDetector()
            result = detector.analyze(ticker)

            # 提取关键指标
            crowding_score = result.get("crowding_score", 5.0)
            consensus = result.get("consensus_strength", 0.5)

            # 拥挤度越低越好（表示机会），越高越坏（表示风险）
            score = 10 - crowding_score if crowding_score > 0 else 5.0

            direction = "bearish" if crowding_score > 70 else ("bullish" if crowding_score < 30 else "neutral")

            discovery = f"拥挤度 {crowding_score:.0f}/100 | 共识 {consensus:.2f}"

            self._publish(ticker, discovery, "crowding_detector", score, direction)

            return {
                "score": score,
                "direction": direction,
                "discovery": discovery,
                "source": "ScoutBeeNova",
                "details": result
            }

        except Exception as e:
            return {"error": str(e), "source": "ScoutBeeNova", "score": 5.0}


class OracleBeeEcho(BeeAgent):
    """市场预期蜂 - 期权 IV、P/C Ratio、Gamma Exposure"""

    def analyze(self, ticker: str) -> Dict:
        """分析期权市场预期"""
        try:
            from options_analyzer import OptionsAgent
            agent = OptionsAgent()
            result = agent.analyze(ticker, stock_price=100.0)

            score = result.get("options_score", 5.0)
            signal_summary = result.get("signal_summary", "平衡")

            # 从 signal_summary 推断方向
            direction = "bullish" if "多" in signal_summary or "增强" in signal_summary else (
                "bearish" if "空" in signal_summary else "neutral"
            )

            discovery = signal_summary

            self._publish(ticker, discovery, "options_analyzer", score, direction)

            return {
                "score": score,
                "direction": direction,
                "discovery": discovery,
                "source": "OracleBeeEcho",
                "details": result
            }

        except Exception as e:
            return {"error": str(e), "source": "OracleBeeEcho", "score": 5.0}


class BuzzBeeWhisper(BeeAgent):
    """情绪分析蜂 - X 平台与社交舆情"""

    def analyze(self, ticker: str) -> Dict:
        """分析社交媒体情绪"""
        try:
            # 由于 Twitter/X API 受限，这里使用简化版本
            # 在实际系统中可以集成 StockTwits、Twitter API 等

            # 模拟情绪数据（在实际应用中从 StockTwits 获取）
            sentiment_score = 6.0  # 假设中性偏多
            sentiment_pct = 60  # 60% 看多

            direction = "bullish" if sentiment_pct > 55 else ("bearish" if sentiment_pct < 45 else "neutral")

            discovery = f"社交情绪 {sentiment_pct}% 看多 | 强度 {sentiment_score:.1f}/10"

            self._publish(ticker, discovery, "social_sentiment", sentiment_score, direction)

            return {
                "score": sentiment_score,
                "direction": direction,
                "discovery": discovery,
                "source": "BuzzBeeWhisper",
                "details": {"sentiment_pct": sentiment_pct}
            }

        except Exception as e:
            return {"error": str(e), "source": "BuzzBeeWhisper", "score": 5.0}


class ChronosBeeHorizon(BeeAgent):
    """催化剂追踪蜂 - 财报、事件、时间线"""

    def analyze(self, ticker: str) -> Dict:
        """分析催化剂事件与时间线"""
        try:
            from catalyst_refinement import CatalystRefinement
            refiner = CatalystRefinement()
            catalysts = refiner.get_catalysts(ticker)

            if catalysts:
                # 有催化剂则加分
                score = 7.0 + len(catalysts) * 0.5
                discovery = f"催化剂 {len(catalysts)} 个 | 近期：{catalysts[0].get('event', 'N/A')}"
                direction = "bullish"  # 有即将发生的催化剂通常是利好信号
            else:
                score = 5.0
                discovery = "无近期催化剂"
                direction = "neutral"

            self._publish(ticker, discovery, "catalyst_refinement", min(score, 10.0), direction)

            return {
                "score": min(score, 10.0),
                "direction": direction,
                "discovery": discovery,
                "source": "ChronosBeeHorizon",
                "details": {"catalysts": catalysts[:3]}
            }

        except Exception as e:
            return {"error": str(e), "source": "ChronosBeeHorizon", "score": 5.0}


class RivalBeeVanguard(BeeAgent):
    """竞争分析与 ML 预测蜂 - 行业对标与概率预测"""

    def analyze(self, ticker: str) -> Dict:
        """分析 ML 预测与行业竞争格局"""
        try:
            from ml_predictor_extended import ExtendedMLPredictor
            predictor = ExtendedMLPredictor()
            prediction = predictor.predict(ticker)

            predicted_return = prediction.get("expected_return", 0.0)
            score = prediction.get("win_rate", 5.0) * 10 / 100 if prediction.get("win_rate") else 5.0

            direction = "bullish" if predicted_return > 0 else ("bearish" if predicted_return < 0 else "neutral")

            discovery = f"ML 预测：{predicted_return:+.2f}% | 胜率 {prediction.get('win_rate', 50):.0f}%"

            self._publish(ticker, discovery, "ml_predictor_extended", min(score, 10.0), direction)

            return {
                "score": min(score, 10.0),
                "direction": direction,
                "discovery": discovery,
                "source": "RivalBeeVanguard",
                "details": prediction
            }

        except Exception as e:
            return {"error": str(e), "source": "RivalBeeVanguard", "score": 5.0}


class GuardBeeSentinel(BeeAgent):
    """交叉验证与风险评估蜂 - 读取信息素板进行共振检测与风险调整"""

    def analyze(self, ticker: str) -> Dict:
        """交叉验证所有 Agent 发现并检测共振"""
        try:
            # 检测信息素板中的共振信号
            resonance = self.board.detect_resonance(ticker)
            top_signals = self.board.get_top_signals(ticker, n=3)

            # 如果有共振，则加强信号
            if resonance["resonance_detected"]:
                score = 7.5  # 多个 Agent 同向的基础分
                direction = resonance["direction"]
                discovery = f"信号共振✅ {resonance['supporting_agents']} 个 Agent 同向"
            else:
                # 无共振则保守评估
                avg_score = sum(e.self_score for e in top_signals) / len(top_signals) if top_signals else 5.0
                score = avg_score * 0.8  # 打 80% 折扣
                direction = "neutral"
                discovery = f"信号分散 | 平均分 {avg_score:.1f}"

            self._publish(ticker, discovery, "guard_bee_sentinel", score, direction)

            return {
                "score": score,
                "direction": direction,
                "discovery": discovery,
                "source": "GuardBeeSentinel",
                "details": {
                    "resonance": resonance,
                    "top_signals_count": len(top_signals)
                }
            }

        except Exception as e:
            return {"error": str(e), "source": "GuardBeeSentinel", "score": 5.0}


class QueenDistiller:
    """王后蒸馏蜂 - 最终汇总、多数投票、加权合成"""

    def __init__(self, board: PheromoneBoard):
        self.board = board

    def distill(self, ticker: str, agent_results: List[Dict]) -> Dict:
        """
        多数投票 + 加权合成，生成最终判断

        Args:
            ticker: 股票代码
            agent_results: 6 个 Agent 的分析结果

        Returns:
            最终蒸馏结果
        """
        # 过滤有效结果（无错误）
        valid_results = [r for r in agent_results if r and "error" not in r]

        # 提取分数
        scores = [r.get("score", 5.0) for r in valid_results]
        avg_score = sum(scores) / len(scores) if scores else 5.0

        # 检测共振
        resonance = self.board.detect_resonance(ticker)

        # 应用共振增强：如果有共振，提升 20~30%
        if resonance["resonance_detected"]:
            boost = resonance["confidence_boost"] / 100.0 * avg_score
            final_score = min(10.0, avg_score + boost * 0.3)  # 最多提升 30%
        else:
            final_score = avg_score

        # 多数投票确定方向
        directions = [r.get("direction", "neutral") for r in valid_results]
        bullish_count = directions.count("bullish")
        bearish_count = directions.count("bearish")

        if bullish_count > bearish_count:
            final_direction = "bullish"
        elif bearish_count > bullish_count:
            final_direction = "bearish"
        else:
            final_direction = "neutral"

        return {
            "ticker": ticker,
            "final_score": round(final_score, 2),
            "direction": final_direction,
            "resonance": resonance,
            "supporting_agents": len(valid_results),
            "agent_breakdown": {
                "bullish": bullish_count,
                "bearish": bearish_count,
                "neutral": directions.count("neutral")
            },
            "pheromone_snapshot": self.board.snapshot()
        }
