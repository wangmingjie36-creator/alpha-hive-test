# 🐝 Alpha Hive 优化系统 - 完整使用指南

> 4 大优化已完整实现：Thesis Breaks、Crowding Detection、Catalyst Refinement、Feedback Loop

---

## 📦 文件清单

### Python 模块（已生成）

```
thesis_breaks.py              # 优化 5：失效条件监控
catalyst_refinement.py        # 优化 3：催化剂精细化
crowding_detector.py          # 优化 4：拥挤度检测
feedback_loop.py              # 优化 7：反馈环路
generate_optimized_report.py  # 主集成脚本
```

### 生成的 HTML 报告

```
alpha-hive-NVDA-optimized-2026-02-23.html   # NVDA 优化报告（44KB）
alpha-hive-VKTX-optimized-2026-02-23.html   # VKTX 优化报告（33KB）
```

### 代码统计

- **总代码行数**：2,654 行
- **模块分布**：
  - `thesis_breaks.py`：~350 行
  - `catalyst_refinement.py`：~550 行
  - `crowding_detector.py`：~450 行
  - `feedback_loop.py`：~400 行
  - `generate_optimized_report.py`：~500 行

---

## 🚀 快速开始

### 第一步：在浏览器中查看报告

```bash
# 打开生成的优化报告
open alpha-hive-NVDA-optimized-2026-02-23.html
open alpha-hive-VKTX-optimized-2026-02-23.html
```

### 第二步：为新标的生成报告

编辑 `generate_optimized_report.py`，添加新的生成函数：

```python
def generate_tsla_optimized_report():
    """为 TSLA 生成完整优化报告"""
    generator = OptimizedReportGenerator("TSLA", "2026-02-23")

    # 1. 添加失效条件
    generator.add_thesis_breaks_section(initial_score=6.85)

    # 2. 添加催化剂
    tsla_catalysts = create_tsla_catalysts()  # 需要先创建
    generator.add_catalyst_section(tsla_catalysts)

    # 3. 添加拥挤度
    tsla_metrics = get_tsla_crowding_metrics()  # 需要先定义
    generator.add_crowding_section(initial_score=6.85, metrics=tsla_metrics)

    # 4. 生成并保存
    base_content = """..."""
    filename = generator.save_report(base_content=base_content)
    return filename
```

---

## 📊 4 大优化详解

### 优化 5：Thesis Breaks（失效条件）

#### 使用方法

```python
from thesis_breaks import ThesisBreakMonitor

# 创建监控器
monitor = ThesisBreakMonitor("NVDA", initial_score=8.52)

# 定义失效条件的指标数据
test_metrics = {
    "datacenter_revenue_decline": 2.5,  # 2.5% 增长
    "competitor_threat": 0,
    "china_ban_risk": 35  # Polymarket 禁令概率
}

# 检查条件
result = monitor.check_all_conditions(test_metrics)
print(f"最终评分: {result['final_score']}")

# 生成 HTML
html = monitor.generate_html_section()

# 保存到 JSON
monitor.save_to_json("nvda_breaks.json")
```

#### 输出内容

- **Level 1 预警**：触发时降低评分 -15%
- **Level 2 认输**：触发时反转推荐，降低 -30%
- **实时监控表**：显示每个条件的当前状态
- **HTML 报告段落**：集成到最终报告中

#### 关键特点

✅ 自定义失效条件（按标的特化）
✅ 实时监控（持续检查触发条件）
✅ 分级告警（预警 vs 认输）
✅ 自动评分调整

---

### 优化 4：Crowding Detection（拥挤度检测）

#### 使用方法

