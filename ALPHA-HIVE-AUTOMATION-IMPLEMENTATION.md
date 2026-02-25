# 🐝 Alpha Hive 自动化完整实现指南

**版本**: 2.0 | **日期**: 2026-02-24 | **状态**: ✅ 已完成并激活

---

## 📋 执行摘要

本实现完成了 Alpha Hive 投资研究系统从手动流程到 **24/7 全自动编排** 的升级。通过引入统一的编排脚本、灵活的 CLI 参数、自动 GitHub 部署和实时仪表板，系统现在可以：

✅ 每日自动在指定时间运行（UTC 03:00 主扫 + UTC 17:00 午盘）
✅ 接受灵活的标的列表参数（--tickers NVDA TSLA VKTX）
✅ 执行 5 个自动化步骤（数据采集 → 蜂群分析 → ML 报告 → 仪表板 → GitHub 推送）
✅ 单点失败不影响整体流程（每步独立错误处理）
✅ 实时记录系统状态和执行日志
✅ 自动生成中英文报告并推送到 GitHub Pages

---

## 🏗️ 架构设计

### 整体流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cron 触发                                    │
│  UTC 03:00 (主扫) 或 UTC 17:00 (午盘) 每工作日                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
    ┌──────────────────────────────────────────┐
    │ alpha-hive-orchestrator.sh (唯一入口)   │
    │ 解析参数：--tickers NVDA TSLA VKTX      │
    └──────────────────┬───────────────────────┘
                       │
        ┌──────────────┴──────────────┬─────────────┬──────────────┬──────────────┐
        │                              │              │              │              │
        ▼                              ▼              ▼              ▼              ▼
  Step 1:                        Step 2:         Step 3:        Step 4:        Step 5:
  data_fetcher.py           alpha_hive_      generate_ml_   update_       auto_deploy.py
  (数据采集)               daily_report.py   report.py      dashboard.py   (GitHub推送)
  └─────────────┬─────────────┴──────────────┴──────────────┴──────────────┬─────────────┘
                │                                                            │
                └────────────────────────────────┬─────────────────────────┘
                                                 │
                                                 ▼
                                      status.json (系统状态)
                                      orchestrator-YYYY-MM-DD.log
```

### 文件结构

```
/Users/igg/
├── .claude/
│   ├── scripts/
│   │   ├── alpha-hive-orchestrator.sh ........... [新建] 唯一 Cron 入口
│   │   ├── alpha-hive-daily.sh .................. [保留] 备份
│   │   └── ...
│   ├── reports/
│   │   ├── alpha_hive_daily_report.py ........... [修改] +argparse --tickers
│   │   ├── generate_ml_report.py ................ [修改] +argparse --tickers
│   │   ├── auto_deploy.py ....................... [新建] GitHub 自动推送
│   │   ├── update_dashboard.py .................. [新建] 仪表板自动更新
│   │   ├── config.py ............................ [保持] 配置管理
│   │   ├── data_fetcher.py ...................... [保持] 数据采集
│   │   ├── index.html ........................... [自动生成] 仪表板首页
│   │   ├── alpha-hive-daily-YYYY-MM-DD.* ....... [自动生成] 日报
│   │   ├── status.json .......................... [自动生成] 系统状态
│   │   └── ...
│   ├── logs/
│   │   ├── orchestrator-YYYY-MM-DD.log ......... [自动生成] 编排日志
│   │   ├── cron.log ............................. [自动生成] Cron 日志
│   │   ├── cron-midday.log ...................... [自动生成] 午盘日志
│   │   └── ...
│   └── GITHUB-TOKEN-SETUP.md .................... [新建] Token 设置指南
│
└── CLAUDE.md (项目指令 - 保持不变)
```

---

## 🔄 核心改进

### 1️⃣ 统一编排脚本（alpha-hive-orchestrator.sh）

**问题解决**：
- ❌ 之前：两条独立流水线（Shell脚本路径 vs scheduler.py路径）
- ✅ 现在：单一唯一入口，所有流程统一协调

**特性**：

```bash
# 使用方式
bash /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh [可选标的列表]

