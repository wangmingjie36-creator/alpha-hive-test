# 📋 Alpha Hive 实时数据集成 - 文件清单

> **日期**: 2026-02-23
> **状态**: ✅ 完全实现
> **版本**: 1.0

---

## 📁 新增文件清单

### 核心模块（4 个 Python 文件）

#### 1️⃣ `config.py` (274 行)
**用途**: 集中管理所有配置参数

**主要内容**:
- API 配置（Polymarket、StockTwits、Yahoo Finance 等）
- 缓存配置（TTL、目录、过期策略）
- 监控列表（NVDA、VKTX、TSLA）
- 评分权重（拥挤度、失效条件等）
- 催化剂日期（重要事件时间表）

**关键函数**:
- `init_cache()` - 初始化缓存目录

**编辑理由**:
- 添加新数据源
- 调整缓存 TTL
- 新增监控标的
- 修改权重参数

---

#### 2️⃣ `data_fetcher.py` (526 行)
**用途**: 实时数据采集系统，支持 6 个数据源

**主要类**:
- `CacheManager` - 缓存管理（加载、保存、过期检查）
- `DataFetcher` - 核心数据采集类

**支持的数据源**:
1. **StockTwits** - 社交媒体消息量和情绪
2. **Polymarket** - 预测市场赔率
3. **Yahoo Finance** - 股票价格和做空比例
4. **Google Trends** - 搜索热度
5. **SEC EDGAR** - 监管文件（Form 4、13F）
6. **Seeking Alpha** - 投资研究平台数据

**关键方法**:
- `get_stocktwits_metrics(ticker)` - 获取社交数据
- `get_polymarket_odds(ticker)` - 获取赔率
- `get_yahoo_finance_metrics(ticker)` - 获取价格数据
- `get_google_trends(ticker)` - 获取热度数据
- `get_sec_filings(ticker, form_type)` - 获取监管文件
- `get_seeking_alpha_mentions(ticker)` - 获取研究数据
- `collect_all_metrics(ticker)` - 综合采集所有指标

**输出**:
- JSON 文件：`realtime_metrics.json`（5.2KB，3 个标的）

**编辑理由**:
- 添加新数据源
- 修改示例数据
- 调整采集逻辑
- 实现真实 API 集成

---

#### 3️⃣ `generate_report_with_realtime_data.py` (523 行)
**用途**: 使用实时数据生成优化报告

**主要类**:
- `RealtimeReportGenerator` - 报告生成器

**关键方法**:
- `load_realtime_metrics(ticker)` - 加载实时数据
- `calculate_crowding_score(metrics)` - 计算拥挤度
- `generate_html_report(...)` - 生成 HTML
- `generate_realtime_report(ticker)` - 完整流程

**特点**:
- 响应式设计（支持移动端）
- 实时数据可视化
- 6 维度拥挤度图表
- 数据源信息面板
- 完整的免责声明

**输出**:
- HTML 文件：`alpha-hive-{TICKER}-realtime-2026-02-23.html`（13KB）

**编辑理由**:
- 修改报告样式
- 添加新的数据展示
- 自定义排版
- 集成额外优化指标

---

#### 4️⃣ `scheduler.py` (437 行)
**用途**: 定时任务调度系统

**主要类**:
- `ReportScheduler` - 报告生成调度器

**关键方法**:
- `collect_data()` - 采集数据
- `generate_reports()` - 生成报告
- `upload_to_github()` - 上传到 GitHub
- `full_pipeline()` - 完整流程
- `health_check()` - 系统健康检查

**支持的运行模式**:
1. **后台守护进程** - `python3 scheduler.py daemon`
2. **一次性执行** - `python3 scheduler.py once`
3. **Cron 任务** - `python3 scheduler.py cron`

**默认调度**:
- 每 5 分钟：采集数据
- 每 15 分钟：生成报告
- 每 30 分钟：上传 GitHub
- 每 1 小时：完整流程
- 每 6 小时：健康检查

**编辑理由**:
- 修改调度频率
- 添加新的任务
- 修改上传策略
- 自定义告警规则

---

### 文档文件（4 个 Markdown 文件）

#### 📄 `REALTIME-SETUP.md` (528 行)
**用途**: 详细的部署和使用指南

**覆盖内容**:
1. 快速开始（5 分钟内完成）
2. 依赖安装说明
3. 6 个数据源的配置方法
4. 3 种运行方式（单次、定时、后台）
5. 完整集成脚本
6. 详细故障排查
7. 成本分析

**适用人群**: 首次使用者

---