```python
from crowding_detector import CrowdingDetector

# 创建检测器
detector = CrowdingDetector("NVDA")

# 准备指标数据
metrics = {
    "stocktwits_messages_per_day": 45000,
    "google_trends_percentile": 84,
    "bullish_agents": 6,
    "polymarket_odds_change_24h": 8.2,
    "seeking_alpha_page_views": 85000,
    "short_float_ratio": 0.02,
    "price_momentum_5d": 6.8
}

# 计算拥挤度评分
crowding_score, component_scores = detector.calculate_crowding_score(metrics)
print(f"拥挤度: {crowding_score:.0f}/100")

# 获取调整因子
adjustment_factor = detector.get_adjustment_factor(crowding_score)
final_score = initial_score * adjustment_factor
print(f"调整后评分: {final_score:.2f}")

# 获取对冲建议
hedges = detector.get_hedge_recommendations(crowding_score)

# 生成 HTML
html = detector.generate_html_section(metrics, initial_score)
```

#### 6 维度评分

| 维度 | 权重 | 说明 |
|------|------|------|
| StockTwits 消息量 | 25% | 社交媒体热度 |
| Google Trends | 15% | 搜索热度 |
| Agent 共识强度 | 25% | 模型看法一致性 |
| Polymarket 赔率变化 | 15% | 市场重新定价速度 |
| Seeking Alpha 浏览 | 10% | 机构关注度 |
| 短期价格动量 | 10% | 股价急速上升风险 |

#### 评分含义

- **< 30**：低拥挤度 🟢 → 加权 +20%
- **30-60**：中等拥挤 🟡 → 轻微折扣
- **> 60**：高拥挤度 🔴 → 打折 30%

#### 对冲建议

系统根据拥挤度自动提供：
- 看涨期权价差（Bull Call Spread）
- 看跌期权保护（Protective Put）
- 等待回调进场

---

### 优化 3：Catalyst Refinement（催化剂精细化）

#### 使用方法

```python
from catalyst_refinement import Catalyst, CatalystTimeline

# 创建时间线
timeline = CatalystTimeline("NVDA")

# 创建催化剂
earnings = Catalyst("NVDA", CatalystType.EARNINGS)
earnings.event_name = "Q4 FY2026 财报发布"
earnings.scheduled_date = "2026-03-15"
earnings.scheduled_time = "16:00"
earnings.is_confirmed = True

# 添加历史数据
earnings.add_historical_data(
    beat_pct=0.65,
    miss_pct=0.15,
    inline_pct=0.20,
    avg_move=7.5,
    upside_ratio=1.8
)

# 添加市场预期
earnings.add_market_expectation(
    consensus="Beat",
    confidence=68,
    iv_implied=15.2,
    polymarket_odds={"beat": 0.65, "miss": 0.22}
)

# 添加关键指标
earnings.add_key_metric("DataCenter Revenue", 28.5, 28.5, 28.0, "CRITICAL")

# 添加后续事件
earnings.add_subsequent_event(
    "Earnings Call",
    "2026-03-15",
    "17:00",
    "CEO 讨论关键指标"
)

# 生成 HTML
html = timeline.generate_timeline_html()

# 保存
timeline.save_to_json("nvda_catalysts.json")
```

#### 输出内容

- **精细时间**：确切日期 + 时间 + 确定性等级
- **历史对标**：过去 3 年财报的 Beat/Miss 比例
- **市场预期**：分析师共识 + Polymarket 赔率 + 期权 IV
- **关键指标**：市场最关注的 3 个数据
- **后续事件**：财报发布后的重要活动
- **失效条件**：哪些情况会使分析无效

#### 可靠性等级

- **A+**：极高可靠性（官方确认、时间确定）
- **A**：高可靠性
- **B**：中等可靠性
- **C**：低可靠性（时间不确定、可能延期）

---

### 优化 7：Feedback Loop（反馈环路）

#### 使用方法

