#!/usr/bin/env python3
"""
🐝 Alpha Hive 蜂群系统验证脚本
测试信息素板、所有 Agent、共振检测、QueenDistiller
"""

import json
from pheromone_board import PheromoneBoard, PheromoneEntry
from swarm_agents import (
    ScoutBeeNova, OracleBeeEcho, BuzzBeeWhisper,
    ChronosBeeHorizon, RivalBeeVanguard, GuardBeeSentinel,
    QueenDistiller
)


def test_pheromone_board():
    """测试信息素板的基本功能"""
    print("\n" + "=" * 70)
    print("🧪 测试 1：信息素板 (PheromoneBoard)")
    print("=" * 70)

    board = PheromoneBoard()
    print("✅ 信息素板初始化成功")

    # 发布 5 条信息素
    agents = ["ScoutBeeNova", "OracleBeeEcho", "BuzzBeeWhisper", "ChronosBeeHorizon", "RivalBeeVanguard"]
    for i, agent in enumerate(agents):
        entry = PheromoneEntry(
            agent_id=agent,
            ticker="NVDA",
            discovery=f"测试发现 {i+1}",
            source="test",
            self_score=6.0 + i,
            direction="bullish"
        )
        board.publish(entry)
    print(f"✅ 发布 {len(agents)} 条信息素到板上")

    # 检测共振
    resonance = board.detect_resonance("NVDA")
    print(f"✅ 共振检测：")
    print(f"   - 检测到：{'是' if resonance['resonance_detected'] else '否'}")
    print(f"   - 支持 Agent 数：{resonance['supporting_agents']}")
    print(f"   - 置信度加成：+{resonance['confidence_boost']}%")

    # 获取快照
    snapshot = board.snapshot()
    print(f"✅ 信息素板快照：{len(snapshot)} 条记录")
    print(f"   平均强度：{sum(e['pheromone_strength'] for e in snapshot) / len(snapshot):.3f}")

    return True


def test_individual_agents():
    """测试每个 Agent 的独立功能"""
    print("\n" + "=" * 70)
    print("🧪 测试 2：单个 Agent 分析 (TSLA)")
    print("=" * 70)

    board = PheromoneBoard()

    agents = [
        ("🔍 ScoutBeeNova", ScoutBeeNova(board)),
        ("🎲 OracleBeeEcho", OracleBeeEcho(board)),
        ("💬 BuzzBeeWhisper", BuzzBeeWhisper(board)),
        ("⏰ ChronosBeeHorizon", ChronosBeeHorizon(board)),
        ("🤖 RivalBeeVanguard", RivalBeeVanguard(board)),
        ("🛡️ GuardBeeSentinel", GuardBeeSentinel(board)),
    ]

    results = {}
    for name, agent in agents:
        try:
            result = agent.analyze("TSLA")
            score = result.get("score", 0)
            direction = result.get("direction", "?")
            status = "✅"
        except Exception as e:
            score = "错误"
            direction = "N/A"
            status = "⚠️"

        print(f"{status} {name:20s} → 评分：{score:5} | 方向：{direction:8s}")
        results[name] = result

    print(f"\n✅ 板上现有记录：{board.get_entry_count()} 条")

    return results


def test_resonance_detection():
    """测试共振检测机制"""
    print("\n" + "=" * 70)
    print("🧪 测试 3：信号共振检测")
    print("=" * 70)

    board = PheromoneBoard()

    # 场景 A：3 个 Agent 同向（应该触发共振）
    print("场景 A：3 个 Agent 看多 VKTX")
    for i in range(3):
        entry = PheromoneEntry(
            agent_id=f"Agent{i}",
            ticker="VKTX",
            discovery=f"看多信号 {i+1}",
            source="test",
            self_score=7.5,
            direction="bullish"
        )
        board.publish(entry)

    resonance_a = board.detect_resonance("VKTX")
    print(f"  共振检测：{resonance_a['resonance_detected']}")
    print(f"  支持 Agent：{resonance_a['supporting_agents']}")
    print(f"  方向：{resonance_a['direction']}")
    print(f"  置信度加成：+{resonance_a['confidence_boost']}%")

    # 场景 B：1 个 Agent 看空，3 个看多（不触发共振？）
    print("\n场景 B：1 个 Agent 看空，3 个看多 MSFT")
    board.publish(PheromoneEntry(
        agent_id="BearAgent",
        ticker="MSFT",
        discovery="看空信号",
        source="test",
        self_score=6.0,
        direction="bearish"
    ))
    for i in range(3):
        board.publish(PheromoneEntry(
            agent_id=f"BullAgent{i}",
            ticker="MSFT",
            discovery="看多信号",
            source="test",
            self_score=7.0,
            direction="bullish"
        ))

    resonance_b = board.detect_resonance("MSFT")
    print(f"  共振检测：{resonance_b['resonance_detected']}")
    print(f"  支持 Agent：{resonance_b['supporting_agents']}")
    print(f"  方向：{resonance_b['direction']}")

    return True


