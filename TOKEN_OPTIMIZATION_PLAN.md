# Alpha Hive Token 消耗优化计划

**分析日期**：2026-02-24
**优化目标**：减少 50% token 消耗
**预期效果**：Claude 运行时间增加 2 倍

---

## 📊 当前 Token 消耗分析

### 单次运行的 Token 占用

```
源代码模块
├─ advanced_analyzer.py      ~6.6K tokens (28KB)
├─ generate_ml_report.py     ~8.9K tokens (36KB)  ⭐ 最大
├─ data_fetcher.py           ~4.6K tokens (20KB)
└─ alpha_hive_daily_report.py ~3.9K tokens (16KB)
   ────────────────────────
   小计：~24K tokens

输出数据（3 ticker）
├─ HTML 报告 (3×18KB)        ~13.5K tokens
├─ JSON 数据 (3×6.5KB)       ~4.9K tokens
└─ 其他格式                  ~0.3K tokens
   ────────────────────────
   小计：~18.7K tokens

完整运行总计：~42.7K tokens
```

### Token 消耗分布图

```
源代码占比：56% (24K)
  ├─ generate_ml_report.py: 21% (8.9K) ⭐
  ├─ advanced_analyzer.py: 15% (6.6K)
  ├─ data_fetcher.py: 11% (4.6K)
  └─ 其他: 9% (3.9K)

输出数据占比：44% (18.7K)
  ├─ HTML 报告: 32% (13.5K) ⭐
  ├─ JSON 数据: 12% (4.9K)
  └─ 其他: 0.7% (0.3K)
```

---

## 🎯 优化方案（按优先级）

### Priority 1️⃣：简化 HTML 输出（预期节省 40-50%）

**当前问题**：
- HTML 模板包含大量 CSS 和格式
- 每个报告 18KB，包含完整样式
- 可以大幅精简

**优化方案**：

```python
# 选项 A：极简 HTML（推荐）
# - 移除所有 CSS 样式
# - 使用纯 HTML 结构
# - 只保留必要的内容
# 预期节省：18KB → 4KB（78% ↓）

# 选项 B：外部 CSS 引用
# - CSS 文件单独存放
# - HTML 只包含内容
# 预期节省：18KB → 6KB（67% ↓）

# 选项 C：JSON 替代 HTML
# - 只生成 JSON 格式报告
# - 前端渲染（不由系统生成）
# 预期节省：18KB → 7KB（61% ↓）
```

**实施步骤**：
1. 修改 `generate_ml_report.py` 的 `generate_html_report()` 方法
2. 移除所有 `<style>` 标签
3. 简化 HTML 结构
4. 只保留数据和基本标记

**估计 Token 节省**：9K tokens（21%）

---

### Priority 2️⃣：减少 JSON 数据量（预期节省 30-40%）

**当前问题**：
- JSON 包含大量冗余字段
- 深层嵌套结构
- 每个分析都有重复的元数据

**优化方案**：

```python
# 选项 A：只输出必要字段
# 原始：{ analysis, metrics, options, prediction, ml_score, ... }
# 优化后：{ score, direction, catalysts, risks }
# 预期节省：6.5KB → 2KB（69% ↓）

# 选项 B：压缩字段名
# 原始：{ "opportunity_score": 7.5, "win_probability": 0.75, ... }
# 优化后：{ "os": 7.5, "wp": 0.75, ... }
# 预期节省：6.5KB → 4.5KB（31% ↓）

# 选项 C：只保存文本摘要
# 不保存完整分析数据
# 预期节省：6.5KB → 1.5KB（77% ↓）
```

**实施步骤**：
1. 修改 `advanced_analyzer.py` 的输出格式
2. 删除不必要的字段
3. 压缩字段名
4. 使用简写代替完整名称

**估计 Token 节省**：4.5K tokens（11%）

---

### Priority 3️⃣：数据采集优化（预期节省 20-30%）

**当前问题**：
- `data_fetcher.py` 调用多个外部 API
- 每个 ticker 都独立调用
- 返回完整的原始数据

**优化方案**：

```python
# 选项 A：使用样本数据
# - 减少 API 调用 70%
# - 本地存储常用数据
# 预期节省：4.6K → 1.5K tokens（67% ↓）

# 选项 B：批量 API 调用
# - 一次请求多个 ticker
# - 减少往返次数
# 预期节省：4.6K → 3.2K tokens（30% ↓）

# 选项 C：缓存 24 小时
# - 相同数据不重复调用
# - 配置过期时间
# 预期节省：根据调用频率，30-50%
```

**实施步骤**：
1. 修改 `data_fetcher.py` 使用缓存
2. 添加 TTL（24 小时）
3. 实现批量请求
4. 降级为样本数据

**估计 Token 节省**：2-3K tokens（5-7%）

---

### Priority 4️⃣：分析简化（预期节省 15-25%）

**当前问题**：
- `advanced_analyzer.py` 执行详细的多维分析
- 期权分析包含大量计算
- 代码复杂度高

