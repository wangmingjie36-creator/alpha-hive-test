# ⚡ Alpha Hive 实时系统快速参考

> **最后更新**: 2026-02-23
> **适用版本**: 1.0

---

## 🚀 5 分钟快速开始

### 第 1 步：一键部署（3 分钟）

```bash
bash setup_realtime.sh
```

**自动完成**：
- ✅ 安装依赖
- ✅ 采集数据
- ✅ 生成报告
- ✅ 启动守护进程

### 第 2 步：验证（1 分钟）

```bash
# 查看生成的报告
ls -lh alpha-hive-*-realtime-*.html

# 查看实时数据
cat realtime_metrics.json | jq '.NVDA.crowding_input'

# 查看运行状态
./run_realtime.sh daemon status
```

### 第 3 步：使用（1 分钟）

```bash
# 在浏览器中打开报告
open alpha-hive-NVDA-realtime-*.html

# 或查看日志
tail -f logs/scheduler.log
```

---

## 📋 常用命令速查表

### 数据采集

| 命令 | 说明 | 耗时 |
|------|------|------|
| `python3 data_fetcher.py` | 采集所有数据源 | ~300ms |
| `./run_realtime.sh fetch` | 采集数据（简化版） | ~300ms |

**示例**：
```bash
python3 data_fetcher.py
# 输出: 📊 开始采集 NVDA 的所有数据...
#       ✅ 数据采集完成 NVDA (0.00秒)
```

### 报告生成

| 命令 | 说明 | 耗时 |
|------|------|------|
| `python3 generate_report_with_realtime_data.py` | 生成所有报告 | ~600ms |
| `./run_realtime.sh report` | 生成报告（简化版） | ~600ms |

**示例**：
```bash
python3 generate_report_with_realtime_data.py
# 输出: 🎉 所有报告已生成完毕！
#       alpha-hive-NVDA-realtime-2026-02-23.html (13KB)
```

### 后台守护进程

| 命令 | 说明 |
|------|------|
| `./run_realtime.sh daemon start` | 启动守护进程 |
| `./run_realtime.sh daemon stop` | 停止守护进程 |
| `./run_realtime.sh daemon status` | 查看状态 |
| `./run_realtime.sh daemon logs` | 查看日志 |

**示例**：
```bash
# 启动
./run_realtime.sh daemon start
# 输出: ✅ 守护进程已启动 (PID: 12345)

# 查看状态
./run_realtime.sh daemon status
# 输出: ✅ 运行中 (PID: 12345)

# 查看日志（实时）
./run_realtime.sh daemon logs
# 输出: 2026-02-23 22:10:00 - INFO - 🔄 启动完整流程
```

### 完整流程

| 命令 | 说明 |
|------|------|
| `./run_realtime.sh full` | 采集 + 生成 + 上传 |
| `python3 scheduler.py once` | 同上 |

**示例**：
```bash
./run_realtime.sh full
# 输出: 🔄 执行完整流程...
#       ✅ 数据采集成功
#       ✅ 生成了 3 份报告
#       ✅ 上传成功
```

### GitHub 上传

| 命令 | 说明 |
|------|------|
| `./run_realtime.sh push` | 上传到 GitHub |
| `git push origin main` | 直接推送（手动） |

**示例**：
```bash
./run_realtime.sh push
# 输出: 🚀 上传到 GitHub...
#       ✅ 上传成功
```

### 系统维护

| 命令 | 说明 |
|------|------|
| `./run_realtime.sh check` | 健康检查 |
| `./run_realtime.sh clean` | 清理缓存 |

---

## 📊 数据查询速查表

### 查看实时拥挤度评分

```bash
python3 -c "
import json
with open('realtime_metrics.json') as f:
    data = json.load(f)
    for ticker in data:
        print(f'{ticker}:')
        metrics = data[ticker]['crowding_input']
        for key, value in metrics.items():
            print(f'  {key}: {value}')
"
```

### 查看最后更新时间

