# 🚀 Alpha Hive Phase 2 - 智能进化系统设计

**版本**: 3.0 (Phase 2) | **状态**: 设计中 | **目标完成**: 2026-03-15

---

## 🎯 Phase 2 整体目标

从 **"自动化系统"** 升级为 **"自进化的智能蜂群"**：

✨ 自主感知 + 自我调适 + 自动优化 + 持久学习

---

## 📋 四大进化方向

### 1️⃣ 🔔 智能告警系统 (Alert Intelligence)

#### 目标
实时异常检测 + 多渠道推送通知 + 智能优先级排序

#### 架构

```
编排脚本执行
    ↓
AlertManager (新增)
    ├─ 异常检测引擎
    │   ├─ 性能异常 (执行时间 > 150% 基线)
    │   ├─ 数据异常 (无报告生成)
    │   ├─ 机会异常 (Top 3 均低分)
    │   └─ 部署异常 (GitHub 推送失败)
    │
    ├─ 优先级评分 (P0/P1/P2)
    │   ├─ P0: 系统完全失败
    │   ├─ P1: 关键步骤失败
    │   └─ P2: 性能下降/低分报告
    │
    └─ 多渠道发送
        ├─ Slack Webhook (即时)
        ├─ 邮件 (汇总)
        └─ 仪表板气泡 (可视化)
```

#### 核心逻辑

```python
class AlertManager:
    def analyze_execution(status_json):
        """分析执行结果"""
        alerts = []

        # 检测 P0: 总失败
        if status['status'] == 'failed':
            alerts.append(Alert('CRITICAL', 'Pipeline Failed'))

        # 检测 P1: 步骤失败
        for step, result in status['steps_result'].items():
            if result['status'] == 'failed':
                alerts.append(Alert('HIGH', f'{step} Failed'))

        # 检测 P1: 性能异常
        if status['total_duration_seconds'] > PERF_BASELINE * 1.5:
            alerts.append(Alert('HIGH', 'Slow Execution'))

        # 检测 P2: 低分报告
        report = load_report()
        if max_opportunity_score < 6.0:
            alerts.append(Alert('MEDIUM', 'Low Opportunity Scores'))

        return alerts

    def send_alerts(alerts):
        """多渠道发送"""
        for alert in alerts:
            if alert.priority == 'CRITICAL':
                send_slack(alert)  # 立即
                send_email(alert)   # 立即
            elif alert.priority == 'HIGH':
                queue_slack(alert)  # 汇总后发送
            # P2 仅写入仪表板
```

#### 集成点

- **触发**: orchestrator.sh Step 6 新增
- **输入**: status.json + 当日报告
- **输出**: /logs/alerts-YYYY-MM-DD.json + Slack 消息
- **配置**: /config.py 新增 ALERT_CONFIG

#### 文件清单

```
新建:
  ├─ alert_manager.py (2KB)
  ├─ slack_notifier.py (1KB)
  └─ email_notifier.py (1KB)

修改:
  ├─ alpha-hive-orchestrator.sh (添加 Step 6)
  └─ config.py (添加 ALERT_CONFIG)
```

---

### 2️⃣ 📊 实时性能监控 (Performance Observability)

#### 目标
收集 → 存储 → 可视化 → 趋势预警

#### 架构

```
每次执行
    ↓
MetricsCollector (新增)
    ├─ 执行时间 (Step 1-5 各步)
    ├─ 内存占用 (peak memory)
    ├─ 文件大小 (报告、日志体积)
    ├─ 报告质量 (avg score、稳定性)
    └─ 部署状态 (GitHub 推送成功率)
    ↓
InfluxDB/SQLite (新增)
    ├─ time-series 数据库
    ├─ 保留 90 天历史
    └─ 自动聚合 (daily/weekly/monthly)
    ↓
Grafana 仪表板 (新增)
    ├─ 实时执行时间趋势
    ├─ 报告质量分布
    ├─ 系统健康度评分
    └─ 异常点自动标记
```

#### 核心指标

```json
{
  "timestamp": "2026-02-24T10:17:10Z",
  "execution": {
    "total_duration": 5,
    "step_durations": [1, 2, 1, 0, 1],
    "peak_memory_mb": 128
  },
  "quality": {
    "avg_opportunity_score": 5.1,
    "top_opportunity_score": 5.1,
    "bottom_opportunity_score": 5.0,
    "score_stddev": 0.05
  },
  "deployment": {
    "github_success": true,
    "files_pushed": 18,
    "deploy_duration": 1
  },
  "health": {
    "overall_score": 8.5,
    "system_status": "healthy"
  }
}
```

#### 集成点

- **触发**: orchestrator.sh Step 6 新增
- **存储**: SQLite3 (metrics.db)
- **查询**: 提供 REST API 端点
- **可视化**: HTML 仪表板 + Grafana (可选)

#### 文件清单