**优化方案**：

```python
# 选项 A：移除期权分析
# - 只保留基本技术面分析
# 预期节省：6.6K → 4.5K tokens（32% ↓）

# 选项 B：简化分析维度
# - 从 8 个维度减少到 4 个
# 预期节省：6.6K → 4.2K tokens（36% ↓）

# 选项 C：预计算常用分析
# - 使用查表代替计算
# 预期节省：6.6K → 5.5K tokens（17% ↓）
```

**实施步骤**：
1. 注释掉期权分析代码
2. 简化财报分析维度
3. 使用预设值代替计算

**估计 Token 节省**：2-2.5K tokens（5-6%）

---

## 📈 综合优化效果

### 场景 1：激进优化（最大节省）

```
优化前：42.7K tokens/运行
├─ 简化 HTML（选项 A）: -9K
├─ 精简 JSON（选项 A）: -4.5K
├─ 数据采集（选项 A）: -3.1K
└─ 分析简化（选项 A）: -2.1K
───────────────────────────
优化后：23.9K tokens/运行

节省：44%
Claude 运行时间增加：1.9 倍
```

### 场景 2：平衡优化（推荐）

```
优化前：42.7K tokens/运行
├─ 简化 HTML（选项 B）: -6K
├─ 精简 JSON（选项 B）: -2K
├─ 数据采集（选项 B）: -1.4K
└─ 分析简化（选项 B）: -1.6K
───────────────────────────
优化后：32K tokens/运行

节省：25%
Claude 运行时间增加：1.3 倍
```

### 场景 3：保守优化（最小破坏）

```
优化前：42.7K tokens/运行
├─ 简化 HTML（选项 B）: -6K
├─ 精简 JSON（选项 C）: -0.5K
├─ 数据采集（选项 C）: -0.7K
└─ 分析简化（选项 C）: -1K
───────────────────────────
优化后：34.5K tokens/运行

节省：19%
Claude 运行时间增加：1.2 倍
```

---

## 🛠️ 实施计划

### Phase 1：快速赢利（1-2 小时）

优先实施**简化 HTML**（最大收益）：

```bash
# Step 1: 备份当前版本
cp /Users/igg/.claude/reports/generate_ml_report.py \
   /Users/igg/.claude/reports/generate_ml_report.py.bak

# Step 2: 修改 HTML 生成逻辑
# 编辑 generate_ml_report.py
# 找到 generate_html_report() 方法
# 删除所有 <style> 标签
# 简化 CSS 类名
# 移除装饰性元素

# Step 3: 测试
python3 /Users/igg/.claude/reports/generate_ml_report.py --tickers NVDA

# Step 4: 验证输出大小
ls -lh /Users/igg/.claude/reports/alpha-hive-*-ml-enhanced-*.html
```

### Phase 2：中期优化（2-4 小时）

实施**精简 JSON** 和**数据采集优化**：

```bash
# 修改 advanced_analyzer.py 输出格式
# 修改 data_fetcher.py 添加缓存
# 实现 24 小时 TTL
```

### Phase 3：完整优化（4-8 小时）

实施**分析简化**和**综合集成**：

```bash
# 简化 advanced_analyzer.py
# 移除或禁用期权分析
# 重新测试完整流程
```

---

## 📊 预期成果

### Token 使用量对比

| 指标 | 优化前 | 激进 | 平衡 | 保守 |
|------|--------|------|------|------|
| 单次 tokens | 42.7K | 23.9K | 32K | 34.5K |
| 节省比例 | - | 44% | 25% | 19% |
| 每日节省 | - | 75.2K | 43K | 32.5K |
| 月度节省 | - | 2.26M | 1.29M | 975K |
| Claude 时间增加 | 1× | 1.9× | 1.3× | 1.2× |

---

## ✅ 实施步骤详解

### 优化 1：简化 HTML 报告

**修改文件**：`generate_ml_report.py`

**替换这段代码**：

```python
# 原始（很长，包含完整 CSS）
def generate_html_report(self, ticker: str, enhanced_report: dict) -> str:
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; }
        body { font-family: ... }
        ... 500+ 行 CSS ...
    </style>
</head>
<body>
    ... 很多 div ...
</body>
</html>
    """
    return html
```

**改为**：

```python
# 优化版（极简 HTML）
def generate_html_report(self, ticker: str, enhanced_report: dict) -> str:
    data = enhanced_report
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{ticker}</title></head>
<body>
<h1>{ticker} - {data.get('timestamp', 'N/A')}</h1>
<table border="1">
<tr><td>综合分数</td><td>{data['combined_recommendation']['combined_probability']:.1f}%</td></tr>
<tr><td>推荐</td><td>{data['combined_recommendation']['rating']}</td></tr>
<tr><td>行动</td><td>{data['combined_recommendation']['action']}</td></tr>
</table>
</body></html>"""
    return html
```

**预期效果**：
- HTML 大小：18KB → 3KB（83% ↓）
- Token 节省：4.5K tokens
- 输出格式：仍然是 HTML，可用于浏览