```bash
python3 -c "
import json
from datetime import datetime
with open('realtime_metrics.json') as f:
    data = json.load(f)
    ts = datetime.fromisoformat(data[list(data.keys())[0]]['timestamp'])
    delta = datetime.now() - ts
    print(f'最后更新: {int(delta.total_seconds())}秒前')
"
```

### 提取单个标的数据

```bash
# NVDA 的 Polymarket 赔率
cat realtime_metrics.json | jq '.NVDA.sources.polymarket.yes_odds'

# VKTX 的 StockTwits 消息量
cat realtime_metrics.json | jq '.VKTX.sources.stocktwits.messages_per_day'

# TSLA 的 5 日涨跌幅
cat realtime_metrics.json | jq '.TSLA.sources.yahoo_finance.price_change_5d'
```

---

## 🔧 配置速查表

### 更改采集频率

编辑 `scheduler.py`：

```python
# 改为每 10 分钟采集
schedule.every(10).minutes.do(scheduler.collect_data)

# 改为每 30 分钟生成报告
schedule.every(30).minutes.do(scheduler.generate_reports)
```

### 添加新标的

编辑 `config.py`：

```python
WATCHLIST = {
    "AMD": {
        "name": "Advanced Micro Devices",
        "sector": "Technology",
    },
}
```

编辑 `data_fetcher.py`：

```python
tickers = ["NVDA", "VKTX", "TSLA", "AMD"]  # 添加 AMD
```

### 更改缓存 TTL

编辑 `config.py`：

```python
CACHE_CONFIG = {
    "ttl": {
        "stocktwits": 1800,    # 改为 30 分钟
        "polymarket": 60,      # 改为 1 分钟
    }
}
```

---

## 🐛 故障排查速查表

### 问题：ImportError: No module named 'yfinance'

```bash
# 解决
pip3 install yfinance --upgrade

# 验证
python3 -c "import yfinance; print('OK')"
```

### 问题：缓存导致数据不更新

```bash
# 清除缓存
rm -rf cache/*

# 或重启守护进程
./run_realtime.sh daemon stop
./run_realtime.sh daemon start
```

### 问题：守护进程无响应

```bash
# 强制停止所有 Python 进程
pkill -f scheduler.py

# 重新启动
./run_realtime.sh daemon start

# 查看日志排查
tail -f logs/scheduler.log
```

### 问题：报告生成失败

```bash
# 检查数据文件
cat realtime_metrics.json | jq '.' | head -20

# 手动生成测试
python3 generate_report_with_realtime_data.py

# 查看错误
cat logs/scheduler.log | grep ERROR
```

### 问题：Git 推送失败

```bash
# 检查认证
git config user.name
git config user.email

# 重新配置（如需）
git config user.name "wangmingjie36-creator"
git config user.email "wangmingjie36@gmail.com"

# 测试连接
git push origin main --dry-run
```

---

## 📈 性能参考

### 执行时间

```
采集数据:     ~300ms （3 个标的，使用缓存）
生成报告:     ~600ms （3 份报告）
上传 GitHub:  ~5-10s （取决于网络）
完整流程:     ~15-20s
```

### 资源占用

```
内存:         ~50MB
CPU (空闲):   <1%
CPU (运行中): 5-10%
磁盘空间:     ~50KB（数据 + 缓存）
```

### 数据延迟

```
StockTwits:   实时（<1 秒）
Polymarket:   实时（<1 秒）
Yahoo Finance: 实时（延迟 5 分钟）
Google Trends: 数小时延迟
SEC EDGAR:    1-2 天延迟
```

---

## 🎯 使用场景

### 场景 1：每 5 分钟更新一次

```bash
# 启动守护进程（自动处理）
./run_realtime.sh daemon start

# 查看日志
./run_realtime.sh daemon logs
```

### 场景 2：每日早上 6 点生成报告

```bash
# 使用 crontab
crontab -e

# 添加：
0 6 * * * cd /Users/igg/.claude/reports && ./run_realtime.sh full
```

### 场景 3：手动一次性执行

```bash
# 执行完整流程
./run_realtime.sh full

# 或分步执行
./run_realtime.sh fetch
./run_realtime.sh report
./run_realtime.sh push
```

### 场景 4：仅采集数据，不生成报告