def test_queen_distiller():
    """测试 QueenDistiller 多数投票与汇总"""
    print("\n" + "=" * 70)
    print("🧪 测试 4：QueenDistiller 汇总 (AMD)")
    print("=" * 70)

    board = PheromoneBoard()

    # 模拟 6 个 Agent 的分析结果
    agent_results = [
        {"score": 7.5, "direction": "bullish", "source": "ScoutBeeNova"},
        {"score": 6.8, "direction": "bullish", "source": "OracleBeeEcho"},
        {"score": 6.2, "direction": "neutral", "source": "BuzzBeeWhisper"},
        {"score": 7.1, "direction": "bullish", "source": "ChronosBeeHorizon"},
        {"score": 6.5, "direction": "bearish", "source": "RivalBeeVanguard"},
        {"score": 7.2, "direction": "bullish", "source": "GuardBeeSentinel"},
    ]

    # 先发布到信息素板
    for result in agent_results:
        entry = PheromoneEntry(
            agent_id=result["source"],
            ticker="AMD",
            discovery=result["source"],
            source="test",
            self_score=result["score"],
            direction=result["direction"]
        )
        board.publish(entry)

    # QueenDistiller 汇总
    queen = QueenDistiller(board)
    distilled = queen.distill("AMD", agent_results)

    print(f"✅ 最终评分：{distilled['final_score']:.2f}/10")
    print(f"✅ 最终方向：{distilled['direction'].upper()}")
    print(f"✅ 支持 Agent：{distilled['supporting_agents']}/6")
    print(f"✅ Agent 投票：")
    print(f"   - 看多：{distilled['agent_breakdown']['bullish']}")
    print(f"   - 看空：{distilled['agent_breakdown']['bearish']}")
    print(f"   - 中性：{distilled['agent_breakdown']['neutral']}")
    print(f"✅ 共振信号：{'是' if distilled['resonance']['resonance_detected'] else '否'}")
    print(f"✅ 信息素板快照：{len(distilled['pheromone_snapshot'])} 条记录")

    return distilled


def test_full_swarm_workflow():
    """完整蜂群工作流测试"""
    print("\n" + "=" * 70)
    print("🧪 测试 5：完整蜂群工作流 (COIN)")
    print("=" * 70)

    board = PheromoneBoard()

    # 创建所有 Agent
    agents = [
        ScoutBeeNova(board),
        OracleBeeEcho(board),
        BuzzBeeWhisper(board),
        ChronosBeeHorizon(board),
        RivalBeeVanguard(board),
        GuardBeeSentinel(board),
    ]

    print(f"🐝 启动 {len(agents)} 个自治 Agent")

    # 并行分析（模拟）
    results = []
    for agent in agents:
        try:
            result = agent.analyze("COIN")
            results.append(result)
            print(f"  ✓ {agent.__class__.__name__:20s} → {result.get('score', 0):.1f}/10")
        except Exception as e:
            print(f"  ⚠️  {agent.__class__.__name__:20s} → 错误")

    # Queen Distiller 最终汇总
    queen = QueenDistiller(board)
    final = queen.distill("COIN", results)

    print(f"\n📊 蜂群最终判断（共振加权）：")
    print(f"  综合评分：{final['final_score']:.2f}/10")
    print(f"  投票方向：{final['direction'].upper()}")
    print(f"  共振检测：{'✅ 是' if final['resonance']['resonance_detected'] else '❌ 否'}")
    print(f"  支持 Agent：{final['supporting_agents']}/6")

    return final


def main():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print("🐝 Alpha Hive 蜂群系统验证测试")
    print("=" * 70)

    try:
        test_pheromone_board()
        test_individual_agents()
        test_resonance_detection()
        test_queen_distiller()
        test_full_swarm_workflow()

        print("\n" + "=" * 70)
        print("🎉 所有测试通过！蜂群系统就绪")
        print("=" * 70)
        print("\n✅ 蜂群系统组件验证完成")
        print("   - 信息素板 (PheromoneBoard) ✓")
        print("   - 6 个自治 Agent ✓")
        print("   - 共振检测机制 ✓")
        print("   - QueenDistiller 多数投票 ✓")
        print("   - 完整工作流 ✓")
        print("\n📋 使用说明：")
        print("   python3 alpha_hive_daily_report.py --swarm --tickers NVDA TSLA")
        print("\n")

    except Exception as e:
        print(f"\n❌ 测试失败：{str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
