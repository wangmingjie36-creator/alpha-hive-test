# 🐝 Tradier API 集成指南

**更新时间**: 2026-02-24
**状态**: ✅ 完全实现，支持实时数据

---

## 📋 快速概览

Alpha Hive 现已支持 **Tradier API** 作为期权数据的主要来源，具有以下特性：

| 特性 | 说明 |
|------|------|
| **多源容错** | Tradier API → yfinance → 样本数据 |
| **自动切换** | 无缝降级，用户无感知 |
| **重试机制** | 指数退避重试，处理速率限制 |
| **环境支持** | 沙箱（测试）和生产环境 |
| **权限管理** | Token 安全存储（.env 文件权限 600） |

---

## 🚀 快速开始（5 分钟）

### 1️⃣ 获取 Tradier API Token

**Step 1: 注册开发者账户**
```
访问：https://tradier.com/developer
选择：Free Tier（免费开发者账户）
```

**Step 2: 创建应用**
```
1. 登录后进入 Dashboard
2. 点击 "Create New Application"
3. 填写应用名称（如 "Alpha Hive"）
4. 选择 "API Only"
5. 同意条款并创建
```

**Step 3: 获取 Token**
```
1. 进入应用设置
2. 找到 "Sandbox Token" 或 "Access Token"
3. 复制完整的 Token 字符串
   示例：Bearer_xxxxxxxxxxxxxxxxxxxx（通常 > 100 字符）
```

**Step 4: 选择环境**
- **Sandbox** (推荐): 用于测试，无需资金
- **Production**: 需要真实账户和资金

### 2️⃣ 配置 Token

#### 方法 A: 交互式配置（推荐）
```bash
cd /Users/igg/.claude/reports
python3 setup_tradier.py
```

按照提示：
1. 选择环境（1=沙箱，2=生产）
2. 粘贴您的 API Token
3. 选择保存方式（1=环境变量，2=.env 文件）

#### 方法 B: 手动环境变量
```bash
export TRADIER_API_TOKEN="your_token_here"
export TRADIER_ENV="sandbox"
export TRADIER_BASE_URL="https://sandbox.tradier.com"
```

#### 方法 C: .env 文件
创建 `~/.claude/.env.tradier`:
```
TRADIER_ENV=sandbox
TRADIER_BASE_URL=https://sandbox.tradier.com
TRADIER_API_TOKEN=your_token_here
```

**安全提示**: 文件权限自动设置为 600（仅所有者可读写）

### 3️⃣ 验证配置
```bash
python3 test_tradier_integration.py
```

输出示例：
```
✅ PASS - 环境设置
✅ PASS - 模块导入
✅ PASS - Tradier API 连接
✅ PASS - OptionsAgent 功能
...
总计: ✅ 8 | ❌ 0 | ⏭️  0
```

---

## 📊 使用示例

### 基础使用

```python
from options_analyzer import OptionsAgent

# 创建 Agent
agent = OptionsAgent()

# 分析单个标的（自动使用 Tradier API 或容错备用源）
result = agent.analyze('NVDA', stock_price=145.0)

# 查看结果
print(f"Options Score: {result['options_score']}/10")
print(f"IV Rank: {result['iv_rank']}")
print(f"P/C Ratio: {result['put_call_ratio']}")
print(f"Data Source: {result.get('source', 'yfinance')}")
```

### 在完整分析中使用

```python
from advanced_analyzer import AdvancedAnalyzer
import json

# 加载市场数据
with open('realtime_metrics.json') as f:
    metrics = json.load(f)

# 生成完整分析（自动包含期权分析）
analyzer = AdvancedAnalyzer()
analysis = analyzer.generate_comprehensive_analysis('NVDA', metrics['NVDA'])

# 访问期权分析结果
options = analysis['options_analysis']
print(f"Options Score: {options['options_score']}")
print(f"Source: {options.get('source', 'Unknown')}")
```

### 批量分析

```python
from options_analyzer import OptionsAgent

agent = OptionsAgent()
tickers = ['NVDA', 'TSLA', 'AMD', 'MSFT']

for ticker in tickers:
    result = agent.analyze(ticker)
    print(f"{ticker}: Score={result['options_score']}, Flow={result['flow_direction']}")
```

---

## 🔧 配置详解

### 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `TRADIER_API_TOKEN` | **必需** - Tradier API Token | `Bearer_xxxx...` |
| `TRADIER_ENV` | 环境选择 | `sandbox` 或 `production` |
| `TRADIER_BASE_URL` | API 基础 URL | `https://sandbox.tradier.com` |

### 配置文件 (config.py)