#### 📄 `REALTIME-INTEGRATION-SUMMARY.md` (620 行)
**用途**: 完整的系统总结和架构说明

**覆盖内容**:
1. 项目完成情况
2. 系统架构图
3. 数据流程
4. 快速开始（4 步）
5. 高级配置
6. 性能指标
7. 故障排查
8. 下一步行动

**适用人群**: 系统管理员、架构师

---

#### 📄 `QUICK-START-REALTIME.md` (468 行)
**用途**: 快速参考卡片

**覆盖内容**:
1. 5 分钟快速开始
2. 常用命令速查表
3. 数据查询示例
4. 配置修改示例
5. 故障排查速查表
6. 性能参考
7. 使用场景示例
8. Pro 提示

**适用人群**: 日常使用者

---

#### 📄 `REALTIME-FILES-MANIFEST.md` (本文件)
**用途**: 详细的文件清单和说明

**覆盖内容**:
1. 所有新增文件
2. 每个文件的用途
3. 代码行数统计
4. 关键函数说明
5. 输入/输出说明
6. 编辑建议

**适用人群**: 开发者、维护者

---

### 脚本文件（2 个 Shell 脚本）

#### 🔧 `setup_realtime.sh` (100+ 行)
**用途**: 一键部署脚本

**自动完成**:
1. 检查 Python 版本
2. 创建目录结构（cache、logs、backups）
3. 安装 Python 依赖
4. 验证配置文件
5. 执行首次采集
6. 生成首个报告
7. 启动定时任务（可选）

**用法**:
```bash
bash setup_realtime.sh
```

**预期耗时**: ~2 分钟

---

#### 🎮 `run_realtime.sh` (245+ 行)
**用途**: 系统控制脚本

**支持的命令**:
- `fetch` - 采集数据
- `report` - 生成报告
- `daemon start/stop/status/logs` - 后台进程控制
- `push` - 上传到 GitHub
- `full` - 完整流程
- `clean` - 清理缓存
- `check` - 系统检查

**用法**:
```bash
./run_realtime.sh [命令]
```

**示例**:
```bash
./run_realtime.sh daemon start  # 启动
./run_realtime.sh full          # 完整流程
./run_realtime.sh check         # 健康检查
```

---

## 📊 文件统计

### 代码行数

| 文件 | 行数 | 类型 | 功能 |
|------|------|------|------|
| `config.py` | 274 | Python | 配置管理 |
| `data_fetcher.py` | 526 | Python | 数据采集 |
| `generate_report_with_realtime_data.py` | 523 | Python | 报告生成 |
| `scheduler.py` | 437 | Python | 任务调度 |
| **Python 总计** | **1,760** | | |
| `REALTIME-SETUP.md` | 528 | Markdown | 使用指南 |
| `REALTIME-INTEGRATION-SUMMARY.md` | 620 | Markdown | 系统总结 |
| `QUICK-START-REALTIME.md` | 468 | Markdown | 快速参考 |
| `REALTIME-FILES-MANIFEST.md` | ~500 | Markdown | 文件清单 |
| **文档总计** | **2,116** | | |
| `setup_realtime.sh` | ~100 | Shell | 部署脚本 |
| `run_realtime.sh` | ~245 | Shell | 控制脚本 |
| **脚本总计** | **~345** | | |
| **🎯 总计** | **~4,221** | | |

### 文件大小

| 文件 | 大小 | 备注 |
|------|------|------|
| `realtime_metrics.json` | 5.2 KB | 生成的实时数据 |
| `alpha-hive-NVDA-realtime-*.html` | 13 KB | 报告（单份） |
| `alpha-hive-VKTX-realtime-*.html` | 13 KB | 报告（单份） |
| `alpha-hive-TSLA-realtime-*.html` | 13 KB | 报告（单份） |
| **报告总计** | 39 KB | 3 份报告 |
| 缓存文件（6 个数据源） | ~20 KB | 自动生成 |
| 日志文件 | <1 MB | 自动生成 |

---

## 🔄 文件关系图

```
config.py
  ├─> 数据源配置
  ├─> 缓存 TTL
  ├─> 监控列表
  └─> 权重参数
        ↓
data_fetcher.py
  ├─> StockTwits
  ├─> Polymarket
  ├─> Yahoo Finance
  ├─> Google Trends
  ├─> SEC EDGAR
  └─> Seeking Alpha
        ↓
realtime_metrics.json
  ├─> 实时数据存储
  └─> 自动更新
        ↓
generate_report_with_realtime_data.py
  ├─> crowding_detector
  ├─> catalyst_refinement
  ├─> thesis_breaks
  └─> feedback_loop
        ↓
alpha-hive-*.html
  └─> 优化报告展示
        ↓
scheduler.py
  ├─> 定时采集
  ├─> 定时生成
  ├─> 定时上传
  └─> 健康检查
        ↓
GitHub Pages
  └─> 在线分享
```