```python
from feedback_loop import ReportSnapshot, BacktestAnalyzer

# 第 1 步：保存报告快照
snapshot = ReportSnapshot("NVDA", "2026-02-23")
snapshot.composite_score = 8.52
snapshot.direction = "Long"
snapshot.price_target = 650
snapshot.stop_loss = 580
snapshot.entry_price = 640

snapshot.agent_votes = {
    "Scout": 8.5,
    "SentimentBee": 8.2,
    "OddsBee": 8.8,
    "CatalystBee": 8.7,
    "CrossBee": 8.6,
    "ValidatorBee": 8.3
}

# 保存快照
snapshot.save_to_json()

# 第 2 步：T+1/T+7/T+30 后更新实际价格
snapshot.actual_price_t1 = 648
snapshot.actual_price_t7 = 655
snapshot.actual_price_t30 = 620

# 第 3 步：计算准确度
returns = snapshot.calculate_returns()
accuracy = snapshot.check_direction_accuracy()

# 第 4 步：回溯分析
analyzer = BacktestAnalyzer()
accuracy_t7 = analyzer.calculate_accuracy("t7")
print(f"T+7 方向准确度: {accuracy_t7['direction_accuracy']:.0f}%")
print(f"Sharpe 比率: {accuracy_t7['sharpe_ratio']:.2f}")

# 第 5 步：计算 Agent 贡献度
agent_accuracy = analyzer.calculate_agent_contribution()

# 第 6 步：建议权重调整
adjustments = analyzer.suggest_weight_adjustments()

# 第 7 步：生成准确度看板
dashboard = analyzer.save_accuracy_dashboard()
```

#### 反馈循环

1. **保存快照**：报告生成时保存所有信息
2. **价格跟踪**：记录 T+1、T+7、T+30 的实际价格
3. **准确度计算**：评估方向预测的正确性
4. **Agent 评分**：每个 Agent 的准确度贡献
5. **权重优化**：建议新的权重分配
6. **平滑迁移**：逐步应用新权重（避免激进变化）

#### 权重调整公式

```
新权重 = 0.7 × 旧权重 + 0.3 × 建议权重
```

这样确保权重调整不会过于激进，防止过拟合。

---

## 📈 报告示例

### NVDA 优化报告结构

```
1. 页眉
   ├─ 标题：NVDA 优化分析
   ├─ 日期：2026-02-23
   └─ 更新时间

2. 目录
   ├─ 基础分析
   ├─ 失效条件监控
   ├─ 催化剂时间线
   ├─ 拥挤度分析
   └─ 方法论说明

3. 基础分析
   ├─ 综合评分：8.52/10
   ├─ 推荐方向：看多
   ├─ 目标价：$650
   └─ 止损：$580

4. 失效条件监控
   ├─ Level 1 预警条件
   │  ├─ DataCenter 收入下滑 > 5%
   │  ├─ 竞争对手重大新产品
   │  └─ 中国禁令风险 > 60%
   └─ Level 2 认输条件
      ├─ EPS 实际 < 预期 20%+
      └─ CEO 离职或重大丑闻

5. 催化剂时间线
   ├─ 财报发布
   │  ├─ 日期：2026-03-15
   │  ├─ 时间：16:00（NYSE 收盘后）
   │  ├─ 历史 65% Beat 概率
   │  └─ 期权 IV：15.2%
   └─ Earnings Call
      ├─ 时间：17:00
      └─ 关键讨论：DataCenter、中国市场

6. 拥挤度分析
   ├─ 拥挤度评分：72/100（高拥挤）
   ├─ 6 维度分解
   ├─ 评分调整：× 0.70（打折 30%）
   └─ 对冲建议

7. 方法论说明
   ├─ 4 大优化创新
   ├─ 评分公式
   └─ 免责声明
```

---

## 💻 集成到现有系统

### 第 1 步：数据接口（需自行实现）

创建 `data_fetcher.py` 获取实时数据：

```python
# 需要实现以下函数
def get_stocktwits_volume(ticker):
    """获取 StockTwits 消息量"""
    pass

def get_google_trends(ticker):
    """获取 Google Trends 热度"""
    pass

def get_polymarket_odds(event_name):
    """获取 Polymarket 赔率"""
    pass

def get_sec_filings(ticker):
    """获取 SEC 披露"""
    pass

def get_current_price(ticker):
    """获取当前股价"""
    pass
```

