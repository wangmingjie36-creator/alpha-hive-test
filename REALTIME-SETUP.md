# 🚀 Alpha Hive 实时数据集成指南

> **日期**：2026-02-23
> **状态**：✅ 实时数据系统已配置
> **版本**：1.0

---

## 📋 目录

1. [快速开始](#快速开始)
2. [安装依赖](#安装依赖)
3. [数据源配置](#数据源配置)
4. [运行实时采集](#运行实时采集)
5. [集成到报告](#集成到报告)
6. [故障排查](#故障排查)
7. [成本分析](#成本分析)

---

## 快速开始

### 第 1 步：验证基础设置

```bash
# 检查 Python 版本
python3 --version  # 需要 3.8+

# 检查已有的文件
ls -lh config.py data_fetcher.py
```

### 第 2 步：安装依赖库

```bash
# 安装所需的 Python 包
pip3 install requests yfinance pytrends beautifulsoup4

# 可选：用于数据处理
pip3 install pandas numpy

# 可选：用于定时任务
pip3 install schedule APScheduler
```

### 第 3 步：运行首次采集

```bash
# 执行数据采集脚本
python3 data_fetcher.py

# 检查输出
cat realtime_metrics.json | jq '.' | head -50
```

---

## 安装依赖

### 必需的库

| 库 | 用途 | 安装 | 说明 |
|----|----|------|------|
| `requests` | HTTP 请求 | `pip install requests` | 调用 API |
| `yfinance` | Yahoo Finance | `pip install yfinance` | 股票价格、做空比例 |
| `pytrends` | Google Trends | `pip install pytrends` | 搜索热度数据 |
| `beautifulsoup4` | 网页爬取 | `pip install beautifulsoup4` | 解析 HTML |

### 可选的库

| 库 | 用途 | 安装 |
|----|------|------|
| `schedule` | 定时任务 | `pip install schedule` |
| `APScheduler` | 高级定时 | `pip install APScheduler` |
| `pandas` | 数据处理 | `pip install pandas` |

### 完整安装

```bash
# 一次性安装所有库
pip3 install requests yfinance pytrends beautifulsoup4 schedule APScheduler pandas

# 验证安装
python3 -c "import yfinance; import requests; print('✅ 依赖安装成功')"
```

---

## 数据源配置

### 1️⃣ StockTwits API

**无需认证** ✅（公开数据）

```python
# data_fetcher.py 中已集成
# 直接调用即可
fetcher.get_stocktwits_metrics("NVDA")
```

### 2️⃣ Polymarket API

**无需认证** ✅（公开数据）

```python
# 完全免费的预测市场数据
fetcher.get_polymarket_odds("NVDA")
```

### 3️⃣ Yahoo Finance

**无需认证** ✅（yfinance 库处理）

```python
# 通过 yfinance 库自动处理认证
fetcher.get_yahoo_finance_metrics("NVDA")
```

### 4️⃣ Google Trends

**无需认证** ✅（pytrends 库处理）

```bash
# 注意：pytrends 有反爬虫限制，建议使用缓存
pip install pytrends
```

**使用建议**：
- 缓存时间：24 小时
- 查询间隔：避免连续请求
- 备用方案：使用 Google 官方 API（需付费）

### 5️⃣ SEC EDGAR（可选）

**无需认证** ✅（需要网页爬取）

```bash
# 安装爬取库
pip install beautifulsoup4 selenium

# 获取 CIK 号（一次性）
python3
>>> from data_fetcher import DataFetcher
>>> fetcher = DataFetcher()
>>> fetcher.get_sec_filings("NVDA", form_type="4")
```

**注意**：
- 仅用于主要投资人披露（Form 4）
- 建议缓存 7 天以上
- SEC 有请求频率限制

### 6️⃣ Seeking Alpha（可选）

**部分功能需付费** ⚠️

```bash
# 使用网页爬取（需代理避免被封）
pip install selenium cloudscraper

# 或使用官方 API（需订阅）
# 详见：https://api.seekingalpha.com
```

---

## 运行实时采集

### 方式 1：单次采集

```bash
# 采集单个标的
python3 -c "
from data_fetcher import DataFetcher
fetcher = DataFetcher()
metrics = fetcher.collect_all_metrics('NVDA')
print(metrics)
"
```

### 方式 2：批量采集

```bash
# 运行完整脚本（采集 NVDA、VKTX、TSLA）
python3 data_fetcher.py
```

**输出示例**：

```json
{
  "NVDA": {
    "timestamp": "2026-02-23T10:30:45.123456",
    "sources": {
      "stocktwits": {
        "messages_per_day": 45000,
        "bullish_ratio": 0.75,
        "sentiment_trend": "positive"
      },
      "polymarket": {
        "yes_odds": 0.65,
        "volume_24h": 8200000,
        "odds_change_24h": 8.2
      },
      "yahoo_finance": {
        "current_price": 145.32,
        "price_change_5d": 6.8,
        "short_float_ratio": 0.025
      }
    },
    "crowding_input": {
      "stocktwits_messages_per_day": 45000,
      "google_trends_percentile": 84.0,
      "bullish_agents": 5,
      "polymarket_odds_change_24h": 8.2
    }
  }
}
```

### 方式 3：定时采集（推荐）

**使用 schedule 库**：

```python
# scheduler.py
import schedule
import time
from data_fetcher import DataFetcher

def collect_and_report():
    fetcher = DataFetcher()
    tickers = ["NVDA", "VKTX", "TSLA"]
    for ticker in tickers:
        metrics = fetcher.collect_all_metrics(ticker)
        print(f"✅ {ticker} 数据已更新")

# 每 5 分钟采集一次（Polymarket 快速变化）
schedule.every(5).minutes.do(collect_and_report)

# 每 1 小时采集一次（StockTwits）
schedule.every(1).hours.do(collect_and_report)

while True:
    schedule.run_pending()
    time.sleep(1)
```

**运行定时采集**：

```bash
python3 scheduler.py &
```

**使用 APScheduler（更强大）**：

```python
# scheduler_advanced.py
from apscheduler.schedulers.background import BackgroundScheduler
from data_fetcher import DataFetcher
import logging

scheduler = BackgroundScheduler()
fetcher = DataFetcher()

def collect_job():
    for ticker in ["NVDA", "VKTX", "TSLA"]:
        fetcher.collect_all_metrics(ticker)

# 每 5 分钟运行一次
scheduler.add_job(collect_job, 'interval', minutes=5)
scheduler.start()

print("✅ 定时采集已启动")
```

---

## 集成到报告

### 更新 generate_optimized_report.py

修改生成报告脚本，使用实时数据：

```python
from data_fetcher import DataFetcher
from crowding_detector import CrowdingDetector

def generate_realtime_report(ticker: str) -> str:
    """使用实时数据生成优化报告"""

    # 1. 采集实时数据
    fetcher = DataFetcher()
    metrics = fetcher.collect_all_metrics(ticker)

    # 2. 拥挤度检测（使用实时数据）
    detector = CrowdingDetector(ticker)
    crowding_score, scores = detector.calculate_crowding_score(
        metrics["crowding_input"]
    )

    # 3. 生成报告
    html = generate_html_with_realtime_data(
        ticker=ticker,
        metrics=metrics,
        crowding_score=crowding_score,
        scores=scores
    )

    return html

# 使用示例
if __name__ == "__main__":
    for ticker in ["NVDA", "VKTX", "TSLA"]:
        html = generate_realtime_report(ticker)
        with open(f"alpha-hive-{ticker}-realtime.html", "w") as f:
            f.write(html)
```

### 完整集成脚本

```bash
#!/bin/bash
# realtime_report_generator.sh

# 采集数据
python3 data_fetcher.py

# 生成报告
python3 generate_optimized_report.py --realtime

# 上传到 GitHub Pages
git add alpha-hive-*.html realtime_metrics.json
git commit -m "🔄 实时报告更新 - $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main

echo "✅ 实时报告已生成并上传"
```

---

## 故障排查

### 问题 1：ImportError - 找不到模块

```bash
# 症状：ModuleNotFoundError: No module named 'yfinance'

# 解决：
pip3 install yfinance --upgrade

# 验证：
python3 -c "import yfinance; print('✅ OK')"
```

### 问题 2：网络超时

```bash
# 症状：requests.exceptions.Timeout

# 解决方案 1：增加超时时间
# 在 data_fetcher.py 中修改：
TIMEOUT = 20  # 从 10 改为 20 秒

# 解决方案 2：使用代理
PROXIES = {
    "http": "http://proxy.example.com:8080",
    "https": "http://proxy.example.com:8080",
}

# 解决方案 3：检查网络
curl -I https://api.stocktwits.com
```

### 问题 3：数据源无响应

```bash
# 症状：采集某个数据源失败

# 检查日志：
cat /Users/igg/.claude/reports/logs/data_fetcher.log

# 验证 API 可用性：
python3 -c "
import requests
response = requests.get('https://api.stocktwits.com/api/2/streams/symbols/NVDA.json', timeout=5)
print(response.status_code)
"
```

### 问题 4：缓存导致数据过期

```bash
# 症状：数据不更新

# 清除缓存：
rm -rf /Users/igg/.claude/reports/cache/*

# 或修改 TTL：
# 在 config.py 中调整缓存过期时间
CACHE_CONFIG = {
    "ttl": {
        "stocktwits": 1800,  # 30 分钟而不是 1 小时
        "polymarket": 60,    # 1 分钟而不是 5 分钟
    }
}
```

### 问题 5：内存不足

```bash
# 症状：MemoryError

# 解决：使用流式处理
# 修改 data_fetcher.py：

def collect_metrics_streaming(self, tickers: List[str]):
    """流式采集，避免一次性加载所有数据"""
    for ticker in tickers:
        yield self.collect_all_metrics(ticker)
```

---

## 成本分析

### 免费数据源 ✅

| 数据源 | 额度 | 成本 |
|--------|------|------|
| StockTwits | 无限 | 免费 |
| Polymarket | 无限 | 免费 |
| Yahoo Finance | 无限 | 免费 |
| Google Trends | ~200 req/day | 免费 |
| SEC EDGAR | 无限 | 免费 |

**总成本**：$0/月 ✅

### 可选付费升级

| 服务 | 功能 | 价格 |
|------|------|------|
| Alpha Vantage API | 实时股票数据 | $5-500/月 |
| Seeking Alpha Premium | 高级研究 | $239/年 |
| Bloomberg Terminal | 企业级数据 | $24,000/年 |
| IQFeed | 期权数据 | $148/月 |

**建议**：使用免费数据源首先验证系统，再考虑付费升级。

---

## 💡 最佳实践

### 1. 缓存策略

```python
# 根据数据变化频率设置不同的 TTL
CACHE_TTL = {
    "polymarket": 300,      # 5 分钟（快速变化）
    "stocktwits": 3600,     # 1 小时
    "google_trends": 86400, # 24 小时
    "sec_filings": 604800,  # 7 天
}
```

### 2. 错误处理

```python
# 实现优雅降级
try:
    data = fetcher.get_polymarket_odds(ticker)
except ConnectionError:
    logger.warning(f"Polymarket 不可用，使用缓存数据")
    data = cache.load(key, ttl=0)  # 忽略 TTL
```

### 3. 速率限制

```python
# 避免被 API 限流
import time
time.sleep(1)  # 请求间延迟 1 秒
```

### 4. 监控与告警

```python
# 定期检查数据质量
def health_check():
    for ticker in WATCHLIST:
        metrics = fetcher.collect_all_metrics(ticker)
        if metrics is None:
            send_alert(f"⚠️ {ticker} 数据采集失败")
```

---

## 🚀 下一步

1. **验证数据质量**
   ```bash
   python3 data_fetcher.py
   cat realtime_metrics.json | jq '.NVDA.crowding_input'
   ```

2. **集成到报告生成**
   ```bash
   # 更新 generate_optimized_report.py
   # 使用 realtime_metrics.json 而不是硬编码数据
   ```

3. **设置定时采集**
   ```bash
   # 创建 cron 任务或使用 scheduler.py
   */5 * * * * python3 /path/to/data_fetcher.py
   ```

4. **监控数据源**
   ```bash
   # 定期检查数据质量
   python3 -c "from data_fetcher import DataFetcher; f = DataFetcher(); print(f.collect_all_metrics('NVDA'))"
   ```

---

## 📞 常见问题

**Q: 是否可以自动生成报告？**
A: 是的。使用 scheduler.py + generate_optimized_report.py 的组合，可以每 5 分钟自动更新一次。

**Q: 数据延迟有多久？**
A:
- Polymarket：实时（<1 秒）
- StockTwits：5-10 分钟
- Google Trends：数小时延迟
- SEC EDGAR：1-2 天延迟

**Q: 如何处理数据缺失？**
A: data_fetcher.py 会自动降级到示例数据，同时记录错误日志供排查。

**Q: 可否离线运行？**
A: 不行。实时数据采集需要互联网连接。可以先采集数据保存到 JSON，然后离线使用。

---

**最后更新**：2026-02-23
**维护者**：Alpha Hive Team
**反馈**：提交 Issue 或 PR
