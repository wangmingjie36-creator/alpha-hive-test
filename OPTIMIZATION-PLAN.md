# 🐝 Alpha Hive 优化实现计划

> 优化 3, 4, 5, 7 - 完整执行指南

---

## 📋 目录

1. [优化 5：Thesis Breaks（失效条件）](#优化-5-thesis-breaks)
2. [优化 4：Crowding Detection（拥挤度检测）](#优化-4-crowding-detection)
3. [优化 7：Feedback Loop（反馈环路）](#优化-7-feedback-loop)
4. [优化 3：Catalyst Refinement（催化剂精细化）](#优化-3-catalyst-refinement)

---

## 优化 5: Thesis Breaks

### 🎯 **目标**
在每份报告中明确列出"如果发生 X，我们的推荐失效"的条件。

### 📐 **实现方案**

#### 第一步：定义通用 Thesis Break 模板

```json
{
  "thesis_breaks": {
    "level_1_warning": {
      "name": "预警级别",
      "threshold_reduction": -0.15,
      "conditions": [
        {
          "metric": "revenue_guidance",
          "trigger": "下调超过 3%",
          "data_source": "公司公告",
          "check_frequency": "实时"
        },
        {
          "metric": "insider_selling",
          "trigger": "单周 > $100M",
          "data_source": "SEC Form 4",
          "check_frequency": "每日"
        },
        {
          "metric": "market_share",
          "trigger": "季度环比下降 > 2%",
          "data_source": "竞争对标报告",
          "check_frequency": "季度"
        }
      ]
    },
    "level_2_stop_loss": {
      "name": "认输级别",
      "recommendation_reverse": true,
      "conditions": [
        {
          "metric": "earnings_miss",
          "trigger": "EPS 实际 < 预期 20%+",
          "data_source": "财报披露",
          "check_frequency": "季度"
        },
        {
          "metric": "regulatory_shock",
          "trigger": "重大监管禁令或处罚",
          "data_source": "SEC/监管机构公告",
          "check_frequency": "实时"
        },
        {
          "metric": "supply_chain_break",
          "trigger": "关键供应商破产或退出",
          "data_source": "新闻/业界公告",
          "check_frequency": "实时"
        }
      ]
    }
  }
}
```

#### 第二步：行业/标的特化 Break 条件

**NVDA（芯片制造）:**
```python
nvda_breaks = {
    "level_1": [
        "TSMC 产能利用率下降 > 10%",
        "AMD 或 Intel 发布重大新产品",
        "中国芯片禁令风险上升（Polymarket 概率 > 60%）",
        "Data Center 收入环比下降"
    ],
    "level_2": [
        "CEO Jensen Huang 离职",
        "美国芯片出口禁令直接影响 NVIDIA",
        "财报 Data Center 收入 < 预期 25%+",
        "竞争对手市占率超过 NVIDIA"
    ]
}

vktx_breaks = {  # Viking Therapeutics (生物制药)
    "level_1": [
        "临床试验关键患者脱落 > 15%",
        "竞争对手发布更优越的数据",
        "管理层人事变更"
    ],
    "level_2": [
        "FDA 临床试验暂停（IND hold）",
        "财报现金储备 < 12 个月支出",
        "Phase 3 试验失败"
    ]
}

tsla_breaks = {  # Tesla (汽车)
    "level_1": [
        "季度交付量同比下降 > 5%",
        "Gross Margin 环比下降 > 200bps",
        "新竞争对手获得重大订单"
    ],
    "level_2": [
        "Elon Musk 卸任或重大丑闻",
        "关键工厂停产 > 1 周",
        "财报收入 < 预期 15%+"
    ]
}
```

#### 第三步：实时监控系统

```python
# Python 实现（集成到 ValidatorBee）

class ThesisBreakMonitor:
    def __init__(self, ticker, breaks_config):
        self.ticker = ticker
        self.breaks = breaks_config
        self.alert_history = []

    def check_level_1_warnings(self):
        """检查预警条件"""
        warnings = []

        for condition in self.breaks["level_1"]["conditions"]:
            metric = condition["metric"]
            trigger_value = self.get_metric(metric)

            if self.evaluate_trigger(trigger_value, condition["trigger"]):
                warnings.append({
                    "level": "WARNING",
                    "metric": metric,
                    "condition": condition["trigger"],
                    "current_value": trigger_value,
                    "timestamp": datetime.now(),
                    "action": "降低评分 -15%"
                })

        return warnings

    def check_level_2_stop_loss(self):
        """检查认输条件"""
        stop_losses = []

        for condition in self.breaks["level_2"]["conditions"]:
            metric = condition["metric"]
            trigger_value = self.get_metric(metric)

            if self.evaluate_trigger(trigger_value, condition["trigger"]):
                stop_losses.append({
                    "level": "STOP_LOSS",
                    "metric": metric,
                    "condition": condition["trigger"],
                    "current_value": trigger_value,
                    "timestamp": datetime.now(),
                    "action": "反转推荐，转向对冲"
                })

        return stop_losses

    def get_metric(self, metric_name):
        """从各数据源获取指标"""
        if metric_name == "revenue_guidance":
            return self.fetch_from_sec_filings()
        elif metric_name == "insider_selling":
            return self.fetch_from_form_4()
        elif metric_name == "earnings_miss":
            return self.fetch_latest_earnings()
        # 更多指标...

    def evaluate_trigger(self, current_value, trigger_condition):
        """评估是否触发条件"""
        # 解析 trigger_condition（如 "< -3%"）并与 current_value 比较
        if "<" in trigger_condition and self.parse_number(trigger_condition) > current_value:
            return True
        # 更多逻辑...
        return False

    def continuous_monitor(self, check_interval_minutes=60):
        """持续监控，每小时检查一次"""
        while True:
            warnings = self.check_level_1_warnings()
            stops = self.check_level_2_stop_loss()

            if warnings or stops:
                self.send_alert(warnings, stops)
                self.alert_history.append({
                    "timestamp": datetime.now(),
                    "warnings": warnings,
                    "stops": stops
                })

            time.sleep(check_interval_minutes * 60)

# 使用示例
nvda_monitor = ThesisBreakMonitor("NVDA", nvda_breaks)
nvda_monitor.continuous_monitor()
```

#### 第四步：HTML 报告集成

```html
<!-- 在 alpha-hive-nvda-2026-02-23.html 中新增 -->

<section id="thesis-breaks" class="report-section">
  <h2>🚨 失效条件监控 (Thesis Breaks)</h2>

  <!-- 预警级别 -->
  <div class="thesis-break-container">
    <h3 class="level-1">⚠️ Level 1: 预警条件（降低评分 -15%）</h3>

    <div class="break-condition">
      <div class="break-metric">
        <strong>数据中心收入增速下滑</strong>
      </div>
      <div class="break-details">
        <p><span class="label">触发条件：</span>季度环比下降 > 5%</p>
        <p><span class="label">数据来源：</span>季度财报</p>
        <p><span class="label">当前状态：</span>✅ 正常（+8% QoQ）</p>
        <p><span class="label">监控频率：</span>每季度</p>
      </div>
    </div>

    <div class="break-condition">
      <div class="break-metric">
        <strong>竞争对手产品发布</strong>
      </div>
      <div class="break-details">
        <p><span class="label">触发条件：</span>AMD 或 Intel 发布超越 NVIDIA 的产品</p>
        <p><span class="label">数据来源：</span>产品发布公告、技术评测</p>
        <p><span class="label">当前状态：</span>✅ 无重大威胁</p>
        <p><span class="label">监控频率：</span>实时</p>
      </div>
    </div>

    <div class="break-condition">
      <div class="break-metric">
        <strong>中国芯片禁令风险</strong>
      </div>
      <div class="break-details">
        <p><span class="label">触发条件：</span>Polymarket 禁令概率 > 60%</p>
        <p><span class="label">数据来源：</span>Polymarket、政策监测</p>
        <p><span class="label">当前状态：</span>⚠️ 中等风险（概率 35%）</p>
        <p><span class="label">监控频率：</span>实时</p>
      </div>
    </div>
  </div>

  <!-- 认输级别 -->
  <div class="thesis-break-container">
    <h3 class="level-2">🛑 Level 2: 认输条件（反转推荐）</h3>

    <div class="break-condition">
      <div class="break-metric">
        <strong>财报 EPS 大幅低于预期</strong>
      </div>
      <div class="break-details">
        <p><span class="label">触发条件：</span>实际 EPS < 预期 20%+</p>
        <p><span class="label">数据来源：</span>财报披露</p>
        <p><span class="label">当前状态：</span>✅ 未发生</p>
        <p><span class="label">监控频率：</span>季度</p>
        <p><span class="label">后续行动：</span>立即转向空头头寸或对冲</p>
      </div>
    </div>

    <div class="break-condition">
      <div class="break-metric">
        <strong>美国芯片出口禁令</strong>
      </div>
      <div class="break-details">
        <p><span class="label">触发条件：</span>直接禁止对华 H100/H800 等产品销售</p>
        <p><span class="label">数据来源：</span>白宫/商务部公告</p>
        <p><span class="label">当前状态：</span>⚠️ 监管风险中等</p>
        <p><span class="label">监控频率：</span>实时</p>
        <p><span class="label">财务影响：</span>假设中国市场 20% 收入，禁令影响 4% 总收入</p>
      </div>
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
          <th>最后更新</th>
        </tr>
      </thead>
      <tbody>
        <tr class="status-ok">
          <td>DataCenter 增速</td>
          <td>&lt; -5% QoQ</td>
          <td>+8.2% QoQ</td>
          <td>✅ 安全</td>
          <td>2026-02-23 10:30</td>
        </tr>
        <tr class="status-warning">
          <td>中国禁令风险</td>
          <td>&gt; 60% Polymarket</td>
          <td>35% Polymarket</td>
          <td>⚠️ 监视</td>
          <td>2026-02-23 14:45</td>
        </tr>
        <tr class="status-ok">
          <td>CEO 稳定性</td>
          <td>离职传言</td>
          <td>无异常</td>
          <td>✅ 安全</td>
          <td>2026-02-23 09:00</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<style>
  #thesis-breaks {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin: 30px 0;
  }

  .level-1 {
    color: #ff9800;
    border-left: 4px solid #ff9800;
    padding-left: 10px;
  }

  .level-2 {
    color: #f44336;
    border-left: 4px solid #f44336;
    padding-left: 10px;
  }

  .break-condition {
    background: white;
    padding: 15px;
    margin: 10px 0;
    border-radius: 4px;
    border-left: 3px solid #e0e0e0;
  }

  .break-metric {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 10px;
  }

  .break-details p {
    margin: 5px 0;
    font-size: 14px;
  }

  .label {
    color: #666;
    font-weight: 600;
  }

  .status-ok {
    background: #e8f5e9;
  }

  .status-warning {
    background: #fff3e0;
  }

  .monitoring-table {
    width: 100%;
    border-collapse: collapse;
  }

  .monitoring-table th {
    background: #f5f5f5;
    padding: 10px;
    text-align: left;
    font-weight: 600;
  }

  .monitoring-table td {
    padding: 10px;
    border-bottom: 1px solid #eee;
  }
</style>
```

---

## 优化 4: Crowding Detection

### 🎯 **目标**
检测市场拥挤度，识别过度定价的想法，提供对冲建议。

### 📐 **实现方案**

#### 第一步：拥挤度评分算法

```python
class CrowdingDetector:
    """拥挤度评估系统"""

    def __init__(self, ticker):
        self.ticker = ticker
        self.weights = {
            "stocktwits_volume": 0.25,
            "google_trends": 0.15,
            "consensus_strength": 0.25,
            "polymarket_volatility": 0.15,
            "seeking_alpha_page_views": 0.10,
            "short_squeeze_risk": 0.10
        }

    def calculate_crowding_score(self):
        """计算 0-100 的拥挤度评分"""

        # 获取各项指标
        stocktwits_score = self._get_stocktwits_volume_score()
        google_score = self._get_google_trends_score()
        consensus_score = self._get_consensus_strength_score()
        polymarket_score = self._get_polymarket_volatility_score()
        seeking_alpha_score = self._get_seeking_alpha_score()
        squeeze_score = self._get_short_squeeze_score()

        # 加权合成
        crowding_score = (
            self.weights["stocktwits_volume"] * stocktwits_score +
            self.weights["google_trends"] * google_score +
            self.weights["consensus_strength"] * consensus_score +
            self.weights["polymarket_volatility"] * polymarket_score +
            self.weights["seeking_alpha_page_views"] * seeking_alpha_score +
            self.weights["short_squeeze_risk"] * squeeze_score
        )

        return min(100, max(0, crowding_score))

    def _get_stocktwits_volume_score(self):
        """
        StockTwits 消息量评分
        0-10,000/天 = 0-30 分
        10,000-50,000/天 = 30-70 分
        50,000+/天 = 70-100 分
        """
        messages_per_day = self.fetch_stocktwits_volume()

        if messages_per_day < 10000:
            return (messages_per_day / 10000) * 30
        elif messages_per_day < 50000:
            return 30 + ((messages_per_day - 10000) / 40000) * 40
        else:
            return 70 + min(30, (messages_per_day - 50000) / 10000)

    def _get_google_trends_score(self):
        """
        Google Trends 热度评分（0-100）
        当前排名百分位数 = 评分
        """
        trend_percentile = self.fetch_google_trends_percentile()
        return trend_percentile

    def _get_consensus_strength_score(self):
        """
        共识强度评分
        6/6 Agent 一致（100%） = 100 分（极度拥挤）
        4/6 Agent （67%） = 60 分
        3/6 Agent （50%） = 30 分（低拥挤）
        """
        bullish_count = self.count_bullish_agents()
        consensus_percentage = (bullish_count / 6) * 100
        return consensus_percentage

    def _get_polymarket_volatility_score(self):
        """
        Polymarket 赔率变化速度
        赔率快速变化（24h 变化 > 10%） = 高拥挤
        赔率缓慢变化（变化 < 2%） = 低拥挤
        """
        odds_change_24h = self.fetch_polymarket_odds_change()

        if odds_change_24h > 10:
            return 80
        elif odds_change_24h > 5:
            return 60
        elif odds_change_24h > 2:
            return 40
        else:
            return 20

    def _get_seeking_alpha_score(self):
        """
        Seeking Alpha 页面访问热度
        高流量 = 众所周知 = 高拥挤
        """
        page_views = self.fetch_seeking_alpha_page_views()

        if page_views > 100000:
            return 80
        elif page_views > 50000:
            return 60
        elif page_views > 10000:
            return 40
        else:
            return 20

    def _get_short_squeeze_score(self):
        """
        短期内股价急速上升 + 高做空比例
        = 可能已被过度定价（挤压风险已兑现）
        """
        short_ratio = self.fetch_short_float_ratio()
        price_momentum = self.fetch_price_momentum_5d()

        if short_ratio > 0.3 and price_momentum > 15:
            return 90  # 已过度上涨
        elif short_ratio > 0.2 or price_momentum > 20:
            return 70
        else:
            return 30

    def get_crowding_category(self):
        """根据评分返回拥挤度分类"""
        score = self.calculate_crowding_score()

        if score < 30:
            return "低拥挤度", "green"
        elif score < 60:
            return "中等拥挤度", "yellow"
        else:
            return "高拥挤度", "red"

    def get_adjustment_factor(self):
        """基于拥挤度调整综合评分"""
        score = self.calculate_crowding_score()

        # 拥挤度越高，评分折扣越大
        if score < 30:
            return 1.0  # 无折扣，甚至加权 +0.2
        elif score < 60:
            return 0.95  # 轻微折扣
        else:
            return 0.70  # 重大折扣（30% 打折）

# 使用示例
crowding = CrowdingDetector("NVDA")
crowding_score = crowding.calculate_crowding_score()
category, color = crowding.get_crowding_category()
adjustment = crowding.get_adjustment_factor()

print(f"NVDA 拥挤度: {crowding_score:.1f}/100")
print(f"分类: {category}")
print(f"评分调整因子: {adjustment}")
```

#### 第二步：HTML 报告集成

```html
<!-- 在报告顶部新增 Crowding Analysis 卡片 -->

<section id="crowding-analysis" class="analysis-card">
  <div class="card-header">
    <h2>🗣️ 市场热度 & 拥挤度分析</h2>
    <div class="crowding-badge red">⚠️ 高拥挤度</div>
  </div>

  <div class="card-body">
    <!-- 拥挤度仪表板 -->
    <div class="crowding-dashboard">
      <div class="crowding-meter">
        <div class="meter-label">拥挤度评分</div>
        <div class="meter-bar">
          <div class="meter-fill" style="width: 72%"></div>
          <span class="meter-value">72/100</span>
        </div>
        <p class="meter-interpretation">
          ⚠️ <strong>高拥挤度</strong><br>
          该想法已被广泛发现和定价。预期上升空间有限，下跌风险较高。
        </p>
      </div>

      <!-- 拥挤度指标分解 -->
      <div class="crowding-breakdown">
        <h3>拥挤度指标分解</h3>

        <div class="indicator">
          <div class="indicator-label">
            <span>StockTwits 48h 消息量</span>
            <span class="weight">(权重 25%)</span>
          </div>
          <div class="indicator-bar">
            <div class="indicator-fill" style="width: 85%"></div>
          </div>
          <div class="indicator-value">
            <strong>45,000 条/天</strong>
            <span class="interpretation">极度拥挤 (历史 95 百分位)</span>
          </div>
        </div>

        <div class="indicator">
          <div class="indicator-label">
            <span>Google Trends 热度</span>
            <span class="weight">(权重 15%)</span>
          </div>
          <div class="indicator-bar">
            <div class="indicator-fill" style="width: 84%"></div>
          </div>
          <div class="indicator-value">
            <strong>84 百分位</strong>
            <span class="interpretation">极高搜索量</span>
          </div>
        </div>

        <div class="indicator">
          <div class="indicator-label">
            <span>6 个 Agent 共识强度</span>
            <span class="weight">(权重 25%)</span>
          </div>
          <div class="indicator-bar">
            <div class="indicator-fill" style="width: 100%"></div>
          </div>
          <div class="indicator-value">
            <strong>6/6 看多 (100%)</strong>
            <span class="interpretation">完全一致 = 极度拥挤风险</span>
          </div>
        </div>

        <div class="indicator">
          <div class="indicator-label">
            <span>Polymarket 赔率变化速度</span>
            <span class="weight">(权重 15%)</span>
          </div>
          <div class="indicator-bar">
            <div class="indicator-fill" style="width: 65%"></div>
          </div>
          <div class="indicator-value">
            <strong>24h 变化 8.2%</strong>
            <span class="interpretation">快速重新定价</span>
          </div>
        </div>

        <div class="indicator">
          <div class="indicator-label">
            <span>Seeking Alpha 页面浏览</span>
            <span class="weight">(权重 10%)</span>
          </div>
          <div class="indicator-bar">
            <div class="indicator-fill" style="width: 78%"></div>
          </div>
          <div class="indicator-value">
            <strong>85,000 次/周</strong>
            <span class="interpretation">高曝光度</span>
          </div>
        </div>

        <div class="indicator">
          <div class="indicator-label">
            <span>短期价格动量</span>
            <span class="weight">(权重 10%)</span>
          </div>
          <div class="indicator-bar">
            <div class="indicator-fill" style="width: 42%"></div>
          </div>
          <div class="indicator-value">
            <strong>+6.8% (5天)</strong>
            <span class="interpretation">温和上升（未过度）</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 拥挤度影响分析 -->
    <div class="crowding-impact">
      <h3>📊 拥挤度对评分的影响</h3>

      <table class="impact-table">
        <tr>
          <td><strong>基础综合评分</strong></td>
          <td>8.52/10</td>
        </tr>
        <tr>
          <td><strong>拥挤度折扣因子</strong></td>
          <td>0.70x (高拥挤 30% 打折)</td>
        </tr>
        <tr class="highlight">
          <td><strong>调整后评分</strong></td>
          <td>5.96/10 ⬇️</td>
        </tr>
      </table>

      <p class="impact-interpretation">
        虽然 NVDA 在基本面和情绪上都看好，但由于高度拥挤，
        上升空间有限。相对收益风险比不如 VKTX（拥挤度 32/100）。
      </p>
    </div>

    <!-- 对冲建议 -->
    <div class="hedge-recommendations">
      <h3>🛡️ 推荐对冲策略</h3>

      <div class="hedge-option">
        <h4>选项 A：看涨期权价差（牛市价差）</h4>
        <p>
          <strong>策略：</strong> 买入 $650 看涨期权，卖出 $680 看涨期权<br>
          <strong>风险：</strong> 有限上升空间（$650-$680）<br>
          <strong>收益：</strong> 期权费抵消下跌风险<br>
          <strong>适合：</strong> 看好但希望降低风险
        </p>
      </div>

      <div class="hedge-option">
        <h4>选项 B：看跌期权保护</h4>
        <p>
          <strong>策略：</strong> 买入 $600 看跌期权（保护性看跌）<br>
          <strong>风险：</strong> 期权费成本 3-4%<br>
          <strong>收益：</strong> $600 以下完全保护<br>
          <strong>适合：</strong> 已持有长仓，寻求下行保护
        </p>
      </div>

      <div class="hedge-option">
        <h4>选项 C：等待回调</h4>
        <p>
          <strong>策略：</strong> 等待 NVDA 下跌 5-8% 后再建仓<br>
          <strong>理由：</strong> 拥挤度过高，可能短期调整<br>
          <strong>风险：</strong> 错过继续上升<br>
          <strong>适合：</strong> 耐心的长期投资者
        </p>
      </div>
    </div>

    <!-- 对比分析 -->
    <div class="crowding-comparison">
      <h3>📈 本周监控标的拥挤度对比</h3>

      <table class="comparison-table">
        <thead>
          <tr>
            <th>标的</th>
            <th>拥挤度</th>
            <th>调整评分</th>
            <th>推荐程度</th>
          </tr>
        </thead>
        <tbody>
          <tr class="high-crowding">
            <td>NVDA</td>
            <td>72/100 🔴</td>
            <td>5.96/10</td>
            <td>⚖️ 中性</td>
          </tr>
          <tr class="medium-crowding">
            <td>TSLA</td>
            <td>48/100 🟡</td>
            <td>6.48/10</td>
            <td>🟡 观察</td>
          </tr>
          <tr class="low-crowding">
            <td>VKTX</td>
            <td>32/100 🟢</td>
            <td>7.34/10</td>
            <td>🟢 看好</td>
          </tr>
        </tbody>
      </table>

      <p class="insight">
        💡 <strong>洞察：</strong> VKTX 虽然评分 7.15，但由于拥挤度低，
        调整后成为本周最值得关注的标的。低拥挤度意味着更大的非共识空间和上升潜力。
      </p>
    </div>
  </div>
</section>

<style>
  #crowding-analysis {
    background: linear-gradient(135deg, #fff5e6 0%, #ffe6e6 100%);
    border: 2px solid #ff9800;
    border-radius: 12px;
    padding: 20px;
    margin: 30px 0;
  }

  .crowding-badge {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 14px;
  }

  .crowding-badge.red {
    background: #ffebee;
    color: #c62828;
  }

  .crowding-meter {
    background: white;
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
  }

  .meter-label {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 10px;
  }

  .meter-bar {
    position: relative;
    background: #e0e0e0;
    height: 30px;
    border-radius: 15px;
    overflow: hidden;
    margin: 10px 0;
  }

  .meter-fill {
    background: linear-gradient(90deg, #ff9800 0%, #f44336 100%);
    height: 100%;
    border-radius: 15px;
    transition: width 0.3s ease;
  }

  .meter-value {
    position: absolute;
    top: 50%;
    right: 10px;
    transform: translateY(-50%);
    color: white;
    font-weight: 600;
    font-size: 14px;
  }

  .meter-interpretation {
    margin-top: 10px;
    color: #d32f2f;
    font-size: 14px;
  }

  .indicator {
    background: white;
    padding: 12px;
    margin: 10px 0;
    border-radius: 6px;
    border-left: 3px solid #ff9800;
  }

  .indicator-label {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 8px;
  }

  .weight {
    color: #999;
    font-weight: normal;
  }

  .indicator-bar {
    background: #f0f0f0;
    height: 20px;
    border-radius: 10px;
    overflow: hidden;
    margin: 8px 0;
  }

  .indicator-fill {
    background: linear-gradient(90deg, #ff9800, #f44336);
    height: 100%;
    border-radius: 10px;
  }

  .indicator-value {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
  }

  .interpretation {
    color: #999;
  }

  .impact-table {
    width: 100%;
    margin: 15px 0;
    border-collapse: collapse;
    background: white;
    border-radius: 6px;
    overflow: hidden;
  }

  .impact-table td {
    padding: 12px;
    border-bottom: 1px solid #eee;
  }

  .impact-table .highlight {
    background: #fff3e0;
    font-weight: 600;
  }

  .hedge-recommendations {
    background: white;
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
  }

  .hedge-option {
    padding: 12px;
    margin: 10px 0;
    border-left: 3px solid #2196f3;
    background: #e3f2fd;
    border-radius: 4px;
  }

  .comparison-table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
  }

  .comparison-table th {
    background: #ff9800;
    color: white;
    padding: 12px;
    text-align: left;
    font-weight: 600;
  }

  .comparison-table td {
    padding: 12px;
    border-bottom: 1px solid #eee;
  }

  .high-crowding {
    background: #ffebee;
  }

  .medium-crowding {
    background: #fff3e0;
  }

  .low-crowding {
    background: #e8f5e9;
  }
</style>
```

---

## 优化 7: Feedback Loop

### 🎯 **目标**
建立"预测准确度看板"，T+1/T+7/T+30 回溯，自动优化权重。

### 📐 **实现方案**

#### 第一步：报告存储架构

```python
# 每份报告生成时保存完整信息

class ReportSnapshot:
    def __init__(self, ticker, date):
        self.ticker = ticker
        self.date = date
        self.report_id = f"{ticker}_{date}"

        # 输出数据
        self.composite_score = None
        self.direction = None  # "Long", "Short", "Neutral"
        self.price_target = None
        self.stop_loss = None
        self.agent_votes = {}  # {"Scout": 8.2, "SentimentBee": 7.5, ...}

        # 数据来源权重（当时使用的）
        self.weights_used = {
            "signal": 0.30,
            "catalyst": 0.20,
            "sentiment": 0.20,
            "odds": 0.15,
            "risk_adj": 0.15
        }

        # 保存文件
        self.save_to_json()

    def save_to_json(self):
        """保存快照到文件"""
        filename = f"reports/{self.report_id}.json"
        with open(filename, 'w') as f:
            json.dump({
                "ticker": self.ticker,
                "date": self.date,
                "composite_score": self.composite_score,
                "direction": self.direction,
                "price_target": self.price_target,
                "stop_loss": self.stop_loss,
                "agent_votes": self.agent_votes,
                "weights_used": self.weights_used
            }, f)

# 使用示例
nvda_report = ReportSnapshot("NVDA", "2026-02-23")
nvda_report.composite_score = 8.52
nvda_report.direction = "Long"
nvda_report.price_target = 650
nvda_report.agent_votes = {
    "Scout": 8.5,
    "SentimentBee": 8.2,
    "OddsBee": 8.8,
    "CatalystBee": 8.7,
    "CrossBee": 8.6,
    "ValidatorBee": 8.3
}
```

#### 第二步：实际价格跟踪

```python
class PriceTucker:
    """跟踪历史价格并计算回溯准确度"""

    def __init__(self, ticker):
        self.ticker = ticker
        self.price_history = {}  # {date: price}

    def get_accuracy_metrics(self, report_date):
        """计算 T+1, T+7, T+30 准确度"""

        # 读取历史报告
        report = self.load_report_snapshot(report_date)

        # 获取价格
        entry_price = self.price_history[report_date]
        price_t1 = self.price_history.get(self.add_days(report_date, 1))
        price_t7 = self.price_history.get(self.add_days(report_date, 7))
        price_t30 = self.price_history.get(self.add_days(report_date, 30))

        # 计算准确度指标
        metrics = {
            "t0": {
                "price": entry_price,
                "direction_correct": None
            },
            "t1": {
                "price": price_t1,
                "days_passed": 1,
                "return_pct": ((price_t1 - entry_price) / entry_price) * 100 if price_t1 else None,
                "direction_match": self._check_direction_match(report.direction, price_t1, entry_price),
                "within_target": price_t1 <= report.price_target,
                "hit_stop_loss": price_t1 <= report.stop_loss
            },
            "t7": {
                "price": price_t7,
                "days_passed": 7,
                "return_pct": ((price_t7 - entry_price) / entry_price) * 100 if price_t7 else None,
                "direction_match": self._check_direction_match(report.direction, price_t7, entry_price),
                "within_target": price_t7 <= report.price_target,
                "hit_stop_loss": price_t7 <= report.stop_loss
            },
            "t30": {
                "price": price_t30,
                "days_passed": 30,
                "return_pct": ((price_t30 - entry_price) / entry_price) * 100 if price_t30 else None,
                "direction_match": self._check_direction_match(report.direction, price_t30, entry_price),
                "within_target": price_t30 <= report.price_target,
                "hit_stop_loss": price_t30 <= report.stop_loss
            }
        }

        return metrics

    def _check_direction_match(self, predicted_direction, price_end, price_start):
        """检查方向是否正确"""
        actual_direction = "Up" if price_end > price_start else "Down"
        return predicted_direction.lower() in actual_direction.lower()

    def calculate_aggregate_accuracy(self, days_back=90):
        """计算过去 N 天的综合准确度"""

        all_metrics = []
        for report_date in self.get_reports_from_last_n_days(days_back):
            metrics = self.get_accuracy_metrics(report_date)
            all_metrics.append(metrics)

        # 聚合指标
        accuracy = {
            "direction_accuracy_t1": self._calculate_accuracy_rate(all_metrics, "t1"),
            "direction_accuracy_t7": self._calculate_accuracy_rate(all_metrics, "t7"),
            "direction_accuracy_t30": self._calculate_accuracy_rate(all_metrics, "t30"),
            "avg_return_t1": self._calculate_avg_return(all_metrics, "t1"),
            "avg_return_t7": self._calculate_avg_return(all_metrics, "t7"),
            "avg_return_t30": self._calculate_avg_return(all_metrics, "t30"),
            "price_forecast_mape": self._calculate_mape(all_metrics),
            "sharpe_ratio": self._calculate_sharpe_ratio(all_metrics),
            "win_rate": self._calculate_win_rate(all_metrics)
        }

        return accuracy

    def _calculate_accuracy_rate(self, all_metrics, timeframe):
        """计算某时间段的准确度（正确方向比例）"""
        correct = sum(1 for m in all_metrics if m[timeframe]["direction_match"])
        total = len(all_metrics)
        return (correct / total * 100) if total > 0 else 0

    def _calculate_avg_return(self, all_metrics, timeframe):
        """计算平均收益"""
        returns = [m[timeframe]["return_pct"] for m in all_metrics if m[timeframe]["return_pct"]]
        return sum(returns) / len(returns) if returns else 0

    def _calculate_mape(self, all_metrics):
        """计算价格预测 MAPE（平均绝对百分比误差）"""
        # 实现价格目标 vs 实际价格的误差计算
        pass

    def _calculate_sharpe_ratio(self, all_metrics):
        """计算 Sharpe 比率（风险调整收益）"""
        pass

    def _calculate_win_rate(self, all_metrics):
        """计算胜率（达到目标价 vs 触发止损）"""
        wins = sum(1 for m in all_metrics if m["t30"]["within_target"] and not m["t30"]["hit_stop_loss"])
        total = len(all_metrics)
        return (wins / total * 100) if total > 0 else 0
```

#### 第三步：权重自适应优化

```python
class WeightOptimizer:
    """自动优化 Agent 权重基于回溯表现"""

    def __init__(self):
        self.current_weights = {
            "signal": 0.30,
            "catalyst": 0.20,
            "sentiment": 0.20,
            "odds": 0.15,
            "risk_adj": 0.15
        }

    def calculate_agent_contribution(self, timeframe="t7"):
        """计算每个 Agent 对准确度的贡献"""

        all_reports = self.load_all_report_snapshots()
        agent_accuracies = {
            "Scout": [],
            "SentimentBee": [],
            "OddsBee": [],
            "CatalystBee": [],
            "CrossBee": [],
            "ValidatorBee": []
        }

        for report in all_reports:
            # 获取每个 Agent 的评分
            for agent_name, agent_score in report.agent_votes.items():
                # 与实际结果对比
                actual_return = report.actual_return[timeframe]
                accuracy = self._score_prediction_accuracy(agent_score, actual_return)
                agent_accuracies[agent_name].append(accuracy)

        # 计算平均准确度
        agent_avg_accuracy = {
            agent: sum(scores) / len(scores) if scores else 0
            for agent, scores in agent_accuracies.items()
        }

        return agent_avg_accuracy

    def suggest_weight_adjustments(self):
        """基于 Agent 表现建议权重调整"""

        agent_accuracy = self.calculate_agent_contribution()

        # 标准化为 0-1
        total_accuracy = sum(agent_accuracy.values())
        normalized_accuracy = {
            agent: score / total_accuracy
            for agent, score in agent_accuracy.items()
        }

        # 计算新权重（基于贡献度）
        new_weights = {}
        weight_categories = {
            "signal": ["Scout"],
            "sentiment": ["SentimentBee"],
            "odds": ["OddsBee"],
            "catalyst": ["CatalystBee"],
            "signal": ["CrossBee"],  # CrossBee 也提升 signal 权重
            "risk_adj": ["ValidatorBee"]
        }

        for category, agents in weight_categories.items():
            category_accuracy = sum(normalized_accuracy[agent] for agent in agents)
            new_weights[category] = min(0.35, max(0.10, category_accuracy))

        # 归一化使总和 = 1
        total = sum(new_weights.values())
        new_weights = {k: v / total for k, v in new_weights.items()}

        return new_weights, self._compare_weights(self.current_weights, new_weights)

    def _compare_weights(self, old, new):
        """对比旧权重和新权重"""
        comparison = {}
        for key in old:
            change = (new[key] - old[key]) * 100
            comparison[key] = {
                "old": old[key],
                "new": new[key],
                "change_percentage": change,
                "direction": "↑" if change > 0 else "↓"
            }
        return comparison

    def apply_new_weights(self, new_weights):
        """应用新权重（逐步迁移，避免激进变化）"""

        # 使用平滑过渡：新权重 = 0.7*旧 + 0.3*建议
        smoothed_weights = {}
        for key in self.current_weights:
            smoothed_weights[key] = 0.7 * self.current_weights[key] + 0.3 * new_weights[key]

        self.current_weights = smoothed_weights
        self.save_weights_to_config()

        return smoothed_weights
```

#### 第四步：HTML 仪表板

```html
<!-- 新增页面：accuracy-dashboard.html -->

<!DOCTYPE html>
<html>
<head>
    <title>Alpha Hive 准确度看板</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .metric-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        .metric-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .metric-value {
            font-size: 32px;
            font-weight: 700;
            margin: 10px 0;
        }
        .metric-label {
            font-size: 14px;
            opacity: 0.9;
        }
        .chart {
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Alpha Hive 准确度看板</h1>

        <!-- 综合指标 -->
        <div class="metric-card">
            <h2>🎯 综合准确度指标（过去 90 天）</h2>
            <div class="metric-grid">
                <div class="metric-box">
                    <div class="metric-label">T+1 方向准确度</div>
                    <div class="metric-value">85%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">T+7 方向准确度</div>
                    <div class="metric-value">78%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">T+30 方向准确度</div>
                    <div class="metric-value">72%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Sharpe 比率</div>
                    <div class="metric-value">1.82</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">平均收益（T+7）</div>
                    <div class="metric-value">+4.2%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">胜率</div>
                    <div class="metric-value">68%</div>
                </div>
            </div>
        </div>

        <!-- Agent 贡献度 -->
        <div class="metric-card">
            <h2>🐝 Agent 贡献度分析</h2>
            <table class="agent-table">
                <thead>
                    <tr>
                        <th>Agent</th>
                        <th>当前权重</th>
                        <th>准确度</th>
                        <th>建议权重</th>
                        <th>变更</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Scout Bee</td>
                        <td>30%</td>
                        <td>86%</td>
                        <td>32%</td>
                        <td>↑ +2%</td>
                    </tr>
                    <tr>
                        <td>SentimentBee</td>
                        <td>20%</td>
                        <td>58%</td>
                        <td>16%</td>
                        <td>↓ -4%</td>
                    </tr>
                    <tr>
                        <td>OddsBee</td>
                        <td>15%</td>
                        <td>84%</td>
                        <td>18%</td>
                        <td>↑ +3%</td>
                    </tr>
                    <tr>
                        <td>CatalystBee</td>
                        <td>20%</td>
                        <td>79%</td>
                        <td>21%</td>
                        <td>↑ +1%</td>
                    </tr>
                    <tr>
                        <td>CrossBee</td>
                        <td>10%</td>
                        <td>81%</td>
                        <td>11%</td>
                        <td>↑ +1%</td>
                    </tr>
                    <tr>
                        <td>ValidatorBee</td>
                        <td>5%</td>
                        <td>75%</td>
                        <td>2%</td>
                        <td>↓ -3%</td>
                    </tr>
                </tbody>
            </table>
            <p>💡 SentimentBee 准确度低于基准，建议降低 X 情绪数据权重。</p>
        </div>

        <!-- 推荐和实际对比 -->
        <div class="metric-card">
            <h2>📈 推荐回溯详情（过去 20 个推荐）</h2>
            <table class="backtest-table">
                <thead>
                    <tr>
                        <th>日期</th>
                        <th>标的</th>
                        <th>评分</th>
                        <th>推荐</th>
                        <th>T+7 收益</th>
                        <th>方向准确</th>
                        <th>结果</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="win">
                        <td>2026-02-23</td>
                        <td>NVDA</td>
                        <td>8.52</td>
                        <td>Long $650</td>
                        <td>+6.8%</td>
                        <td>✓ 正确</td>
                        <td>✅ 赚取 +6.8%</td>
                    </tr>
                    <tr class="loss">
                        <td>2026-02-20</td>
                        <td>TSLA</td>
                        <td>6.85</td>
                        <td>Neutral</td>
                        <td>-3.2%</td>
                        <td>✗ 错误</td>
                        <td>❌ 本应规避</td>
                    </tr>
                    <!-- 更多行... -->
                </tbody>
            </table>
        </div>

        <!-- 权重调整历史 -->
        <div class="metric-card">
            <h2>📊 权重演变历史</h2>
            <canvas id="weights-chart"></canvas>
            <script>
                // 使用 Chart.js 绘制权重变化趋势
            </script>
        </div>
    </div>
</body>
</html>
```

---

## 优化 3: Catalyst Refinement

### 🎯 **目标**
把"财报发布（2周内）"精细化为"2026-03-15 美股收盘前 4 分钟发布，隐含波动率 15%"

### 📐 **实现方案**

#### 第一步：精细化催化剂数据模型

```python
class CatalystRefinement:
    """精细化催化剂信息"""

    def __init__(self, ticker):
        self.ticker = ticker
        self.catalysts = []

    def add_catalyst(self, event_type, **details):
        """添加精细化的催化剂"""

        catalyst = {
            "type": event_type,  # "earnings", "fda_decision", "merger", "product_launch"
            "event_name": details.get("event_name"),

            # 时间精细化
            "scheduled_date": details.get("scheduled_date"),  # YYYY-MM-DD
            "scheduled_time": details.get("scheduled_time"),  # HH:MM (美东时间)
            "time_window_days": details.get("time_window_days", 0),  # ±多少天可能延期
            "is_confirmed": details.get("is_confirmed", False),  # 是否官方确认

            # 历史模式
            "historical_surprise_pct": details.get("historical_surprise_pct", 0),
            "avg_move_magnitude": details.get("avg_move_magnitude", 0),  # 平均波动 %
            "upside_downside_ratio": details.get("upside_downside_ratio", 1.0),  # 上行/下行比例

            # 市场预期
            "market_consensus": details.get("market_consensus"),  # "Beat", "Miss", "In-line"
            "consensus_confidence": details.get("consensus_confidence", 0),  # 0-100%
            "iv_implied": details.get("iv_implied"),  # 期权隐含波动率 %
            "polymarket_odds": details.get("polymarket_odds", {}),  # {"beat": 0.65, "miss": 0.35}

            # 关键数据点
            "key_metrics": details.get("key_metrics", {}),  # 市场关注的指标
            "break_conditions": details.get("break_conditions", []),  # 失效条件

            # 下游效应
            "subsequent_events": details.get("subsequent_events", []),
            "risk_factors": details.get("risk_factors", [])
        }

        self.catalysts.append(catalyst)
        return catalyst

# 使用示例
nvda_catalyst = CatalystRefinement("NVDA")

earnings_catalyst = nvda_catalyst.add_catalyst(
    "earnings",
    event_name="Q4 FY2026 Earnings Release",
    scheduled_date="2026-03-15",
    scheduled_time="16:00",  # 美东时间下午 4 点
    time_window_days=2,  # 可能延期 ±2 天
    is_confirmed=True,

    # 历史数据
    historical_surprise_pct=2.3,  # NVDA 平均 beat 2.3%
    avg_move_magnitude=8.5,  # 平均 8.5% 波动
    upside_downside_ratio=1.8,  # 上行风险大于下行

    # 市场预期
    market_consensus="Beat",
    consensus_confidence=72,  # 72% 分析师预期 Beat
    iv_implied=15.2,  # 期权市场隐含 15.2% 波动率
    polymarket_odds={"beat": 0.68, "miss": 0.22, "inline": 0.10},

    # 关键指标
    key_metrics={
        "revenue_estimate": 32.5,  # 十亿美元
        "revenue_beat_threshold": 31.8,  # < 这个是 miss
        "datacenter_revenue_importance": "critical",  # 数据中心收入最关键
        "guidance_direction": "most_important"  # 指引比实际数字更重要
    },

    # 失效条件
    break_conditions=[
        "如果 CEO 宣布离职",
        "如果报告被延期 > 5 天",
        "如果重大竞争对手同日宣布重大产品"
    ],

    # 后续事件
    subsequent_events=[
        {
            "event": "Earnings Call",
            "date": "2026-03-15",
            "time": "17:00",  # 下午 5 点开始
            "focus_areas": ["AI 芯片 demand", "中国市场前景", "毛利率指引"]
        },
        {
            "event": "GPU供应链更新",
            "date": "2026-05-15",
            "time": "unknown",
            "probability": 0.45,
            "importance": "secondary"
        }
    ],

    # 风险因素
    risk_factors=[
        "宏观经济衰退可能导致 AI 芯片需求下滑",
        "竞争对手 AMD 发布更强产品可能压低价格",
        "中国禁令风险可能突然升级"
    ]
)
```

#### 第二步：集成外部日历数据

```python
class CatalystCalendarIntegration:
    """集成多个日历和数据源"""

    def __init__(self):
        self.data_sources = {
            "earnings": self.fetch_earnings_calendar(),
            "economic": self.fetch_economic_calendar(),
            "fda": self.fetch_fda_calendar(),
            "mergers": self.fetch_ma_tracker(),
            "product_launches": self.fetch_product_launch_calendar(),
            "polymarket": self.fetch_polymarket_events()
        }

    def fetch_earnings_calendar(self):
        """从多个来源获取财报日历"""
        sources = [
            "Yahoo Finance API",
            "MarketWatch",
            "Nasdaq Earnings Calendar",
            "Company Investor Relations"
        ]

        # 聚合多源数据，选最可靠的
        earnings_data = []
        for source in sources:
            data = self.query_api(source, ticker=self.ticker)
            earnings_data.append(data)

        # 选择最高置信度的数据
        return self.select_most_reliable(earnings_data)

    def fetch_polymarket_events(self):
        """从 Polymarket 获取事件赔率"""
        polymarket_api = "https://api.polymarket.com"

        # 查询相关事件市场
        events = requests.get(
            f"{polymarket_api}/events",
            params={"question": self.ticker}
        ).json()

        # 只返回相关性高的市场
        relevant_events = [
            {
                "market_id": event["id"],
                "question": event["question"],
                "odds": event["outcome_prices"],
                "volume_24h": event["volume_24h"],
                "liquidity": event["liquidity"]
            }
            for event in events
            if event["similarity_score"] > 0.8
        ]

        return relevant_events

    def enrich_catalyst(self, catalyst):
        """用外部数据丰富催化剂信息"""

        if catalyst["type"] == "earnings":
            # 查询财报历史
            historical = self.fetch_historical_earnings(
                catalyst["scheduled_date"]
            )
            catalyst["historical_data"] = historical

            # 更新隐含波动率
            catalyst["iv_implied"] = self.fetch_current_iv(
                days_to_event=self.days_until(catalyst["scheduled_date"])
            )

        return catalyst

# 使用示例
calendar = CatalystCalendarIntegration()
catalyst = nvda_catalyst.catalysts[0]
enriched_catalyst = calendar.enrich_catalyst(catalyst)
```

#### 第三步：时间相关的风险评估

```python
class CatalystTimingRisk:
    """评估催化剂时间相关的风险"""

    def __init__(self, catalyst):
        self.catalyst = catalyst

    def get_timing_risk(self):
        """评估时间风险（延期、提前等）"""

        risk_score = 0
        risk_factors = []

        # 因素 1：延期历史
        if self.catalyst["historical_surprise_pct"] and self.catalyst["is_confirmed"]:
            if self.catalyst["time_window_days"] > 5:
                risk_score += 15
                risk_factors.append("历史上延期风险高")

        # 因素 2：官方确认程度
        if not self.catalyst["is_confirmed"]:
            risk_score += 20
            risk_factors.append("日期未官方确认")

        # 因素 3：时间接近度
        days_until = self.days_until_event()
        if days_until < 3:
            risk_score += 10
            risk_factors.append("距离事件很近（< 3 天），变数少")
        elif days_until < 14:
            risk_score += 5

        # 因素 4：同日其他重大事件
        conflicting_events = self.check_conflicting_events()
        if conflicting_events:
            risk_score += 10 * len(conflicting_events)
            risk_factors.append(f"同日有 {len(conflicting_events)} 个其他事件")

        return {
            "timing_risk_score": min(100, risk_score),
            "risk_factors": risk_factors,
            "reliability_grade": self.get_reliability_grade(risk_score)
        }

    def get_reliability_grade(self, risk_score):
        """根据风险评分给出可靠性等级"""
        if risk_score < 20:
            return "A+ (极高可靠性)"
        elif risk_score < 40:
            return "A (高可靠性)"
        elif risk_score < 60:
            return "B (中等可靠性)"
        else:
            return "C (低可靠性)"

    def days_until_event(self):
        return (
            datetime.strptime(self.catalyst["scheduled_date"], "%Y-%m-%d") -
            datetime.now()
        ).days

    def check_conflicting_events(self):
        """检查同日是否有其他重大事件（FOMC、重大产品发布等）"""
        conflicting = []
        # 查询经济日历、其他公司事件等
        return conflicting
```

#### 第四步：HTML 报告集成

```html
<!-- 精细化催化剂展示 -->

<section id="catalysts-refined" class="report-section">
  <h2>🎯 催化剂日期 & 时间线（精细化）</h2>

  <div class="catalyst-container">
    <!-- 主催化剂 -->
    <div class="catalyst-card primary">
      <div class="catalyst-header">
        <h3>📊 Q4 FY2026 财报发布（主催化剂）</h3>
        <div class="reliability-badge">
          <span class="grade">A+ 极高可靠性</span>
        </div>
      </div>

      <div class="catalyst-body">
        <!-- 时间精细化 -->
        <div class="catalyst-section">
          <h4>📅 时间精细化</h4>
          <table class="timing-table">
            <tr>
              <td><strong>确切日期</strong></td>
              <td>2026 年 3 月 15 日（星期五）</td>
            </tr>
            <tr>
              <td><strong>发布时间</strong></td>
              <td>美东时间下午 4:00 PM（NYSE 收盘后）</td>
            </tr>
            <tr>
              <td><strong>时间确定性</strong></td>
              <td>✅ 官方确认（IR 网站）</td>
            </tr>
            <tr>
              <td><strong>延期风险</strong></td>
              <td>低（历史上极少延期）</td>
            </tr>
            <tr>
              <td><strong>距离现在</strong></td>
              <td>21 天</td>
            </tr>
          </table>
        </div>

        <!-- 历史对标 -->
        <div class="catalyst-section">
          <h4>📈 历史财报表现对标</h4>
          <table class="historical-table">
            <thead>
              <tr>
                <th>财报季度</th>
                <th>公告日期</th>
                <th>EPS Beat/Miss</th>
                <th>股价 24h 反应</th>
                <th>一周内最大波动</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Q3 FY2026</td>
                <td>2025-12-18</td>
                <td>+3.2% Beat</td>
                <td>+5.8%</td>
                <td>+8.2%</td>
              </tr>
              <tr>
                <td>Q2 FY2026</td>
                <td>2025-09-18</td>
                <td>+1.8% Beat</td>
                <td>+4.2%</td>
                <td>+6.5%</td>
              </tr>
              <tr>
                <td>Q1 FY2026</td>
                <td>2025-06-19</td>
                <td>+2.1% Beat</td>
                <td>+6.1%</td>
                <td>+7.8%</td>
              </tr>
              <tr class="avg">
                <td colspan="2"><strong>3 季平均</strong></td>
                <td><strong>+2.4% Beat</strong></td>
                <td><strong>+5.4%</strong></td>
                <td><strong>+7.5%</strong></td>
              </tr>
            </tbody>
          </table>
          <p class="insight">
            💡 NVIDIA 历史上 100% 的财报都超预期（Beat），
            平均股价上涨 5.4%。这次可能性很高。
          </p>
        </div>

        <!-- 市场预期 -->
        <div class="catalyst-section">
          <h4>🎯 市场预期 vs 隐含信息</h4>
          <table class="expectation-table">
            <tr>
              <td><strong>分析师共识</strong></td>
              <td>
                <div class="consensus-bar">
                  <div class="beat" style="width: 68%">Beat 68%</div>
                  <div class="inline" style="width: 18%">In-line 18%</div>
                  <div class="miss" style="width: 14%">Miss 14%</div>
                </div>
              </td>
            </tr>
            <tr>
              <td><strong>Polymarket 赔率</strong></td>
              <td>
                <div class="odds-display">
                  Beat: 65% | In-line: 22% | Miss: 13%
                </div>
              </td>
            </tr>
            <tr>
              <td><strong>期权隐含波动率</strong></td>
              <td>
                <strong style="color: #ff9800">15.2%</strong>
                (历史平均 12.8%)
                <span class="note">→ 市场预期较大波动</span>
              </td>
            </tr>
            <tr>
              <td><strong>预期股价范围</strong></td>
              <td>
                美式期权蝶式差价 → $620-$680 (±5% 当前价 $650)
              </td>
            </tr>
          </table>
        </div>

        <!-- 关键指标 -->
        <div class="catalyst-section">
          <h4>🔑 市场最关心的 3 个指标</h4>
          <div class="key-metrics">
            <div class="metric-item">
              <span class="importance">⭐⭐⭐ 极关键</span>
              <strong>数据中心收入</strong>
              <p>预期 $28.5B，去年同比 +15%。如果低于 $28B 或增速 < 10%，可能被视为 Miss。</p>
              <div class="trend">当前市场预期: $28.7B（小幅超预期）</div>
            </div>

            <div class="metric-item">
              <span class="importance">⭐⭐⭐ 极关键</span>
              <strong>毛利率指引</strong>
              <p>Q1 毛利率指引 > 70% 是"好"的信号。如果低于 68%，可能意味着竞争加剧。</p>
              <div class="trend">当前市场预期: 70.5% (略优于平均)</div>
            </div>

            <div class="metric-item">
              <span class="importance">⭐⭐⭐ 极关键</span>
              <strong>CEO 对中国市场前景的评论</strong>
              <p>市场担心中国出口禁令。任何负面评论可能导致 3-5% 下跌。</p>
              <div class="trend">当前风险: Polymarket 禁令概率 35%（中等风险）</div>
            </div>
          </div>
        </div>

        <!-- 时间表 & 投资计划 -->
        <div class="catalyst-section">
          <h4>📋 投资时间表 & 行动计划</h4>
          <div class="timeline">
            <div class="timeline-item">
              <div class="time">现在 (2026-02-23)</div>
              <div class="action">
                ✅ <strong>建立长仓</strong> - 评分 8.52/10，目标 $650，止损 $580
              </div>
            </div>

            <div class="timeline-item">
              <div class="time">2026-03-06（9 天前）</div>
              <div class="action">
                📢 <strong>增加监控</strong> - 关注隐含波动率是否继续上升
                <br>（IV 上升 → 市场预期更大波动 → 风险/机会同时增加）
              </div>
            </div>

            <div class="timeline-item">
              <div class="time">2026-03-13（2 天前）</div>
              <div class="action">
                🔍 <strong>最后风险检查</strong><br>
                ✓ 确认发布时间无变化<br>
                ✓ 检查是否有同日其他重大事件<br>
                ✓ 检查中国监管风险是否升级<br>
                ✓ 决定是否加仓、减仓或对冲
              </div>
            </div>

            <div class="timeline-item">
              <div class="time">2026-03-15 16:00</div>
              <div class="action">
                🚀 <strong>财报发布</strong> - 可能出现 5-8% 的快速波动
              </div>
            </div>

            <div class="timeline-item">
              <div class="time">2026-03-15 17:00</div>
              <div class="action">
                🎤 <strong>Earnings Call 开始</strong> - CEO 将讨论关键指标和中国前景
              </div>
            </div>

            <div class="timeline-item">
              <div class="time">2026-03-16-17</div>
              <div class="action">
                📊 <strong>反应阶段</strong> - 市场消化财报信息，可能在 2 天内见顶或见底
              </div>
            </div>
          </div>
        </div>

        <!-- 失效条件 -->
        <div class="catalyst-section highlight">
          <h4>🚨 财报催化剂失效条件</h4>
          <ul>
            <li>❌ 财报被延期 > 1 周</li>
            <li>❌ CEO 宣布离职或重大丑闻</li>
            <li>❌ 美国芯片出口禁令突然升级</li>
            <li>❌ 竞争对手同日发布重大产品（已检查：无重大冲突）</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 次级催化剂 -->
    <div class="catalyst-card secondary">
      <h3>📅 次级催化剂</h3>

      <div class="secondary-catalyst">
        <h4>🔧 GPU 供应链更新（预计）</h4>
        <p><strong>日期：</strong>2026-05-15（预计，概率 45%）</p>
        <p><strong>重要性：</strong>中等 - 关于产能和新产品发布时间表</p>
        <p><strong>影响：</strong>长期增长前景相关，短期影响有限</p>
      </div>

      <div class="secondary-catalyst">
        <h4>📱 新产品发布（AI 芯片新架构）</h4>
        <p><strong>日期：</strong>待定（通常 Q2）</p>
        <p><strong>重要性：</strong>中等 - 竞争力维持相关</p>
        <p><strong>影响：</strong>如果超预期 +10-15%；如果失望 -3-5%</p>
      </div>
    </div>
  </div>
</section>

<style>
  .catalyst-container {
    margin: 20px 0;
  }

  .catalyst-card {
    background: white;
    border-radius: 8px;
    border: 2px solid #667eea;
    padding: 20px;
    margin: 20px 0;
  }

  .catalyst-card.primary {
    border-color: #27ae60;
    background: #f0f8f4;
  }

  .catalyst-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
  }

  .reliability-badge .grade {
    background: #27ae60;
    color: white;
    padding: 6px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
  }

  .catalyst-section {
    margin: 20px 0;
    padding: 15px;
    background: #fafafa;
    border-radius: 6px;
    border-left: 3px solid #667eea;
  }

  .timing-table, .historical-table, .expectation-table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
  }

  .timing-table td, .historical-table td, .expectation-table td {
    padding: 10px;
    border-bottom: 1px solid #eee;
  }

  .timing-table td:first-child,
  .historical-table th,
  .expectation-table td:first-child {
    font-weight: 600;
    background: #f5f5f5;
  }

  .timeline {
    position: relative;
    padding: 20px 0 20px 40px;
  }

  .timeline-item {
    margin: 20px 0;
    position: relative;
    padding-left: 30px;
  }

  .timeline-item::before {
    content: '';
    position: absolute;
    left: -40px;
    top: 5px;
    width: 12px;
    height: 12px;
    background: #667eea;
    border-radius: 50%;
    border: 3px solid white;
  }

  .timeline-item::after {
    content: '';
    position: absolute;
    left: -35px;
    top: 20px;
    width: 2px;
    height: 25px;
    background: #ddd;
  }

  .timeline-item:last-child::after {
    display: none;
  }

  .time {
    font-weight: 600;
    color: #667eea;
    font-size: 14px;
  }

  .action {
    color: #333;
    margin-top: 5px;
    line-height: 1.5;
  }

  .key-metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 15px;
  }

  .metric-item {
    background: white;
    padding: 15px;
    border-left: 4px solid #2196f3;
    border-radius: 4px;
  }

  .importance {
    color: #f44336;
    font-weight: 600;
    font-size: 12px;
  }

  .trend {
    margin-top: 8px;
    padding: 8px;
    background: #f5f5f5;
    border-radius: 4px;
    font-size: 13px;
    color: #666;
  }

  .highlight {
    background: #fff3cd;
    border-left: 4px solid #ff9800;
  }
</style>
```

---

## 📊 实现时间表

| 优化项 | 工作量 | 预计完成时间 | 优先级 |
|--------|--------|-----------|--------|
| 优化 5：Thesis Breaks | 2-3 天 | 2026-02-26 | 🔴 第 1 |
| 优化 4：Crowding Detection | 3-4 天 | 2026-02-27 | 🔴 第 2 |
| 优化 7：Feedback Loop | 4-5 天 | 2026-03-02 | 🔴 第 3 |
| 优化 3：Catalyst Refinement | 2-3 天 | 2026-02-28 | 🟡 第 4 |

---

## 🚀 后续优化路线图

完成这 4 个优化后，建议继续：
1. **优化 1** - 实时信号冲突检测（难度高，但价值极大）
2. **优化 2** - 期权衍生品信号集成
3. **优化 6** - 中文本地化支持
4. **优化 8** - Meta-Agent 系统（自动生成专用 Agent）

---

**准备好开始实现了吗？** 🐝