```python
API_KEYS["TRADIER"] = {
    "environment": "sandbox",
    "base_url": "https://sandbox.tradier.com",
    "timeout": 10,              # 请求超时（秒）
    "max_retries": 3,           # 最大重试次数
    "backoff_factor": 1.0,      # 重试退避倍数
}
```

---

## 🌐 Tradier API 端点

Alpha Hive 使用的 Tradier API 端点：

| 端点 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/v1/markets/options/chains` | GET | 获取期权链 | `symbol`, `expiration`, `greeks` |
| `/v1/markets/options/expirations` | GET | 获取到期日 | `symbol` |
| `/v1/markets/quotes` | GET | 获取行情 | `symbols` |
| `/v1/user/profile` | GET | 获取账户信息 | - |

**注**: 其他 API 端点（交易、订单等）不在 Alpha Hive 范围内

---

## ⚠️ 容错与错误处理

### 自动容错流程

```
┌─────────────────────────────┐
│ 1. 尝试 Tradier API         │
└──────────────┬──────────────┘
               │
        ┌──────▼──────┐
        │ 成功? (200) │
        └──────┬──────┘
               │ ✓ 是
               ▼
        ┌─────────────┐
        │ 返回结果    │
        │ 保存缓存    │
        └─────────────┘
               △
               │ ✗ 否
      ┌────────┴────────┐
      │                 │
┌─────▼─────┐    ┌─────▼──────┐
│ API 错误  │    │ 网络错误   │
│ (401,404) │    │ (连接超时) │
└─────┬─────┘    └─────┬──────┘
      │                │
      └────────┬───────┘
               │
      ┌────────▼──────────┐
      │ 2. 尝试 yfinance  │
      └────────┬──────────┘
               │
        ┌──────▼──────┐
        │ 成功? │
        └──────┬──────┘
               │ ✓ 是
               ▼
        ┌─────────────┐
        │ 返回结果    │
        │ 保存缓存    │
        └─────────────┘
               △
               │ ✗ 否
      ┌────────┴────────┐
      │ 3. 使用样本数据 │
      └─────────────────┘
```

### 常见错误及解决方案

#### 401 Unauthorized
```
错误: API 认证失败 (401)
原因: Token 无效或已过期
解决:
  1. 检查 Token 是否正确复制
  2. 访问 Tradier Dashboard 重新生成 Token
  3. 重新运行 setup_tradier.py
```

#### 429 Too Many Requests
```
错误: API 速率限制 (429)
原因: 请求过于频繁
解决:
  1. 系统自动进行指数退避重试
  2. 建议不要在短时间内分析大量标的
  3. 利用缓存机制（5 分钟 TTL）
```

#### 404 Not Found
```
错误: 资源不存在 (404)
原因: 标的不存在或无期权数据
解决:
  1. 检查股票代码拼写
  2. 确认该股票有期权合约
  3. 使用 yfinance 验证股票数据
```

#### Connection Timeout
```
错误: 连接超时
原因: 网络不稳定或 API 服务器无响应
解决:
  1. 检查网络连接
  2. 系统自动重试（最多 3 次）
  3. 切换到 yfinance 或样本数据
```

---

## 📈 性能指标

### 响应时间

| 数据源 | 首次加载 | 缓存命中 | 备注 |
|-------|--------|--------|------|
| Tradier API | 1-2 秒 | <100ms | 网络依赖 |
| yfinance | 1-3 秒 | <100ms | 更稳定 |
| 样本数据 | <100ms | - | 无网络依赖 |

### 缓存策略

```python
CACHE_CONFIG = {
    "enabled": True,
    "cache_dir": "/Users/igg/.claude/reports/cache",
    "ttl": {
        "tradier": 300,      # 5 分钟
        "yahoo_finance": 300,  # 5 分钟
    }
}
```

**优点**:
- 减少 API 调用
- 加快分析速度
- 降低服务成本

---

## 🔐 安全最佳实践

### Token 管理

✅ **推荐做法**:
- 使用环境变量或 .env 文件
- 文件权限设置为 600
- 不提交 Token 到版本控制
- 定期轮换 Token

❌ **不推荐做法**:
- 将 Token 硬编码到代码
- 发送 Token 通过不加密通道
- 在日志中打印 Token
- 共享 Token 给他人

### .env 文件安全

```bash
# 创建 .env 文件并设置安全权限
echo "TRADIER_API_TOKEN=your_token" > ~/.claude/.env.tradier
chmod 600 ~/.claude/.env.tradier