```bash
python3 data_fetcher.py
# 数据保存到 realtime_metrics.json
```

### 场景 5：在现有报告中集成实时数据

```bash
# 使用新的生成脚本
python3 generate_report_with_realtime_data.py

# 生成的报告包含实时数据
```

---

## 📚 文件速查表

| 文件 | 用途 | 权限 |
|------|------|------|
| `config.py` | 配置管理 | 可编辑 |
| `data_fetcher.py` | 数据采集 | 可编辑 |
| `generate_report_with_realtime_data.py` | 报告生成 | 可编辑 |
| `scheduler.py` | 定时调度 | 可编辑 |
| `setup_realtime.sh` | 一键部署 | 只读 |
| `run_realtime.sh` | 系统控制 | 只读 |
| `realtime_metrics.json` | 实时数据 | 自动生成 |
| `alpha-hive-*.html` | 优化报告 | 自动生成 |
| `logs/` | 日志目录 | 自动创建 |
| `cache/` | 缓存目录 | 自动创建 |

---

## 🚨 警告和注意

### ⚠️ 不要手动编辑这些文件

```
realtime_metrics.json    （自动生成）
alpha-hive-*.html        （自动生成）
logs/                    （自动生成）
cache/                   （自动生成）
```

### ⚠️ 网络要求

```
需要互联网连接以采集实时数据
离线模式：先采集后离线使用
```

### ⚠️ 定时任务限制

```
Crontab 最小间隔：1 分钟
后台守护进程最小间隔：1 秒
建议最小间隔：5 分钟（避免 API 限流）
```

---

## 💡 Pro 提示

### Tip 1：快速查看报告

```bash
# 直接在浏览器打开
open alpha-hive-NVDA-realtime-*.html

# 或使用服务器
python3 -m http.server 8000
# 然后访问 http://localhost:8000/alpha-hive-NVDA-realtime-*.html
```

### Tip 2：自动备份

```bash
# 每周备份一次
0 0 * * 0 cd /Users/igg/.claude/reports && tar czf backups/weekly-$(date +%Y%m%d).tar.gz alpha-hive-*.html realtime_metrics.json
```

### Tip 3：监控磁盘空间

```bash
# 定期清理旧报告
find . -name "alpha-hive-*-realtime-*.html" -mtime +30 -delete
```

### Tip 4：集成通知

```bash
# Crontab 中添加邮件通知
MAILTO=your-email@example.com
0 6 * * * cd /Users/igg/.claude/reports && ./run_realtime.sh full
```

---

## 📞 获取帮助

### 查看完整文档

```bash
cat REALTIME-INTEGRATION-SUMMARY.md    # 完整总结
cat REALTIME-SETUP.md                  # 详细部署指南
cat OPTIMIZATION-USAGE.md              # 优化功能使用
```

### 检查系统状态

```bash
./run_realtime.sh check

# 输出：
# 📁 文件检查:
#   ✅ config.py
#   ✅ data_fetcher.py
#   ...
# 📊 数据检查:
#   ✅ realtime_metrics.json 存在
#      包含 3 个标的
#   ...
```

### 查看日志

```bash
# 最近 10 行
tail logs/scheduler.log

# 实时监控
tail -f logs/scheduler.log

# 搜索错误
grep ERROR logs/scheduler.log
```

---

## 🎉 快速参考总结

```bash
# 一键部署
bash setup_realtime.sh

# 采集数据
python3 data_fetcher.py
./run_realtime.sh fetch

# 生成报告
python3 generate_report_with_realtime_data.py
./run_realtime.sh report

# 后台运行
./run_realtime.sh daemon start
./run_realtime.sh daemon status
./run_realtime.sh daemon logs
./run_realtime.sh daemon stop

# 完整流程
./run_realtime.sh full

# 上传 GitHub
./run_realtime.sh push
git push origin main

# 维护
./run_realtime.sh check
./run_realtime.sh clean
```

---

**最后更新**：2026-02-23
**版本**：1.0
**维护**：Alpha Hive Team

🚀 现在开始：`bash setup_realtime.sh`