```
新建:
  ├─ metrics_collector.py (2.5KB)
  ├─ metrics_db.py (1.5KB)
  ├─ grafana_dashboard.json (配置文件)
  └─ performance_dashboard.html (独立页面)

修改:
  ├─ alpha-hive-orchestrator.sh (添加度量收集)
  └─ index.html (嵌入性能卡片)
```

---

### 3️⃣ 🧠 动态蜂群扩展 (Adaptive Swarming)

#### 目标
根据任务复杂度和负载自动调整 Agent 数量

#### 架构

```
任务输入 (标的数量 + 市场种类)
    ↓
Analyzer (新增)
    ├─ 计算 Complexity Score
    │   ├─ 标的数: 1-20 → spawn base
    │   ├─ 市场数: 1-5 → 倍数
    │   ├─ 催化剂密度: → 调整
    │   └─ 历史难度: → 经验调整
    │
    └─ 确定 Optimal Agent Pool
        ├─ 简单任务 (1-3 标的) → 8 Agent
        ├─ 中等任务 (4-10 标的) → 20 Agent
        ├─ 复杂任务 (11+ 标的) → 50 Agent
        └─ 跨市场套利 → +100% Agent
    ↓
DynamicSpawner (新增)
    ├─ 启动计算出的 Agent 数
    ├─ 负载均衡分配任务
    ├─ 实时监控 CPU/内存
    └─ 过载时动态缩减
```

#### 自适应公式

```python
def calculate_optimal_agents(task_config, system_state, history):
    base_agents = 10  # 基础

    # 根据标的复杂度
    ticker_factor = len(task_config['tickers']) / 3.0  # 归一化到3

    # 根据市场复杂度
    market_complexity = {
        'US': 1.0,
        'HK': 1.2,
        'CN': 1.5,  # A股政策风险多
        'CRYPTO': 1.8
    }
    market_factor = sum(market_complexity[m] for m in task_config['markets'])

    # 根据历史表现
    history_efficiency = history.get('avg_agent_efficiency', 1.0)

    # 根据系统负载
    system_load = system_state['cpu_percent'] / 100.0
    load_factor = max(0.5, 1.0 - system_load)  # 过载时缩减

    optimal_agents = int(
        base_agents * ticker_factor * market_factor * history_efficiency * load_factor
    )

    return max(8, min(100, optimal_agents))  # 8-100 范围
```

#### 集成点

- **触发**: orchestrator.sh 解析参数时
- **输入**: --tickers + 历史数据
- **输出**: AGENT_POOL_SIZE 环境变量
- **目标**: alpha_hive_daily_report.py 使用

#### 文件清单

```
新建:
  ├─ adaptive_spawner.py (2KB)
  ├─ task_analyzer.py (1.5KB)
  └─ system_monitor.py (1KB)

修改:
  ├─ alpha-hive-orchestrator.sh (添加 Analyzer)
  └─ alpha_hive_daily_report.py (使用 AGENT_POOL_SIZE)
```

---

### 4️⃣ 💾 信息素板持久化 (Pheromone Persistence)

#### 目标
长期记忆 + 趋势分析 + 自学习

#### 架构

```
每日执行后
    ↓
PheromoneRecorder (新增)
    ├─ 记录本日高价值信号
    │   ├─ 机会摘要
    │   ├─ 数据来源
    │   ├─ 自评价值 (0-10)
    │   ├─ 支持 Agent 数
    │   ├─ 预测方向
    │   └─ 实际表现 (T+1/T+7/T+30)
    │
    ├─ 存储到数据库
    │   └─ SQLite: pheromone.db
    │       └── signals 表 (历史记录)
    │
    └─ 计算信息素强度衰减
        ├─ 新信号: pheromone = 1.0
        ├─ 每天衰减: -0.1
        ├─ 实现正确时: +0.3 (加强)
        └─ 实现错误时: -0.5 (抑制)
```

#### 数据模式

```sql
CREATE TABLE pheromone_signals (
    id INTEGER PRIMARY KEY,
    date TEXT,
    ticker TEXT,
    direction TEXT,
    opportunity_score REAL,
    confidence REAL,
    expected_3d_return REAL,
    expected_7d_return REAL,
    expected_30d_return REAL,

    -- 实际结果 (T+N 回看填充)
    actual_3d_return REAL,
    actual_7d_return REAL,
    actual_30d_return REAL,
    prediction_accuracy REAL,

    -- 信息素
    pheromone_strength REAL,
    creation_timestamp DATETIME,
    last_update DATETIME,
    sources TEXT,  -- JSON 数组
    agent_supporters INTEGER,

    INDEX idx_ticker_date (ticker, date),
    INDEX idx_accuracy (prediction_accuracy)
);
```

#### 学习反馈循环