# 验证权限
ls -la ~/.claude/.env.tradier
# 应该显示: -rw------- (600)
```

### Token 轮换

```bash
# 如需更新 Token
python3 setup_tradier.py
# 选择"重新配置"选项
```

---

## 📊 监控与日志

### 启用调试日志

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("options_analyzer")

# 现在所有 API 调用都会被记录
agent = OptionsAgent()
result = agent.analyze('NVDA')
```

### 检查 API 使用情况

```bash
# 查看最近的 API 调用
tail -f ~/.claude/reports/cache/options_*.json

# 监控 API 请求日志
python3 -c "
import json
from pathlib import Path

cache_dir = Path('/Users/igg/.claude/reports/cache')
for cache_file in cache_dir.glob('options_*.json'):
    print(f'{cache_file.name}: {cache_file.stat().st_mtime}')
"
```

---

## 🧪 测试 & 调试

### 运行完整测试套件

```bash
python3 test_tradier_integration.py
```

测试覆盖：
- ✓ 环境变量检查
- ✓ 模块导入验证
- ✓ API 连接测试
- ✓ OptionsAgent 功能
- ✓ AdvancedAnalyzer 集成
- ✓ HTML 报告生成
- ✓ 容错机制

### 单个测试

```python
# 测试 Tradier API 连接
python3 -c "
from options_analyzer import OptionsDataFetcher

fetcher = OptionsDataFetcher()
if fetcher._has_tradier_token():
    print('✓ Token configured')
    result = fetcher._tradier_api_request(
        '/v1/markets/options/expirations',
        params={'symbol': 'NVDA'}
    )
    print(result)
else:
    print('✗ Token not configured')
"

# 测试 OptionsAgent
python3 -c "
from options_analyzer import OptionsAgent

agent = OptionsAgent()
result = agent.analyze('NVDA')
print(f'Source: {result.get(\"source\")}')
print(f'Options Score: {result[\"options_score\"]}')
"
```

---

## 📚 相关资源

### Tradier 官方文档
- API 文档: https://tradier.com/api/documentation
- 开发者社区: https://tradier.com/community
- 状态页面: https://status.tradier.com

### Alpha Hive 相关文件
- 核心实现: `options_analyzer.py`
- 集成点: `advanced_analyzer.py`
- 报告生成: `generate_ml_report.py`
- 配置文件: `config.py`

### 快速链接
- 快速开始: `QUICK_START_OPTIONS.md`
- 实现报告: `OPTIONS_AGENT_IMPLEMENTATION.md`
- 测试脚本: `test_tradier_integration.py`
- 配置向导: `setup_tradier.py`

---

## 💡 常见问题

### Q1: 我需要付费 Tradier 账户吗？
**A**: 不需要。Tradier 提供免费开发者账户用于沙箱测试。生产环境需要资金账户。

### Q2: yfinance 和 Tradier API 有什么区别？
**A**:
- Tradier: 官方 API，更可靠，但需要 Token
- yfinance: 开源库，无需认证，但可能不稳定

Alpha Hive 自动选择可用的最佳来源。

### Q3: 如何确保数据隐私？
**A**:
- Token 存储在本地 .env 文件
- 权限设置为 600（仅所有者可读）
- 数据不上传到任何服务器
- 缓存存储在本地

### Q4: 我可以在多台机器上使用同一个 Token 吗？
**A**: 可以，但不推荐。最佳实践是为每台机器生成单独的 Token。

### Q5: API 有速率限制吗？
**A**: 沙箱环境有限制，生产环境取决于账户级别。Alpha Hive 自动处理限制（重试 + 退避）。

---

## 🔄 升级指南

### 从样本数据升级到 Tradier API

**Step 1**: 获取 Tradier API Token（见上文）

**Step 2**: 运行配置向导
```bash
python3 setup_tradier.py
```

**Step 3**: 验证连接
```bash
python3 test_tradier_integration.py
```

**Step 4**: 开始使用
```python
# 代码无需改动，自动使用 Tradier API
agent = OptionsAgent()
result = agent.analyze('NVDA')
```

---

## 📞 技术支持

### 问题排查流程

1. **检查环境变量**
   ```bash
   echo $TRADIER_API_TOKEN  # 应该输出 Token
   ```

2. **运行诊断**
   ```bash
   python3 test_tradier_integration.py
   ```

3. **查看日志**
   ```bash
   tail -50 ~/.claude/reports/cache/options_*.json
   ```

4. **测试单个功能**
   ```bash
   python3 setup_tradier.py  # 重新配置 + 测试
   ```

### 获取帮助

- Tradier 支持: https://tradier.com/support
- Alpha Hive GitHub Issues: [待更新]
- 社区讨论: [待更新]

---

**最后更新**: 2026-02-24
**版本**: 1.0
**状态**: ✅ 完整实现，生产就绪
