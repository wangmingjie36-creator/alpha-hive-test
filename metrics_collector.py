#!/usr/bin/env python3
"""
📊 Alpha Hive 性能监控系统 (Week 2)
记录每次运行的性能指标到 SQLite 时序数据库
"""

import json
import sqlite3
import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import traceback

# 导入配置
sys.path.insert(0, str(Path(__file__).parent))
try:
    from config import METRICS_CONFIG
except ImportError:
    METRICS_CONFIG = {
        "enabled": True,
        "db_path": "/Users/igg/.claude/reports/metrics.db",
        "retention_days": 90,
    }


class MetricsCollector:
    """性能指标收集器"""

    def __init__(self, db_path: str = None):
        """
        初始化指标收集器

        Args:
            db_path: SQLite 数据库路径
        """
        self.db_path = db_path or METRICS_CONFIG["db_path"]
        self.retention_days = METRICS_CONFIG.get("retention_days", 90)
        self._init_db()

    def _init_db(self):
        """初始化数据库和表"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 创建 run_metrics 表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS run_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT UNIQUE,
                    date TEXT,
                    timestamp TEXT,
                    tickers TEXT,
                    status TEXT,
                    total_duration_seconds REAL,
                    step1_duration REAL,
                    step2_duration REAL,
                    step3_duration REAL,
                    step4_duration REAL,
                    step5_duration REAL,
                    step6_duration REAL,
                    step7_duration REAL,
                    step1_status TEXT,
                    step2_status TEXT,
                    step3_status TEXT,
                    step4_status TEXT,
                    step5_status TEXT,
                    step6_status TEXT,
                    step7_status TEXT,
                    report_quality_score REAL,
                    agent_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 创建索引以加快查询
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON run_metrics(date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON run_metrics(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON run_metrics(status)")

            conn.commit()
            conn.close()
            print(f"✅ 数据库已初始化：{self.db_path}")
        except Exception as e:
            print(f"⚠️ 数据库初始化失败：{str(e)}")
            traceback.print_exc()

    def record(self, status_json_path: str, agent_count: int = 10, report_quality_score: float = 7.0) -> bool:
        """
        记录一次运行的性能指标

        Args:
            status_json_path: status.json 文件路径
            agent_count: 本次运行的 Agent 数量
            report_quality_score: 报告质量评分（0-10）

        Returns:
            是否成功记录
        """
        try:
            # 读取 status.json
            if not os.path.exists(status_json_path):
                print(f"⚠️ 状态文件不存在：{status_json_path}")
                return False

            with open(status_json_path, "r") as f:
                status_data = json.load(f)

            # 解析数据
            last_run_date = status_data.get("last_run_date", datetime.now().strftime("%Y-%m-%d"))
            last_run = status_data.get("last_run", datetime.now().isoformat())
            overall_status = status_data.get("status", "unknown")
            total_duration = status_data.get("total_duration_seconds", 0)
            steps_result = status_data.get("steps_result", {})
            tickers = status_data.get("tickers", [])

            # 生成 run_id
            run_id = f"{last_run_date}_{int(datetime.fromisoformat(last_run.replace('Z', '+00:00')).timestamp())}"

            # 提取各步骤的耗时和状态
            step_durations = {}
            step_statuses = {}
            for i in range(1, 8):
                step_key = f"step{i}_"
                step_data = {}
                for k, v in steps_result.items():
                    if k.startswith(step_key):
                        step_data = v
                        break

                step_durations[f"step{i}_duration"] = step_data.get("duration_seconds", 0.0)
                step_statuses[f"step{i}_status"] = step_data.get("status", "unknown")

            # 插入到数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO run_metrics (
                    run_id, date, timestamp, tickers, status, total_duration_seconds,
                    step1_duration, step2_duration, step3_duration, step4_duration,
                    step5_duration, step6_duration, step7_duration,
                    step1_status, step2_status, step3_status, step4_status,
                    step5_status, step6_status, step7_status,
                    report_quality_score, agent_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                run_id,
                last_run_date,
                last_run,
                json.dumps(tickers),
                overall_status,
                total_duration,
                step_durations.get("step1_duration", 0),
                step_durations.get("step2_duration", 0),
                step_durations.get("step3_duration", 0),
                step_durations.get("step4_duration", 0),
                step_durations.get("step5_duration", 0),
                step_durations.get("step6_duration", 0),
                step_durations.get("step7_duration", 0),
                step_statuses.get("step1_status", "unknown"),
                step_statuses.get("step2_status", "unknown"),
                step_statuses.get("step3_status", "unknown"),
                step_statuses.get("step4_status", "unknown"),
                step_statuses.get("step5_status", "unknown"),
                step_statuses.get("step6_status", "unknown"),
                step_statuses.get("step7_status", "unknown"),
                report_quality_score,
                agent_count,
            ))

            conn.commit()
            conn.close()

            print(f"✅ 性能指标已记录：{run_id}")
            print(f"   耗时：{total_duration}s | 状态：{overall_status} | Agents：{agent_count} | 报告分：{report_quality_score}")
            return True

        except Exception as e:
            print(f"❌ 记录失败：{str(e)}")
            traceback.print_exc()
            return False

    def get_trend(self, days: int = 7) -> List[Dict]:
        """
        获取近 N 天的趋势数据

        Args:
            days: 回溯天数

        Returns:
            趋势数据列表
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            cursor.execute("""
                SELECT date, AVG(total_duration_seconds) as avg_duration,
                       AVG(report_quality_score) as avg_quality,
                       COUNT(*) as run_count,
                       SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count
                FROM run_metrics
                WHERE date >= ?
                GROUP BY date
                ORDER BY date DESC
            """, (start_date,))

            rows = cursor.fetchall()
            conn.close()

            trend = []
            for row in rows:
                trend.append({
                    "date": row[0],
                    "avg_duration_seconds": round(row[1], 2),
                    "avg_quality_score": round(row[2], 1),
                    "total_runs": row[3],
                    "successful_runs": row[4],
                    "success_rate": f"{(row[4] / row[3] * 100):.1f}%"
                })

            return trend

        except Exception as e:
            print(f"⚠️ 趋势查询失败：{str(e)}")
            return []

    def get_summary(self, days: int = 7) -> Dict:
        """
        获取 N 天内的汇总统计

        Args:
            days: 回溯天数

        Returns:
            汇总统计数据
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            cursor.execute("""
                SELECT
                    COUNT(*) as total_runs,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_runs,
                    AVG(total_duration_seconds) as avg_duration,
                    MAX(total_duration_seconds) as max_duration,
                    MIN(total_duration_seconds) as min_duration,
                    AVG(report_quality_score) as avg_quality,
                    AVG(agent_count) as avg_agent_count
                FROM run_metrics
                WHERE date >= ?
            """, (start_date,))

            row = cursor.fetchone()
            conn.close()

            if row and row[0] > 0:
                return {
                    "period_days": days,
                    "total_runs": row[0],
                    "successful_runs": row[1],
                    "success_rate": f"{(row[1] / row[0] * 100):.1f}%",
                    "avg_duration_seconds": round(row[2], 2),
                    "max_duration_seconds": round(row[3], 2) if row[3] else 0,
                    "min_duration_seconds": round(row[4], 2) if row[4] else 0,
                    "avg_quality_score": round(row[5], 1),
                    "avg_agent_count": round(row[6], 0)
                }
            else:
                return {
                    "period_days": days,
                    "total_runs": 0,
                    "message": "No data available"
                }

        except Exception as e:
            print(f"⚠️ 汇总查询失败：{str(e)}")
            return {"error": str(e)}

    def cleanup(self, retention_days: int = None) -> int:
        """
        清理旧数据，仅保留指定天数内的记录

        Args:
            retention_days: 保留天数（默认使用配置值）

        Returns:
            删除的记录数
        """
        retention_days = retention_days or self.retention_days

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cutoff_date = (datetime.now() - timedelta(days=retention_days)).strftime("%Y-%m-%d")

            cursor.execute("DELETE FROM run_metrics WHERE date < ?", (cutoff_date,))
            deleted_count = cursor.rowcount

            conn.commit()
            conn.close()

            if deleted_count > 0:
                print(f"✅ 清理完成：删除了 {deleted_count} 条旧记录（>{retention_days}天）")
            else:
                print(f"✅ 无需清理（所有记录都在 {retention_days} 天内）")

            return deleted_count

        except Exception as e:
            print(f"⚠️ 清理失败：{str(e)}")
            return 0

    def print_summary(self, days: int = 7):
        """打印汇总信息"""
        summary = self.get_summary(days)
        print("\n" + "=" * 70)
        print(f"📊 性能指标统计（最近 {days} 天）")
        print("=" * 70)
        for key, value in summary.items():
            print(f"  {key}: {value}")
        print("=" * 70 + "\n")


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="Alpha Hive 性能监控系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：
  # 记录本次运行的性能指标
  python3 metrics_collector.py --record --status-json /path/to/status.json

  # 查看近 7 天的趋势
  python3 metrics_collector.py --trend --days 7

  # 查看近 30 天的汇总统计
  python3 metrics_collector.py --summary --days 30

  # 清理超过 90 天的数据
  python3 metrics_collector.py --cleanup --retention-days 90
        """
    )

    parser.add_argument('--record', action='store_true', help='记录一次运行的性能指标')
    parser.add_argument('--status-json', type=str, help='status.json 文件路径')
    parser.add_argument('--agent-count', type=int, default=10, help='本次 Agent 数量')
    parser.add_argument('--quality-score', type=float, default=7.0, help='报告质量分（0-10）')

    parser.add_argument('--trend', action='store_true', help='显示性能趋势')
    parser.add_argument('--summary', action='store_true', help='显示汇总统计')
    parser.add_argument('--cleanup', action='store_true', help='清理旧数据')
    parser.add_argument('--days', type=int, default=7, help='回溯天数或保留天数')
    parser.add_argument('--retention-days', type=int, default=90, help='数据保留天数')

    args = parser.parse_args()

    collector = MetricsCollector()

    # 执行操作
    if args.record:
        if not args.status_json:
            print("❌ --record 需要指定 --status-json")
            sys.exit(1)
        collector.record(args.status_json, args.agent_count, args.quality_score)

    elif args.trend:
        trend = collector.get_trend(args.days)
        print("\n📈 性能趋势（最近 {} 天）".format(args.days))
        print("=" * 70)
        for item in trend:
            print(f"  📅 {item['date']}: 平均耗时 {item['avg_duration_seconds']}s | "
                  f"质量分 {item['avg_quality_score']}/10 | "
                  f"成功率 {item['success_rate']} ({item['successful_runs']}/{item['total_runs']})")
        print("=" * 70 + "\n")

    elif args.summary:
        collector.print_summary(args.days)

    elif args.cleanup:
        collector.cleanup(args.retention_days)

    else:
        # 默认显示汇总
        collector.print_summary(7)


if __name__ == "__main__":
    main()