# 示例
bash alpha-hive-orchestrator.sh                 # 默认：NVDA TSLA VKTX
bash alpha-hive-orchestrator.sh "AAPL MSFT"    # 自定义标的列表
```

**流程**：
```
1. 解析参数（默认或自定义标的）
2. 执行 5 个步骤（每步独立错误处理）
3. 记录时间戳和执行结果
4. 写入 status.json（系统状态）
5. 清理 30+ 天旧日志
```

### 2️⃣ 灵活的 CLI 参数支持

**修改内容**：

| 文件 | 参数 | 效果 |
|-----|------|------|
| alpha_hive_daily_report.py | --tickers NVDA TSLA | 指定扫描标的 |
| alpha_hive_daily_report.py | --all-watchlist | 扫描全部 watchlist |
| generate_ml_report.py | --tickers NVDA TSLA | 生成指定标的的 ML 报告 |
| generate_ml_report.py | --all-watchlist | 生成全部 watchlist 的 ML 报告 |

**代码示例**：
```python
parser = argparse.ArgumentParser()
parser.add_argument('--tickers', nargs='+', default=["NVDA", "TSLA", "VKTX"])
parser.add_argument('--all-watchlist', action='store_true')
args = parser.parse_args()

tickers = WATCHLIST if args.all_watchlist else args.tickers
reporter.run_daily_scan(focus_tickers=tickers)
```

### 3️⃣ 自动 GitHub 部署（auto_deploy.py）

**功能**：

```python
# 1. 读取 Token（从 ~/.alpha_hive_github_token）
token = deployer.read_github_token()

# 2. 扫描今日新文件
files = deployer.get_today_modified_files()

# 3. 提交并推送到 GitHub
deployer.push_to_github(files, token)