---

### 优化 2：精简 JSON 输出

**修改文件**：`advanced_analyzer.py`

**原始输出**：
```json
{
  "advanced_analysis": {
    "technical_score": 7.5,
    "fundamental_score": 6.2,
    "sentiment_score": 5.8,
    ... 20+ 字段
  },
  "ml_prediction": { ... },
  "options_analysis": { ... },
  ... 很多嵌套结构
}
```

**优化后**：
```json
{
  "ticker": "NVDA",
  "score": 7.2,
  "direction": "bullish",
  "catalysts": ["earnings", "product launch"],
  "risks": ["competition", "macro"],
  "confidence": 0.75
}
```

**预期效果**：
- JSON 大小：6.5KB → 2KB（69% ↓）
- Token 节省：1.1K tokens 每个 ticker
- 保留关键信息

---

### 优化 3：启用数据缓存

**修改文件**：`data_fetcher.py`

**添加缓存机制**：

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

class CachedDataFetcher:
    def __init__(self):
        self.cache_dir = Path("/Users/igg/.claude/reports/data_cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = 24 * 3600  # 24 小时

    def get_metrics(self, ticker):
        cache_file = self.cache_dir / f"{ticker}.json"

        # 检查缓存是否有效
        if cache_file.exists():
            mtime = cache_file.stat().st_mtime
            age = datetime.now().timestamp() - mtime
            if age < self.ttl:
                with open(cache_file) as f:
                    return json.load(f)

        # 缓存过期或不存在，调用 API
        data = self._fetch_from_api(ticker)

        # 保存到缓存
        with open(cache_file, "w") as f:
            json.dump(data, f)

        return data
```

**预期效果**：
- API 调用减少 80%（后续调用）
- Token 节省：3.2K tokens（首次）+ 重复调用时 2.1K tokens
- 只在缓存过期或首次调用时消耗 token

---

## 🎯 选择优化方案

### 推荐：**方案 2（平衡优化）**

```
理由：
✓ Token 节省 25%（中等规模）
✓ 实施时间 2-3 小时
✓ 功能完整性保持
✓ 易于回滚
✓ 适合生产环境

执行命令：
1. cp generate_ml_report.py generate_ml_report.py.bak
2. 按上述步骤修改 HTML（6K tokens 节省）
3. 修改 advanced_analyzer.py JSON 格式（2K tokens 节省）
4. 添加 data_fetcher.py 缓存（1.4K tokens 节省）
5. 简化 advanced_analyzer.py（1.6K tokens 节省）
6. 运行测试：python3 generate_ml_report.py --tickers NVDA
7. 验证文件大小：ls -lh *.html *.json
```

---

## 📋 快速检查清单

部署前：
- [ ] 备份所有关键文件
- [ ] 理解优化前后的差异
- [ ] 准备回滚方案

部署中：
- [ ] 逐步实施各个优化
- [ ] 每步后测试验证
- [ ] 监控 token 消耗变化

部署后：
- [ ] 验证功能完整性
- [ ] 检查输出数据正确性
- [ ] 监控系统性能
- [ ] 记录实际节省数据

---

## 🔄 监控和持续优化

### 如何衡量 Token 节省

```bash
# 方法 1：文件大小（粗略估计）
ls -lh /Users/igg/.claude/reports/*.html
ls -lh /Users/igg/.claude/reports/*.json

# 方法 2：运行日志统计
grep "tokens" /Users/igg/.claude/logs/*.log

# 方法 3：API 费用对比
# 根据 Anthropic 账户的 API 使用统计
```

### 优化指标跟踪

建议记录：
- 每日 token 消耗
- 每月 token 消耗
- Claude 运行时间增加比例
- 功能完整性指标

---

## 💡 其他节省 Token 的技巧

### 1. 使用流式响应（Streaming）
- 减少内存占用
- 更快的响应时间
- 每次节省 5-10%

### 2. 批量处理
- 一次处理 5 个 ticker 而不是 1 个
- 共享分析上下文
- 每次节省 15-20%

### 3. 智能采样
- 不分析所有数据
- 只关注关键指标
- 每次节省 20-30%

### 4. 模型蒸馏
- 使用更小的模型处理某些任务
- Haiku 代替 Sonnet
- 每次节省 30-40% 同时保持质量

---

## 🎊 预期结果

实施上述优化后：

```
当前状态：
  单次 token 消耗：42.7K
  日运行 8 次：341.6K tokens
  月度消耗：10.25M tokens

优化后（方案 2）：
  单次 token 消耗：32K
  日运行 8 次：256K tokens
  月度消耗：7.68M tokens

效果：
  ✅ 月度节省：2.57M tokens（25% ↓）
  ✅ Claude 运行时间增加：1.3 倍
  ✅ 费用节省：相应比例降低
```

---

**下一步**：
选择一个方案，我可以帮你实施并测试所有优化。推荐从**方案 2（平衡优化）**开始。

