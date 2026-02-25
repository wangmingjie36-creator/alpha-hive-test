#!/usr/bin/env python3
"""
🐝 Alpha Hive 动态蜂群扩展系统 (Week 3)
根据任务复杂度自动调整 Agent 生成数量（8~100）
"""

import json
import argparse
import sys
import os
import traceback
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# 尝试导入 psutil，如果不可用则降级
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("⚠️ psutil 未安装，系统监控功能将降级")

# 导入配置
sys.path.insert(0, str(Path(__file__).parent))
try:
    from config import SWARM_CONFIG
except ImportError:
    SWARM_CONFIG = {
        "enabled": True,
        "adaptive_spawning": {
            "base_agents": 10,
            "min_agents": 8,
            "max_agents": 100,
            "complexity_factors": {
                "us_market": 1.0,
                "hk_market": 1.2,
                "cn_market": 1.5,
                "crypto": 1.8,
            }
        },
        "system_monitoring": {
            "cpu_threshold": 80,
            "memory_threshold": 85,
        }
    }


class AdaptiveSpawner:
    """动态蜂群生成器"""

    def __init__(self):
        """初始化自适应生成器"""
        config = SWARM_CONFIG.get("adaptive_spawning", {})
        self.base_agents = config.get("base_agents", 10)
        self.min_agents = config.get("min_agents", 8)
        self.max_agents = config.get("max_agents", 100)
        self.complexity_factors = config.get("complexity_factors", {
            "us_market": 1.0,
            "hk_market": 1.2,
            "cn_market": 1.5,
            "crypto": 1.8,
        })

        sys_config = SWARM_CONFIG.get("system_monitoring", {})
        self.cpu_threshold = sys_config.get("cpu_threshold", 80)
        self.memory_threshold = sys_config.get("memory_threshold", 85)

        self.log = []

    def get_system_load(self) -> Dict:
        """
        获取当前系统负载

        Returns:
            CPU 和内存使用率字典
        """
        if not HAS_PSUTIL:
            # 降级：返回默认中等负载
            return {
                "cpu_percent": 50.0,
                "memory_percent": 60.0,
                "available": False,
                "reason": "psutil not available"
            }

        try:
            cpu_percent = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "available": True,
            }
        except Exception as e:
            print(f"⚠️ 系统监控失败：{str(e)}")
            return {
                "cpu_percent": 50.0,
                "memory_percent": 60.0,
                "available": False,
                "reason": str(e)
            }

    def calculate_complexity_factor(self, market_type: str) -> float:
        """
        计算市场类型的复杂度因子

        Args:
            market_type: 市场类型（us_market, hk_market, cn_market, crypto）

        Returns:
            复杂度因子（1.0~1.8）
        """
        return self.complexity_factors.get(market_type, 1.0)

    def calculate_ticker_factor(self, ticker_count: int) -> float:
        """
        计算标的数量的因子

        公式：min(ticker_count / 3, 3.0)
        - 3 个标的 = 1.0 倍
        - 6 个标的 = 2.0 倍
        - 9+ 个标的 = 3.0 倍

        Args:
            ticker_count: 标的数量

        Returns:
            标的因子（1.0~3.0）
        """
        return min(ticker_count / 3.0, 3.0)

    def calculate_load_factor(self) -> float:
        """
        计算系统负载因子

        Returns:
            负载因子（0.5~1.0）
        """
        system_load = self.get_system_load()

        cpu = system_load.get("cpu_percent", 50.0)
        memory = system_load.get("memory_percent", 60.0)

        # 如果 CPU > 80% 或内存 > 85%，缩减到 70%
        if cpu > self.cpu_threshold or memory > self.memory_threshold:
            return 0.7
        # 如果 CPU > 60% 或内存 > 70%，缩减到 85%
        elif cpu > 60 or memory > 70:
            return 0.85
        else:
            return 1.0

    def recommend(self, tickers: List[str], market_type: str = "us_market") -> Dict:
        """
        推荐 Agent 生成数量

        公式：
        spawn_count = base × complexity × ticker_factor × load_factor
        spawn_count = clamp(spawn_count, min_agents, max_agents)

        Args:
            tickers: 股票代码列表
            market_type: 市场类型（us_market, hk_market, cn_market, crypto）

        Returns:
            推荐配置字典，包含 spawn_count 和详细的计算过程
        """
        # 规范化标的列表
        tickers = [t.upper().strip() for t in tickers if t and isinstance(t, str)]
        ticker_count = len(tickers)

        if ticker_count == 0:
            return {
                "error": "No valid tickers provided",
                "recommended_agents": self.base_agents,
                "tickers": []
            }

        # 计算各因子
        complexity = self.calculate_complexity_factor(market_type)
        ticker_factor = self.calculate_ticker_factor(ticker_count)
        load_factor = self.calculate_load_factor()
        system_load = self.get_system_load()

        # 计算推荐 Agent 数
        raw_spawn = self.base_agents * complexity * ticker_factor * load_factor
        recommended_agents = max(self.min_agents, min(int(raw_spawn), self.max_agents))

        # 构建返回信息
        result = {
            "recommended_agents": recommended_agents,
            "calculation": {
                "base_agents": self.base_agents,
                "complexity_factor": round(complexity, 2),
                "complexity_factor_reason": f"market_type='{market_type}'",
                "ticker_count": ticker_count,
                "ticker_factor": round(ticker_factor, 2),
                "load_factor": round(load_factor, 2),
                "load_factor_reason": self._explain_load_factor(system_load),
                "raw_calculation": round(raw_spawn, 2),
                "clamped_range": f"[{self.min_agents}, {self.max_agents}]"
            },
            "system_status": system_load,
            "tickers": tickers,
            "market_type": market_type,
            "timestamp": datetime.now().isoformat()
        }

        return result

    def _explain_load_factor(self, system_load: Dict) -> str:
        """解释负载因子"""
        if not system_load.get("available", False):
            return "system monitoring unavailable (降级使用中等负载假设)"

        cpu = system_load.get("cpu_percent", 50.0)
        memory = system_load.get("memory_percent", 60.0)

        if cpu > self.cpu_threshold or memory > self.memory_threshold:
            return f"高负载（CPU {cpu:.1f}% / MEM {memory:.1f}%）→ 缩减 30%"
        elif cpu > 60 or memory > 70:
            return f"中负载（CPU {cpu:.1f}% / MEM {memory:.1f}%）→ 缩减 15%"
        else:
            return f"正常负载（CPU {cpu:.1f}% / MEM {memory:.1f}%）→ 100%"

    def validate_tickers(self, tickers: List[str]) -> Tuple[List[str], List[str]]:
        """
        验证标的代码格式

        Args:
            tickers: 标的列表

        Returns:
            (有效标的列表, 无效标的列表)
        """
        valid = []
        invalid = []

        for ticker in tickers:
            if not isinstance(ticker, str):
                invalid.append(f"{ticker} (not a string)")
                continue

            cleaned = ticker.upper().strip()
            if 1 <= len(cleaned) <= 5 and cleaned.isalpha():
                valid.append(cleaned)
            else:
                invalid.append(f"{cleaned} (invalid format)")

        return valid, invalid

    def print_recommendation(self, tickers: List[str], market_type: str = "us_market"):
        """打印推荐配置"""
        print("\n" + "=" * 70)
        print("🐝 Alpha Hive 动态蜂群生成器")
        print("=" * 70)

        result = self.recommend(tickers, market_type)

        if "error" in result:
            print(f"❌ 错误：{result['error']}")
        else:
            calc = result.get("calculation", {})
            sys_status = result.get("system_status", {})

            print(f"\n📊 推荐 Agent 数：{result['recommended_agents']}")
            print(f"📋 扫描标的数：{result['ticker_count'] if 'ticker_count' in result else len(result.get('tickers', []))}")
            print(f"🌍 市场类型：{market_type}")

            print(f"\n📈 计算过程：")
            print(f"   基础 Agent 数：{calc.get('base_agents', 'N/A')}")
            print(f"   复杂度因子：{calc.get('complexity_factor', 'N/A')} ({calc.get('complexity_factor_reason', '')})")
            ticker_count = len(result.get('tickers', []))
            print(f"   标的因子：{calc.get('ticker_factor', 'N/A')} ({ticker_count} 个标的)")
            print(f"   负载因子：{calc.get('load_factor', 'N/A')}")
            print(f"      └─ {calc.get('load_factor_reason', 'N/A')}")
            print(f"   计算结果：{calc.get('base_agents', 10)} × "
                  f"{calc.get('complexity_factor', 1.0)} × "
                  f"{calc.get('ticker_factor', 1.0)} × "
                  f"{calc.get('load_factor', 1.0)} = "
                  f"{calc.get('raw_calculation', 'N/A')}")
            print(f"   范围限制：[{self.min_agents}, {self.max_agents}] → "
                  f"{result['recommended_agents']} Agents")

            if sys_status.get("available"):
                print(f"\n💻 系统状态：")
                print(f"   CPU：{sys_status.get('cpu_percent', 'N/A'):.1f}%")
                print(f"   内存：{sys_status.get('memory_percent', 'N/A'):.1f}%")
            else:
                print(f"\n💻 系统监控：{sys_status.get('reason', 'unavailable')}")

            print(f"\n📍 扫描标的：{', '.join(result.get('tickers', []))}")

        print("=" * 70 + "\n")

    def export_config(self, tickers: List[str], market_type: str = "us_market") -> Dict:
        """
        导出可用于配置文件的推荐配置

        Args:
            tickers: 标的列表
            market_type: 市场类型

        Returns:
            推荐配置字典
        """
        result = self.recommend(tickers, market_type)

        if "error" not in result:
            return {
                "swarm_config": {
                    "spawn_count": result["recommended_agents"],
                    "tickers": result["tickers"],
                    "market_type": market_type,
                    "calculation_details": result["calculation"],
                    "system_status": result["system_status"],
                    "timestamp": result["timestamp"]
                }
            }
        else:
            return {"error": result["error"]}


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="Alpha Hive 动态蜂群生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：
  # 获取推荐 Agent 数（美国市场）
  python3 adaptive_spawner.py --tickers NVDA TSLA VKTX

  # 指定市场类型（香港市场）
  python3 adaptive_spawner.py --tickers VKTX --market hk_market

  # 加密市场（最高复杂度）
  python3 adaptive_spawner.py --tickers BTC ETH --market crypto

  # 导出为 JSON 配置
  python3 adaptive_spawner.py --tickers NVDA TSLA --export-json config.json
        """
    )

    parser.add_argument('--tickers', nargs='+', required=True, help='股票代码列表')
    parser.add_argument('--market', default='us_market',
                        choices=['us_market', 'hk_market', 'cn_market', 'crypto'],
                        help='市场类型（默认：us_market）')
    parser.add_argument('--export-json', type=str, help='导出配置到 JSON 文件')
    parser.add_argument('--system-status', action='store_true', help='仅显示系统状态')

    args = parser.parse_args()

    spawner = AdaptiveSpawner()

    if args.system_status:
        # 显示系统状态
        status = spawner.get_system_load()
        print(f"📊 系统状态：{json.dumps(status, indent=2)}")
    else:
        # 生成推荐
        spawner.print_recommendation(args.tickers, args.market)

        # 导出 JSON（如指定）
        if args.export_json:
            config = spawner.export_config(args.tickers, args.market)
            with open(args.export_json, "w") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"✅ 配置已导出：{args.export_json}\n")


if __name__ == "__main__":
    main()
