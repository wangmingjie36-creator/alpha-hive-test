# 🔔 Alpha Hive 智能告警系统 - 快速启动指南

**版本**: 1.0 | **日期**: 2026-02-24 | **状态**: ✅ 已部署

---

## 📊 系统概览

### 核心功能

```
编排脚本执行
    ↓
status.json 生成
    ↓
告警分析引擎 (新)
    ├─ 检测 P0: 系统失败
    ├─ 检测 P1: 步骤失败、性能异常
    ├─ 检测 P2: 低分报告、部署失败
    └─ 生成 alerts-YYYY-MM-DD.json
    ↓
多渠道分发 (可选)
    ├─ Slack 实时通知
    └─ 邮件汇总通知
```

### 告警级别

| 级别 | 触发条件 | 推送方式 | 示例 |
|------|--------|--------|------|
| 🚨 P0 (CRITICAL) | 系统完全失败 | Slack 立即 | Pipeline Failed |
| ⚠️ P1 (HIGH) | 步骤失败、性能↓50% | Slack 立即 | Step 2 Failed |
| ⏱️ P2 (MEDIUM) | 低分报告、部署失败 | 邮件汇总 | Low Scores |

---

## 🚀 快速启动

### 第 1 步：验证系统已安装

```bash
# 检查新增文件
ls -la /Users/igg/.claude/reports/alert_manager.py
ls -la /Users/igg/.claude/reports/slack_notifier.py
ls -la /Users/igg/.claude/reports/email_notifier.py

# 检查配置已更新
grep "ALERT_CONFIG" /Users/igg/.claude/reports/config.py
```

### 第 2 步：运行测试（基础模式，不发送通知）

```bash
# 测试告警分析
python3 /Users/igg/.claude/reports/alert_manager.py \
    --status-json /Users/igg/.claude/reports/status.json \
    --output-dir /Users/igg/.claude/logs

# 查看生成的告警文件
cat /Users/igg/.claude/logs/alerts-$(date +%Y-%m-%d).json | jq .
```

### 第 3 步：启用 Slack 通知（可选）

```bash
# 1. 在 Slack 工作区创建 Incoming Webhook
#    访问: https://api.slack.com/apps
#    New App → From scratch → Create App
#    Incoming Webhooks → Add New Webhook to Workspace
#    选择接收告警的频道

# 2. 保存 Webhook URL
echo "https://hooks.slack.com/services/YOUR/WEBHOOK/URL" > ~/.alpha_hive_slack_webhook
chmod 600 ~/.alpha_hive_slack_webhook

# 3. 在 config.py 启用 Slack
#    ALERT_CONFIG['slack_enabled'] = True

# 4. 测试发送
python3 /Users/igg/.claude/reports/slack_notifier.py "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### 第 4 步：启用邮件通知（可选）

```bash
# 1. 在 config.py 配置邮件
#    ALERT_CONFIG['email_enabled'] = True
#    ALERT_CONFIG['email_config'] = {
#        'smtp_server': 'smtp.gmail.com',
#        'smtp_port': 587,
#        'sender_email': 'your-email@gmail.com',
#        'sender_password': 'your-app-password',  # 不是账户密码！
#        'recipient_emails': ['your-email@gmail.com'],
#        'use_tls': True
#    }

# 2. 获取 Gmail 应用密码
#    - 启用两步验证: https://myaccount.google.com/security
#    - 生成应用密码: https://myaccount.google.com/apppasswords
#    - 使用该密码替换 sender_password
```

### 第 5 步：在编排脚本中启用（自动运行）

编排脚本现已包含 Step 6，自动执行告警分析：

```bash
# 手动测试完整流程（含告警）
bash /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh

# 查看完整日志
tail -50 /Users/igg/.claude/logs/orchestrator-$(date +%Y-%m-%d).log
```

---

## 📝 文件说明

### alert_manager.py (12KB)

**职责**: 中央告警管理器

```python
# 用法 1: 分析并保存告警
analyzer = AlertAnalyzer()
alerts = analyzer.analyze(Path("status.json"))
analyzer.save_alerts(Path("alerts.json"))

# 用法 2: 从命令行
python3 alert_manager.py --status-json status.json --output-dir ./logs
```

**检测规则**:
- P0: status == 'failed'
- P1: 任何 step.status == 'failed'
- P1: 执行时间 > 基线的 150%
- P1: 无报告文件
- P2: 平均分数 < 6.0
- P2: GitHub 部署失败

### slack_notifier.py (5.5KB)

**职责**: Slack 消息推送

```python
# 用法
notifier = SlackNotifier(webhook_url)
notifier.send(alert)

# 或命令行测试
python3 slack_notifier.py "https://hooks.slack.com/services/..."
```

**消息格式**: Slack Block Kit，包含：
- 告警级别 + 彩色标识
- 详细信息表格
- 时间戳和标签

### email_notifier.py (9.6KB)

**职责**: 邮件通知 + 汇总

```python
# 用法
notifier = EmailNotifier(config)
notifier.send(alert)  # P0/P1 立即发送
notifier.alert_queue  # P2 排队等待