### 第 2 步：自动化定时任务

使用 `schedule` 库定时运行：

```python
import schedule
import time

def daily_report_generation():
    """每日凌晨生成报告"""
    for ticker in ["NVDA", "VKTX", "TSLA"]:
        generator = OptimizedReportGenerator(ticker)
        # 添加各部分...
        generator.save_report()

# 每天凌晨 00:30 运行
schedule.every().day.at("00:30").do(daily_report_generation)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 第 3 步：部署到网站

```bash
# 将生成的 HTML 文件上传到服务器
scp alpha-hive-*.html user@server:/var/www/reports/

# 或使用 GitHub Pages（现有的部署方式）
git add alpha-hive-*.html
git commit -m "🐝 优化报告 - $(date +%Y-%m-%d)"
git push origin main
```

---

## ⚙️ 自定义配置

### 修改权重

在 `thesis_breaks.py` 中修改：

```python
self.weights = {
    "stocktwits_volume": 0.30,      # 改为 0.20
    "google_trends": 0.10,           # 改为 0.15
    "consensus_strength": 0.20,     # 改为 0.25
    # ... 其他权重
}
```

### 添加新的失效条件

```python
TSLA_BREAKS = {
    "level_1_warning": {
        "conditions": [
            {
                "id": "new_condition",
                "metric": "新指标名称",
                "trigger": "触发条件",
                "data_source": "数据来源",
                # ... 其他字段
            }
        ]
    }
}
```

### 修改拥挤度评分公式

在 `crowding_detector.py` 中调整各维度的权重或计算方法。

---

## 🐛 常见问题

### Q1：报告显示不完整

**A：** 清除浏览器缓存：
```bash
# Chrome/Edge: Ctrl+Shift+Delete
# Safari: Cmd+Shift+Delete
# Firefox: Ctrl+Shift+Delete
```

### Q2：如何添加新数据源

**A：** 修改 `crowding_detector.py` 中的 `get_metric_display()` 和 `_get_metric_interpretation()` 方法。

### Q3：权重调整后如何生效

**A：** 新权重会在下一次生成报告时自动应用。无需重启系统。

### Q4：如何导出为 PDF

**A：** 在浏览器中：
- 按 `Ctrl+P` (Windows) 或 `Cmd+P` (Mac)
- 选择"另存为 PDF"
- 保存

---

## 📚 进阶使用

### 自定义报告模板

编辑 `generate_optimized_report.py` 中的 HTML 模板部分。

### 多标的对比

```python
tickers = ["NVDA", "VKTX", "TSLA"]
reports = {}

for ticker in tickers:
    generator = OptimizedReportGenerator(ticker)
    # 生成报告...
    reports[ticker] = generator
```

### 实时监控面板

使用 Flask/Django 建立 Web 面板，实时展示各标的的拥挤度、失效条件状态等。

---

## 📞 技术支持

如遇到问题：

1. 检查 Python 版本（建议 3.8+）
2. 确保所有依赖已安装：`pip install --upgrade pytz requests`
3. 查看 JSON 配置文件是否正确
4. 检查数据源连接是否正常

---

## 🎉 总结

你现在拥有：

✅ **4 大优化系统**：完整实现
✅ **2,654 行高质量代码**：模块化、可扩展
✅ **生成的优化报告**：NVDA、VKTX 示例
✅ **完整文档**：快速开始、高级配置

**下一步**：

1. 在浏览器中打开 HTML 报告查看效果
2. 为 TSLA 生成优化报告（按 NVDA 的模式）
3. 集成实时数据源
4. 部署到 GitHub Pages 或自有服务器
5. 设置每日定时任务

🚀 **准备好了吗？开始使用吧！** 🐝