# 4. 更新 status.json（包含部署 URL）
deployer.update_status_json(deploy_result)
```

**安全性**：
- ✅ Token 存储在 ~/.alpha_hive_github_token（权限：600）
- ✅ 不硬编码 Token
- ✅ 自动生成 commit message：`📰 Alpha Hive 日报 YYYY-MM-DD | TICKER SCORE/10`

### 4️⃣ 实时仪表板更新（update_dashboard.py）

**生成的 index.html 包含**：

1. **今日 Top 3 机会** - 来自最新日报
2. **系统状态卡片** - 最后更新时间、运行状态
3. **最近报告侧边栏** - 过去 7 天的报告链接
4. **紫色渐变主题** - 与 Alpha Hive 品牌一致

**示例结构**：
```html
┌─────────────────────────────────────────┐
│  🐝 Alpha Hive 每日投资简报              │
├─────────────────────────────────────────┤
│ ┌──────────────────────┐  ┌──────────┐  │
│ │ 🎯 Top 3 机会      │  │📊系统状态│  │
│ │ - NVDA (8.5/10)   │  │✅ 运行中 │  │
│ │ - TSLA (6.2/10)   │  │⏰ 10:30 │  │
│ │ - VKTX (5.1/10)   │  │📜最近报告│  │
│ └──────────────────────┘  └──────────┘  │
└─────────────────────────────────────────┘
```

### 5️⃣ 改进的日志和状态管理

**日志路径统一**：
```
/Users/igg/.claude/logs/
├── orchestrator-YYYY-MM-DD.log  (编排日志，核心）
├── cron.log                      (每日主扫日志)
├── cron-midday.log              (午盘扫描日志)
└── [自动清理 30+ 天旧文件]
```

**status.json 示例**：
```json
{
  "last_run": "2026-02-24T10:30:45Z",
  "last_run_date": "2026-02-24",
  "status": "success",
  "total_duration_seconds": 152,
  "tickers": ["NVDA", "TSLA", "VKTX"],
  "steps_result": {
    "step1_data_fetcher": {"status": "success", "duration_seconds": 12},
    "step2_hive_analysis": {"status": "success", "duration_seconds": 45},
    "step3_ml_report": {"status": "success", "duration_seconds": 38},
    "step4_dashboard": {"status": "success", "duration_seconds": 18},
    "step5_github_deploy": {"status": "success", "duration_seconds": 39}
  },
  "deploy_status": "success",
  "deploy_url": "https://wangmingjie36-creator.github.io/alpha-hive-deploy/"
}
```

---

## 🚀 使用指南

### 初始设置

#### 1. 设置 GitHub Token（一次性）

```bash
# 参考完整指南：/Users/igg/.claude/GITHUB-TOKEN-SETUP.md
echo "ghp_your_token_here" > ~/.alpha_hive_github_token
chmod 600 ~/.alpha_hive_github_token
```

#### 2. 验证脚本权限

```bash
ls -la /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh
# 应显示：-rwxr-xr-x (755)
```

#### 3. 验证 Cron 配置

```bash
crontab -l | grep alpha-hive
```

### 手动运行

#### 默认标的列表（NVDA, TSLA, VKTX）

```bash
bash /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh
```

#### 自定义标的列表

```bash
bash /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh "AAPL MSFT TSLA"
```

#### 指定单个标的

```bash
bash /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh "NVDA"
```

### 自动运行（Cron）

```cron
# 每日主扫（UTC 03:00 = 北京时间 11:00）
0 3 * * * /bin/bash /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh

# 工作日午盘补充（UTC 17:00 = 美东 12:00）
0 17 * * 1-5 /bin/bash /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh "NVDA TSLA VKTX"
```

---

## 📊 验证与监控

### 查看执行状态

```bash
# 查看最新编排日志
tail -100 /Users/igg/.claude/logs/orchestrator-$(date +%Y-%m-%d).log

# 查看 JSON 状态
cat /Users/igg/.claude/reports/status.json | jq .

# 查看最新报告
ls -lh /Users/igg/.claude/reports/alpha-hive-daily-$(date +%Y-%m-%d).*
```

### 常用监控命令

```bash
# 检查所有步骤状态
cat /Users/igg/.claude/reports/status.json | jq '.steps_result'

# 检查部署 URL
cat /Users/igg/.claude/reports/status.json | jq '.deploy_url'

# 查看今日生成的所有文件
find /Users/igg/.claude/reports -name "*$(date +%Y-%m-%d)*" -type f

# 监控 Cron 日志（实时）
tail -f /Users/igg/.claude/logs/cron.log
```

---

## 🔍 故障排除

### 问题 1：编排脚本无法执行

**症状**：
```
bash: /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh: Permission denied
```

**解决**：
```bash
chmod +x /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh
ls -la /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh  # 检查权限
```

### 问题 2：Python 脚本导入错误

**症状**：
```
ModuleNotFoundError: No module named 'config'
```

**解决**：
```bash
# 确认在报告目录运行
cd /Users/igg/.claude/reports

# 或在编排脚本中修改 PYTHONPATH
export PYTHONPATH="/Users/igg/.claude/reports:$PYTHONPATH"
python3 alpha_hive_daily_report.py --tickers NVDA
```

### 问题 3：GitHub 部署失败

**症状**：
```
fatal: Authentication failed for 'https://github.com/...'
```

**检查清单**：
```bash
# 1. Token 文件存在且可读
cat ~/.alpha_hive_github_token

# 2. Token 权限正确（600）
ls -la ~/.alpha_hive_github_token

# 3. Token 有效（测试 API）
TOKEN=$(cat ~/.alpha_hive_github_token)
curl -H "Authorization: token $TOKEN" https://api.github.com/user

# 4. 仓库访问权限
curl -H "Authorization: token $TOKEN" \
  https://api.github.com/repos/wangmingjie36-creator/alpha-hive-deploy
```

### 问题 4：Cron 未执行

**症状**：日志无更新，没有新报告生成

**检查清单**：
```bash
# 1. Cron 是否启用
sudo launchctl list | grep cron

# 2. 验证 Cron 条目
crontab -l

# 3. 查看系统日志
log stream --predicate 'process == "cron"' --level debug

# 4. 手动触发测试
bash /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh

# 5. 检查文件权限
ls -la /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh
```

---

## 📈 性能指标

### 预期执行时间

| 步骤 | 耗时 | 说明 |
|-----|------|------|
| Step 1: 数据采集 | 10-20s | 网络 I/O |
| Step 2: 蜂群分析 | 30-60s | 3 个标的 |
| Step 3: ML 报告 | 20-40s | 模型推理 |
| Step 4: 仪表板 | 5-15s | 文件生成 |
| Step 5: GitHub 部署 | 20-40s | 网络推送 |
| **总计** | **90-180s** | ~2-3 分钟 |

### 磁盘使用

```
日报（JSON + MD）：      ~50KB per day
ML 报告（HTML）：       ~200KB per day
日志（编排）：          ~10KB per day
30天合计：              ~7MB 日志 + ~8MB 报告 = 15MB
```

---

## 🔒 安全考虑

### Token 安全

✅ **已实施**：
- Token 存储在用户主目录下的隐藏文件
- 文件权限严格限制（600 = 仅所有者可读）
- 不在脚本或日志中硬编码或记录 Token

🔄 **建议**：
- 每 3-6 个月轮换 Token
- 定期检查 GitHub 账户的授权应用
- 监控 GitHub Actions 日志（如果使用）

### 日志安全

- ✅ 不记录 Token 值
- ✅ 日志文件权限合理
- ✅ 自动清理 30+ 天旧日志（防止文件泄露）

---

## 📝 维护清单

### 日常维护

- [ ] **周一**：检查 Cron 日志（`tail -100 /Users/igg/.claude/logs/cron.log`）
- [ ] **每月一次**：查看 status.json 的错误率和性能
- [ ] **每季度**：轮换 GitHub Token

### 定期任务

- [ ] **每 30 天**：验证 GitHub 部署（访问仪表板 URL）
- [ ] **每 90 天**：生成新 GitHub PAT，删除旧的
- [ ] **每 6 个月**：审查日志压缩和存档策略

### 监控告警（可选，未实施）

未来可增加：
- [ ] Slack/邮件通知（编排失败时）
- [ ] 指标监控（执行时间、错误率）
- [ ] 性能追踪（报告生成速度趋势）

---

## 📚 相关文档

- 📖 [Alpha Hive CLAUDE.md](../CLAUDE.md) - 蜂群核心规则
- 🔐 [GitHub Token 安全设置](./GITHUB-TOKEN-SETUP.md)
- 📊 [Alpha Hive 内存库](../.claude/projects/-Users-igg/memory/MEMORY.md)

---

## 🎯 后续优化方向

### Phase 2（未来）

- [ ] 异常告警系统（Slack/邮件）
- [ ] 实时指标仪表板（Prometheus/Grafana）
- [ ] 蜂群 Agent 动态扩展（基于负载自动调整 spawn 数量）
- [ ] 信息素板持久化存储（数据库）
- [ ] 支持多账户和权限管理

### Phase 3（远期）

- [ ] 智能标的选择（基于历史表现动态调整 watchlist）
- [ ] 跨市场整合（美股 + 港股 + A 股）
- [ ] 实时事件推送（重大新闻自动触发快速扫描）
- [ ] API 服务（让其他系统调用 Alpha Hive）

---

## 📞 故障支持

遇到问题？按以下顺序排查：

1. **查看日志** → `/Users/igg/.claude/logs/orchestrator-YYYY-MM-DD.log`
2. **检查状态** → `/Users/igg/.claude/reports/status.json`
3. **验证 Token** → `cat ~/.alpha_hive_github_token`
4. **手动运行** → `bash /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh`
5. **查看本文档** → "故障排除"章节

---

**实现完成日期**: 2026-02-24
**系统状态**: ✅ 生产就绪
**最后验证**: 2026-02-24 10:35 UTC
**维护者**: Claude Code Agent