```
T+0: 发布信号
  score = 7.5, direction = "看多", expected_7d = +5%

T+7: 回看验证
  actual_7d = -2%  ← 预测失败

学习更新:
  accuracy = -7 / 5 = -140%  ← 大失败
  pheromone -= 0.5  ← 强烈抑制此信号

后续决策:
  同类信号权重 ↓ 30%
  该 Agent 评分 ↓ 2 分

T+30: 长期效应
  月度总结
  → 调整评估模型权重
  → 优化催化剂识别
```

#### 集成点

- **触发**: orchestrator.sh Step 6 新增
- **查询**: update_dashboard.py 展示"信息素排行"
- **学习**: 独立脚本定期(T+1/T+7/T+30)回看
- **存储**: pheromone.db

#### 文件清单

```
新建:
  ├─ pheromone_recorder.py (2.5KB)
  ├─ pheromone_db.py (2KB)
  ├─ accuracy_tracker.py (1.5KB)
  └─ learning_feedback.py (2KB)

修改:
  ├─ alpha-hive-orchestrator.sh (添加 Step 6)
  └─ index.html (添加"信息素排行"卡片)
```

#### 仪表板展示

```
📊 信息素排行榜（过去30天）

排名 | 信号类型 | 准确率 | 强度 | 热度
-----|---------|--------|------|----
#1   | NVDA 看多 | 72%  | 0.8 | 🔥🔥🔥
#2   | TSLA 中性 | 65%  | 0.6 | 🔥🔥
#3   | VKTX 看空 | 58%  | 0.4 | 🔥
```

---

## 🏗️ 实施路线图

### Week 1 (2026-02-24 ~ 03-02)
- [ ] 智能告警系统 (AlertManager)
- [ ] Slack/邮件集成
- [ ] 告警规则引擎

### Week 2 (2026-03-03 ~ 03-09)
- [ ] 性能监控系统 (MetricsCollector)
- [ ] SQLite3 指标数据库
- [ ] 性能仪表板 HTML

### Week 3 (2026-03-10 ~ 03-15)
- [ ] 动态蜂群扩展 (AdaptiveSpawner)
- [ ] 系统负载监控
- [ ] 历史效率学习

### Week 4 (2026-03-16 ~ 03-22)
- [ ] 信息素持久化 (PheromoneRecorder)
- [ ] 准确率回看系统
- [ ] 学习反馈循环

### Week 5 (2026-03-23 ~ 03-31)
- [ ] 集成测试
- [ ] 性能优化
- [ ] 文档完善

---

## 📊 预期收益

### 效率提升
- ⏱️ 平均执行时间 → 减少 20-30%（动态扩展）
- 📈 报告准确率 → 提升 15-25%（学习反馈）

### 可靠性提升
- 🔔 故障发现时间 → 从人工 → 自动（<1分钟）
- 🛡️ 系统可用性 → 从 95% → 99%+（自适应）

### 智能化提升
- 🧠 自学习能力 → 完全激活
- 📚 历史知识积累 → 90 天完整记录
- 🎯 决策精准度 → 持续提升

---

## 🔧 架构变化

### 新增服务

```
Alpha Hive v3.0

orchestrator.sh
  ├─ Step 1-5: [保留]
  ├─ Step 6: 告警分析 (新增)
  ├─ Step 7: 指标收集 (新增)
  ├─ Step 8: 信息素记录 (新增)
  └─ Step 9: 学习反馈 (新增)

数据库
  ├─ pheromone.db (新增)
  │   └── signals 表
  ├─ metrics.db (新增)
  │   └── performance 表
  └─ status.json (保留)

API
  ├─ /api/metrics/latest (新增)
  ├─ /api/pheromone/top (新增)
  └─ /api/alerts/recent (新增)

仪表板
  ├─ index.html (增强)
  │   ├─ 性能卡片
  │   ├─ 信息素排行
  │   └─ 告警面板
  └─ /api/metrics → 图表
```

---

## 📚 依赖关系

```
方向1 (告警) ✅ 独立，可率先实施
    ↓
方向2 (监控) ✅ 依赖告警的数据结构
    ↓
方向3 (动态) ✅ 依赖监控的历史数据
    ↓
方向4 (持久) ✅ 汇总前三者的学习结果
```

**建议**: 顺序实施（Week 1→2→3→4）

---

## 🎯 成功指标

| 指标 | 目标 | 验证方法 |
|-----|------|---------|
| 告警覆盖率 | 100% 故障检测 | 故障注入测试 |
| 平均执行时间 | < 4s (对比 5s) | metrics.db 趋势 |
| 准确率提升 | +15% (vs 基线) | 30 日滚动准确率 |
| 数据库大小 | < 100MB/月 | pheromone.db 统计 |

---

## 🚀 开始实施？

准备好了吗？我可以立即开始：

1. **第一阶段**: 智能告警系统 (AlertManager)
2. **集成测试**: 验证告警准确性
3. **迭代升级**: 逐步添加其他功能

**下一步**: 确认实施优先级和时间表

---

**版本**: 3.0 | **日期**: 2026-02-24 | **作者**: Claude Code