notifier.send_digest()  # 汇总邮件（由定时任务调用）
```

**特性**:
- P0/P1 级别告警立即发送
- P2 级别告警排队汇总
- HTML + 纯文本双格式

---

## 🔧 配置详解

### ALERT_CONFIG

```python
ALERT_CONFIG = {
    # Slack 配置
    "slack_enabled": False,     # 改为 True 启用
    "slack_webhook": None,      # 从文件读取

    # 邮件配置
    "email_enabled": False,     # 改为 True 启用
    "email_config": {...},      # SMTP 配置

    # 告警阈值
    "performance_baseline_seconds": 5.0,
    "performance_degradation_threshold": 1.5,  # 150%

    # 告警规则
    "alert_rules": {
        "enable_critical_alerts": True,
        "enable_high_alerts": True,
        "enable_medium_alerts": True,
        "low_score_threshold": 6.0,
        "no_report_alert": True,
        "deployment_failure_alert": True,
    },

    # 输出
    "save_alerts_json": True,
    "alerts_log_dir": "/Users/igg/.claude/logs",
}
```

---

## 📊 使用场景

### 场景 1: 系统故障立即告警

```
Step 1-5 任一步骤失败
    ↓
AlertAnalyzer 检测到 P1 级别告警
    ↓
SlackNotifier 立即推送到 Slack
    ↓
你在 Slack 收到实时通知 ✨
```

### 场景 2: 性能异常告警

```
执行时间从 5s → 8s (160% 基线)
    ↓
AlertAnalyzer 检测到性能异常
    ↓
SlackNotifier 立即推送
    ↓
你知道需要优化系统 🚀
```

### 场景 3: 低分报告汇总

```
多个 P2 级别告警 (低分、部署失败等)
    ↓
EmailNotifier 排队收集
    ↓
定时任务发送汇总邮件
    ↓
你每天/每周收到一份告警摘要 📧
```

---

## ⚙️ 集成到编排脚本

### 现状

编排脚本现已包含 Step 6（告警分析）：

```bash
# 【Step 6/6】智能告警分析 - 启动
python3 "$REPORTDIR/alert_manager.py" \
    --status-json "$REPORTDIR/status.json" \
    --output-dir "$LOGDIR"
```

### 行为

- ✅ 总是执行（即使之前步骤失败）
- ✅ 不中断主流程（失败也不影响）
- ✅ 生成 alerts-YYYY-MM-DD.json
- ⚠️ 暂不自动分发（除非启用 Slack/邮件）

---

## 🧪 测试清单

- [ ] alert_manager.py 可正常导入
- [ ] 执行告警分析生成 JSON
- [ ] Slack 通知（如启用）成功发送
- [ ] 邮件通知（如启用）成功发送
- [ ] 编排脚本中 Step 6 正常执行
- [ ] 告警文件保存到 /logs

---

## 📈 后续计划

**Week 2**: 性能监控系统
- MetricsCollector (收集指标)
- metrics.db (时序数据库)
- 性能仪表板 (可视化)

**Week 3**: 动态蜂群扩展
- AdaptiveSpawner (自动调整 Agent 数)
- 系统负载监控

**Week 4**: 信息素持久化
- PheromoneRecorder (历史记录)
- 准确率回看 (T+1/T+7/T+30)

---

## 🆘 故障排除

### 问题 1: Slack 通知不工作

```bash
# 检查 webhook 文件
cat ~/.alpha_hive_slack_webhook | head -c 50

# 测试 webhook
python3 slack_notifier.py "your-webhook-url"
```

### 问题 2: 邮件发送失败

```bash
# 检查配置
grep "email_config" config.py

# 验证 Gmail 应用密码
# 不是普通密码，必须是应用密码！
```

### 问题 3: 告警未生成

```bash
# 检查 status.json 是否存在
cat /Users/igg/.claude/reports/status.json | jq .

# 运行手动分析
python3 alert_manager.py --status-json /path/to/status.json
```

---

## 📚 相关文件

- `alert_manager.py` - 核心告警引擎
- `slack_notifier.py` - Slack 集成
- `email_notifier.py` - 邮件集成
- `config.py` - 配置文件（ALERT_CONFIG）
- `alpha-hive-orchestrator.sh` - 编排脚本（Step 6）
- `/logs/alerts-YYYY-MM-DD.json` - 告警日志

---

## 🎯 成功指标

- ✅ 能检测所有 P0 级别故障 (<1秒)
- ✅ P1 级别告警 100% 覆盖
- ✅ 故障发现延迟 < 1 分钟
- ✅ Slack/邮件送达率 > 95%

---

**下一步**: 启用 Slack 或邮件通知，体验实时告警 🔔