---

## 🚀 快速导航

### 我想...

| 需求 | 文件 | 命令 |
|------|------|------|
| **部署系统** | `setup_realtime.sh` | `bash setup_realtime.sh` |
| **查看文档** | `REALTIME-SETUP.md` | `cat REALTIME-SETUP.md` |
| **快速参考** | `QUICK-START-REALTIME.md` | `cat QUICK-START-REALTIME.md` |
| **了解架构** | `REALTIME-INTEGRATION-SUMMARY.md` | `cat REALTIME-INTEGRATION-SUMMARY.md` |
| **采集数据** | `data_fetcher.py` | `python3 data_fetcher.py` |
| **生成报告** | `generate_report_with_realtime_data.py` | `python3 generate_report_with_realtime_data.py` |
| **启动后台** | `scheduler.py` | `python3 scheduler.py daemon` |
| **系统控制** | `run_realtime.sh` | `./run_realtime.sh [命令]` |
| **修改配置** | `config.py` | 用编辑器打开 |

---

## 📝 文件编辑指南

### 安全编辑

✅ **可以安全编辑**:
- `config.py` - 修改配置
- `data_fetcher.py` - 修改采集逻辑
- `generate_report_with_realtime_data.py` - 修改报告样式
- `scheduler.py` - 修改调度频率

⚠️ **谨慎编辑**:
- 文档文件（可能导致说明混乱）
- Shell 脚本（可能导致自动化失效）

❌ **不要编辑**:
- `realtime_metrics.json` - 自动生成
- `alpha-hive-*.html` - 自动生成
- `logs/` 目录 - 自动生成
- `cache/` 目录 - 自动生成

---

## 🔐 权限说明

```bash
-rw-r--r-- config.py                           # 可读写
-rw-r--r-- data_fetcher.py                     # 可读写
-rw-r--r-- generate_report_with_realtime_data.py # 可读写
-rw-r--r-- scheduler.py                        # 可读写
-rwxr-xr-x setup_realtime.sh                   # 可执行
-rwxr-xr-x run_realtime.sh                     # 可执行
-rw-r--r-- realtime_metrics.json               # 只读（自动生成）
```

---

## 💾 备份建议

### 定期备份

```bash
# 每周备份
mkdir -p backups/$(date +%Y%m%d)
cp realtime_metrics.json alpha-hive-*.html backups/$(date +%Y%m%d)/

# 或使用脚本
tar czf backups/backup-$(date +%Y%m%d).tar.gz \
  config.py \
  data_fetcher.py \
  generate_report_with_realtime_data.py \
  scheduler.py \
  realtime_metrics.json \
  alpha-hive-*.html
```

### 版本控制

```bash
# Git 跟踪配置和脚本
git add config.py data_fetcher.py scheduler.py
git add *.sh *.md
git commit -m "🔄 实时系统更新"

# 但不追踪自动生成的文件
echo "realtime_metrics.json" >> .gitignore
echo "alpha-hive-*-realtime-*.html" >> .gitignore
echo "logs/" >> .gitignore
echo "cache/" >> .gitignore
```

---

## 📞 获取帮助

### 查看完整文档

| 问题 | 查看文件 |
|------|---------|
| 如何安装和使用？ | `REALTIME-SETUP.md` |
| 常用命令是什么？ | `QUICK-START-REALTIME.md` |
| 系统如何工作的？ | `REALTIME-INTEGRATION-SUMMARY.md` |
| 每个文件是什么？ | `REALTIME-FILES-MANIFEST.md`（本文件） |

### 快速命令

```bash
# 一键部署
bash setup_realtime.sh

# 系统检查
./run_realtime.sh check

# 查看日志
./run_realtime.sh daemon logs

# 获取帮助
./run_realtime.sh  # 显示所有命令
```

---

## 🎯 下一步

1. **现在**：`bash setup_realtime.sh`
2. **5 分钟后**：在浏览器查看 `alpha-hive-NVDA-realtime-*.html`
3. **稍后**：使用 `./run_realtime.sh daemon start` 启动后台运行
4. **定期**：使用 `./run_realtime.sh check` 检查系统状态

---

**最后更新**: 2026-02-23
**版本**: 1.0
**维护者**: Alpha Hive Team

🚀 现在就开始：`bash setup_realtime.sh`
