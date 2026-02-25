#!/usr/bin/env python3
"""
💾 Alpha Hive 信息素持久化系统 (Week 4)
历史信号存储 + T+1/T+7/T+30 预测准确率追踪与回看
"""

import json
import sqlite3
import argparse
import sys
import os
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# 尝试导入 yfinance，用于获取实际收益率
try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False
    print("⚠️ yfinance 未安装，准确率追踪功能将降级")

# 导入配置
sys.path.insert(0, str(Path(__file__).parent))
try:
    from config import PHEROMONE_CONFIG
except ImportError:
    PHEROMONE_CONFIG = {
        "enabled": True,
        "db_path": "/Users/igg/.claude/reports/pheromone.db",
        "retention_days": 30,
        "decay_rate": 0.1,
        "accuracy_tracking": {
            "enable_t1_tracking": True,
            "enable_t7_tracking": True,
            "enable_t30_tracking": True,
        }
    }


@dataclass
class PheromoneSignal:
    """信息素信号数据类"""
    signal_id: str
    date: str
    ticker: str
    direction: str  # "看多", "看空", "中性"
    opp_score: float  # 0-10
    signal_score: float  # 0-10
    pheromone_strength: float  # 0.0-1.0
    source: str  # 数据来源
    notes: str  # 备注信息
    actual_t1: Optional[float] = None  # T+1 实际收益率
    actual_t7: Optional[float] = None  # T+7 实际收益率
    actual_t30: Optional[float] = None  # T+30 实际收益率


class PheromoneRecorder:
    """信息素信号记录器"""

    def __init__(self, db_path: str = None):
        """
        初始化信息素记录器

        Args:
            db_path: SQLite 数据库路径
        """
        self.db_path = db_path or PHEROMONE_CONFIG["db_path"]
        self.retention_days = PHEROMONE_CONFIG.get("retention_days", 30)
        self.decay_rate = PHEROMONE_CONFIG.get("decay_rate", 0.1)
        self.accuracy_tracking = PHEROMONE_CONFIG.get("accuracy_tracking", {})
        self._init_db()

    def _init_db(self):
        """初始化数据库和表"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 创建 signals 表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    signal_id TEXT UNIQUE,
                    date TEXT,
                    ticker TEXT,
                    direction TEXT,
                    opp_score REAL,
                    signal_score REAL,
                    pheromone_strength REAL,
                    source TEXT,
                    notes TEXT,
                    actual_t1 REAL,
                    actual_t7 REAL,
                    actual_t30 REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 创建索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON signals(date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_ticker ON signals(ticker)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_direction ON signals(direction)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_strength ON signals(pheromone_strength)")

            # 创建 accuracy_logs 表（用于日志记录）
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accuracy_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    period TEXT,
                    total_signals INTEGER,
                    correct_signals INTEGER,
                    accuracy_percent REAL,
                    avg_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            conn.close()
            print(f"✅ 信息素数据库已初始化：{self.db_path}")
        except Exception as e:
            print(f"⚠️ 数据库初始化失败：{str(e)}")
            traceback.print_exc()

    def record(self, report_dir: str = None) -> Tuple[int, List[str]]:
        """
        从最新报告中记录信号

        Args:
            report_dir: 报告目录路径

        Returns:
            (记录数, 信号ID列表)
        """
        report_dir = report_dir or Path(__file__).parent
        today = datetime.now().strftime("%Y-%m-%d")

        # 寻找最新的报告 JSON 文件
        report_files = list(Path(report_dir).glob(f"alpha-hive-daily-{today}*.json"))

        if not report_files:
            print(f"⚠️ 未找到今日报告文件：{report_dir}/alpha-hive-daily-{today}*.json")
            return 0, []

        report_file = report_files[-1]  # 最新的文件
        print(f"📂 处理报告文件：{report_file.name}")

        try:
            with open(report_file, "r", encoding="utf-8") as f:
                report_data = json.load(f)

            opportunities = report_data.get("opportunities", [])
            recorded_signals = []

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            for opp in opportunities:
                ticker = opp.get("ticker", "")
                direction = opp.get("direction", "中性")
                opp_score = opp.get("opp_score", 0.0)

                # 生成 signal_id
                signal_id = f"{today}_{ticker}_{direction[:2]}"

                # 计算 pheromone_strength（基于 opp_score）
                pheromone_strength = min(opp_score / 10.0, 1.0)

                signal = PheromoneSignal(
                    signal_id=signal_id,
                    date=today,
                    ticker=ticker,
                    direction=direction,
                    opp_score=opp_score,
                    signal_score=opp.get("signal_score", 5.0) if isinstance(opp, dict) else 5.0,
                    pheromone_strength=pheromone_strength,
                    source="alpha_hive_daily_report",
                    notes=f"关键催化剂: {opp.get('key_catalyst', 'N/A')}"
                )

                # 插入数据库
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO signals (
                            signal_id, date, ticker, direction, opp_score, signal_score,
                            pheromone_strength, source, notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        signal.signal_id,
                        signal.date,
                        signal.ticker,
                        signal.direction,
                        signal.opp_score,
                        signal.signal_score,
                        signal.pheromone_strength,
                        signal.source,
                        signal.notes
                    ))
                    recorded_signals.append(signal.signal_id)
                except Exception as e:
                    print(f"⚠️ 记录失败 {signal.signal_id}：{str(e)}")

            conn.commit()
            conn.close()

            if recorded_signals:
                print(f"✅ 已记录 {len(recorded_signals)} 条信号：{', '.join(recorded_signals[:3])}...")

            return len(recorded_signals), recorded_signals

        except Exception as e:
            print(f"❌ 处理报告失败：{str(e)}")
            traceback.print_exc()
            return 0, []

    def decay_signals(self) -> int:
        """
        对历史信号执行衰减（每日执行）

        Returns:
            衰减的信号数
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 查询所有信号
            cursor.execute("SELECT id, signal_id, pheromone_strength FROM signals")
            rows = cursor.fetchall()

            decayed_count = 0
            for row_id, signal_id, current_strength in rows:
                new_strength = max(0.0, current_strength - self.decay_rate)

                if new_strength < 0.2:
                    # 衰减为 0，标记为已归档
                    cursor.execute(
                        "UPDATE signals SET pheromone_strength = 0.0 WHERE id = ?",
                        (row_id,)
                    )
                    decayed_count += 1
                else:
                    cursor.execute(
                        "UPDATE signals SET pheromone_strength = ? WHERE id = ?",
                        (new_strength, row_id)
                    )
                    decayed_count += 1

            conn.commit()
            conn.close()

            print(f"✅ 衰减完成：{decayed_count} 条信号（衰减率 {self.decay_rate}）")
            return decayed_count

        except Exception as e:
            print(f"⚠️ 衰减失败：{str(e)}")
            return 0

    def update_accuracy(self, days: int = 30) -> Dict:
        """
        回看历史信号的实际收益率，更新准确率

        Args:
            days: 回溯天数

        Returns:
            准确率统计字典
        """
        if not HAS_YFINANCE:
            print("⚠️ yfinance 未安装，无法获取实际收益率")
            return {}

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            # 查询所有待验证的信号
            cursor.execute("""
                SELECT id, signal_id, date, ticker, direction
                FROM signals
                WHERE date >= ? AND (actual_t1 IS NULL OR actual_t7 IS NULL OR actual_t30 IS NULL)
            """, (cutoff_date,))

            rows = cursor.fetchall()
            updated_count = 0

            for row_id, signal_id, signal_date, ticker, direction in rows:
                try:
                    # 获取信号日期和三个验证日期
                    signal_datetime = datetime.strptime(signal_date, "%Y-%m-%d")
                    t1_date = signal_datetime + timedelta(days=1)
                    t7_date = signal_datetime + timedelta(days=7)
                    t30_date = signal_datetime + timedelta(days=30)

                    # 获取股票数据
                    data = yf.download(ticker, start=signal_date, end=t30_date + timedelta(days=1),
                                      progress=False, warn_on_error=False)

                    if data.empty or len(data) < 2:
                        continue

                    signal_price = data.iloc[0]["Close"]

                    # 计算实际收益率
                    actual_t1 = None
                    actual_t7 = None
                    actual_t30 = None

                    # T+1 收益率
                    if len(data) > 1:
                        t1_price = data.iloc[1]["Close"]
                        actual_t1 = ((t1_price - signal_price) / signal_price) * 100

                    # T+7 收益率
                    t7_data = data[data.index <= t7_date]
                    if len(t7_data) > 1:
                        t7_price = t7_data.iloc[-1]["Close"]
                        actual_t7 = ((t7_price - signal_price) / signal_price) * 100

                    # T+30 收益率
                    t30_data = data[data.index <= t30_date]
                    if len(t30_data) > 1:
                        t30_price = t30_data.iloc[-1]["Close"]
                        actual_t30 = ((t30_price - signal_price) / signal_price) * 100

                    # 更新数据库
                    cursor.execute("""
                        UPDATE signals
                        SET actual_t1 = ?, actual_t7 = ?, actual_t30 = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (actual_t1, actual_t7, actual_t30, row_id))

                    updated_count += 1

                except Exception as e:
                    print(f"⚠️ 更新 {signal_id} 失败：{str(e)}")
                    continue

            conn.commit()
            conn.close()

            print(f"✅ 准确率更新完成：{updated_count} 条信号")
            return self.get_accuracy_report(days)

        except Exception as e:
            print(f"❌ 准确率更新失败：{str(e)}")
            traceback.print_exc()
            return {}

    def get_accuracy_report(self, days: int = 30) -> Dict:
        """
        生成准确率报告

        Args:
            days: 回溯天数

        Returns:
            准确率报告字典
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            # T+1 准确率
            cursor.execute("""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN
                        (direction = '看多' AND actual_t1 > 0) OR
                        (direction = '看空' AND actual_t1 < 0)
                        THEN 1 ELSE 0 END) as correct,
                    AVG(opp_score) as avg_score,
                    AVG(actual_t1) as avg_return
                FROM signals
                WHERE date >= ? AND actual_t1 IS NOT NULL
            """, (cutoff_date,))

            t1_row = cursor.fetchone()
            t1_accuracy = {
                "total_signals": t1_row[0] if t1_row[0] else 0,
                "correct_predictions": t1_row[1] if t1_row[1] else 0,
                "accuracy_percent": (t1_row[1] / t1_row[0] * 100) if t1_row[0] else 0,
                "avg_score": round(t1_row[2], 1) if t1_row[2] else 0,
                "avg_return_percent": round(t1_row[3], 2) if t1_row[3] else 0,
            }

            # T+7 准确率
            cursor.execute("""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN
                        (direction = '看多' AND actual_t7 > 0) OR
                        (direction = '看空' AND actual_t7 < 0)
                        THEN 1 ELSE 0 END) as correct,
                    AVG(opp_score) as avg_score,
                    AVG(actual_t7) as avg_return
                FROM signals
                WHERE date >= ? AND actual_t7 IS NOT NULL
            """, (cutoff_date,))

            t7_row = cursor.fetchone()
            t7_accuracy = {
                "total_signals": t7_row[0] if t7_row[0] else 0,
                "correct_predictions": t7_row[1] if t7_row[1] else 0,
                "accuracy_percent": (t7_row[1] / t7_row[0] * 100) if t7_row[0] else 0,
                "avg_score": round(t7_row[2], 1) if t7_row[2] else 0,
                "avg_return_percent": round(t7_row[3], 2) if t7_row[3] else 0,
            }

            # T+30 准确率
            cursor.execute("""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN
                        (direction = '看多' AND actual_t30 > 0) OR
                        (direction = '看空' AND actual_t30 < 0)
                        THEN 1 ELSE 0 END) as correct,
                    AVG(opp_score) as avg_score,
                    AVG(actual_t30) as avg_return
                FROM signals
                WHERE date >= ? AND actual_t30 IS NOT NULL
            """, (cutoff_date,))

            t30_row = cursor.fetchone()
            t30_accuracy = {
                "total_signals": t30_row[0] if t30_row[0] else 0,
                "correct_predictions": t30_row[1] if t30_row[1] else 0,
                "accuracy_percent": (t30_row[1] / t30_row[0] * 100) if t30_row[0] else 0,
                "avg_score": round(t30_row[2], 1) if t30_row[2] else 0,
                "avg_return_percent": round(t30_row[3], 2) if t30_row[3] else 0,
            }

            # 获取最强信号
            cursor.execute("""
                SELECT date, ticker, direction, opp_score, pheromone_strength
                FROM signals
                WHERE date >= ?
                ORDER BY opp_score DESC
                LIMIT 5
            """, (cutoff_date,))

            top_signals = []
            for row in cursor.fetchall():
                top_signals.append({
                    "date": row[0],
                    "ticker": row[1],
                    "direction": row[2],
                    "opp_score": round(row[3], 1),
                    "pheromone_strength": round(row[4], 2)
                })

            conn.close()

            return {
                "report_date": datetime.now().strftime("%Y-%m-%d"),
                "period_days": days,
                "accuracy_t1": t1_accuracy,
                "accuracy_t7": t7_accuracy,
                "accuracy_t30": t30_accuracy,
                "top_signals": top_signals
            }

        except Exception as e:
            print(f"⚠️ 准确率报告失败：{str(e)}")
            return {}

    def get_top_signals(self, limit: int = 10, min_strength: float = 0.5) -> List[Dict]:
        """
        获取当前最强信号

        Args:
            limit: 返回的信号数量上限
            min_strength: 最小信息素强度

        Returns:
            信号列表
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT date, ticker, direction, opp_score, pheromone_strength, notes
                FROM signals
                WHERE pheromone_strength >= ?
                ORDER BY pheromone_strength DESC, opp_score DESC
                LIMIT ?
            """, (min_strength, limit))

            signals = []
            for row in cursor.fetchall():
                signals.append({
                    "date": row[0],
                    "ticker": row[1],
                    "direction": row[2],
                    "opp_score": round(row[3], 1),
                    "pheromone_strength": round(row[4], 2),
                    "notes": row[5]
                })

            conn.close()
            return signals

        except Exception as e:
            print(f"⚠️ 查询信号失败：{str(e)}")
            return []

    def print_accuracy_report(self, days: int = 30):
        """打印准确率报告"""
        report = self.get_accuracy_report(days)

        print("\n" + "=" * 70)
        print(f"📊 Alpha Hive 周度准确率报告 ({days} 天)")
        print("=" * 70)

        if not report:
            print("❌ 报告生成失败")
            return

        print(f"\n📈 T+1 准确率：{report['accuracy_t1']['accuracy_percent']:.1f}% "
              f"({report['accuracy_t1']['correct_predictions']}/{report['accuracy_t1']['total_signals']})")
        print(f"   平均分：{report['accuracy_t1']['avg_score']}/10 | "
              f"平均收益：{report['accuracy_t1']['avg_return_percent']:.2f}%")

        print(f"\n📊 T+7 准确率：{report['accuracy_t7']['accuracy_percent']:.1f}% "
              f"({report['accuracy_t7']['correct_predictions']}/{report['accuracy_t7']['total_signals']})")
        print(f"   平均分：{report['accuracy_t7']['avg_score']}/10 | "
              f"平均收益：{report['accuracy_t7']['avg_return_percent']:.2f}%")

        print(f"\n📅 T+30 准确率：{report['accuracy_t30']['accuracy_percent']:.1f}% "
              f"({report['accuracy_t30']['correct_predictions']}/{report['accuracy_t30']['total_signals']})")
        print(f"   平均分：{report['accuracy_t30']['avg_score']}/10 | "
              f"平均收益：{report['accuracy_t30']['avg_return_percent']:.2f}%")

        if report.get("top_signals"):
            print(f"\n🌟 最强信号（Top 5）：")
            for sig in report["top_signals"][:5]:
                print(f"   {sig['date']} | {sig['ticker']} {sig['direction']} | "
                      f"分数 {sig['opp_score']}/10 | 强度 {sig['pheromone_strength']}")

        print("=" * 70 + "\n")

    def cleanup(self, retention_days: int = None) -> int:
        """
        清理旧数据，仅保留指定天数内的记录

        Args:
            retention_days: 保留天数

        Returns:
            删除的记录数
        """
        retention_days = retention_days or self.retention_days

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cutoff_date = (datetime.now() - timedelta(days=retention_days)).strftime("%Y-%m-%d")

            cursor.execute("DELETE FROM signals WHERE date < ? AND pheromone_strength < 0.2", (cutoff_date,))
            deleted_count = cursor.rowcount

            conn.commit()
            conn.close()

            if deleted_count > 0:
                print(f"✅ 清理完成：删除了 {deleted_count} 条旧信号（>{retention_days}天且强度 < 0.2）")
            else:
                print(f"✅ 无需清理（所有有效信号都在保留期内）")

            return deleted_count

        except Exception as e:
            print(f"⚠️ 清理失败：{str(e)}")
            return 0


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="Alpha Hive 信息素持久化系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：
  # 从今日报告中记录信号
  python3 pheromone_recorder.py --record --report-dir /Users/igg/.claude/reports

  # 执行信号衰减（每日运行）
  python3 pheromone_recorder.py --decay

  # 更新准确率（T+1/T+7/T+30）
  python3 pheromone_recorder.py --update-accuracy --days 30

  # 查看准确率报告
  python3 pheromone_recorder.py --accuracy-report --days 30

  # 显示最强信号
  python3 pheromone_recorder.py --top-signals --limit 10

  # 清理旧信号
  python3 pheromone_recorder.py --cleanup --retention-days 30
        """
    )

    parser.add_argument('--record', action='store_true', help='从报告中记录信号')
    parser.add_argument('--report-dir', type=str, help='报告目录路径')
    parser.add_argument('--decay', action='store_true', help='执行信号衰减')
    parser.add_argument('--update-accuracy', action='store_true', help='更新准确率')
    parser.add_argument('--accuracy-report', action='store_true', help='显示准确率报告')
    parser.add_argument('--top-signals', action='store_true', help='显示最强信号')
    parser.add_argument('--cleanup', action='store_true', help='清理旧数据')
    parser.add_argument('--days', type=int, default=30, help='回溯天数或保留天数')
    parser.add_argument('--retention-days', type=int, default=30, help='数据保留天数')
    parser.add_argument('--limit', type=int, default=10, help='返回的信号数量')

    args = parser.parse_args()

    recorder = PheromoneRecorder()

    if args.record:
        report_dir = args.report_dir or "/Users/igg/.claude/reports"
        count, signals = recorder.record(report_dir)
        print(f"\n✅ 记录完成：{count} 条信号")

    elif args.decay:
        recorder.decay_signals()

    elif args.update_accuracy:
        recorder.update_accuracy(args.days)

    elif args.accuracy_report:
        recorder.print_accuracy_report(args.days)

    elif args.top_signals:
        signals = recorder.get_top_signals(args.limit)
        print("\n🌟 Alpha Hive 最强信号（按强度降序）")
        print("=" * 70)
        for sig in signals:
            print(f"  {sig['date']} | {sig['ticker']} {sig['direction']} | "
                  f"分数 {sig['opp_score']}/10 | 强度 {sig['pheromone_strength']}")
        print("=" * 70 + "\n")

    elif args.cleanup:
        recorder.cleanup(args.retention_days)

    else:
        # 默认显示准确率报告
        recorder.print_accuracy_report(30)


if __name__ == "__main__":
    main()
