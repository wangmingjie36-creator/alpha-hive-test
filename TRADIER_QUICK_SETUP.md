# 🚀 Tradier API 快速设置（3 步完成）

**用时**: 5-10 分钟
**难度**: ⭐ 简单

---

## 第 1 步: 获取 API Token (3 分钟)

### 1.1 注册开发者账户

访问 → https://tradier.com/developer

选择：**Free Tier** (免费开发者账户)

### 1.2 创建应用

登录后：
1. Dashboard → "Applications"
2. "Create New Application"
3. 应用名称：`Alpha Hive`
4. 类型：`API Only`
5. 同意条款 → Create

### 1.3 获取 Token

进入应用设置：
1. 找到 **"Sandbox Access Token"** 部分
2. 复制完整的 Token（粘贴板图标）
   - 格式：`Bearer_xxxxxxxxxxxxxxxxxxxxxxxx` (100+ 字符)
3. **保存好** - 只显示一次！

> 如果丢失，可以在应用设置中重新生成

---

## 第 2 步: 配置 Token (1 分钟)

### 方式 A: 自动配置（推荐 ✨）

```bash
cd /Users/igg/.claude/reports
python3 setup_tradier.py
```

按提示操作：
```
选择环境：1 (Sandbox)
粘贴 Token：Bearer_xxxx...
保存方式：1 (环境变量) 或 2 (.env 文件)
```

完成！✅

### 方式 B: 手动配置（如果自动脚本失败）

```bash
# 设置环境变量（临时，重启后失效）
export TRADIER_API_TOKEN="Bearer_xxxx..."
export TRADIER_ENV="sandbox"

# 或者创建 .env 文件（永久）
cat > ~/.claude/.env.tradier << 'EOF'
TRADIER_API_TOKEN=Bearer_xxxx...
TRADIER_ENV=sandbox
EOF

chmod 600 ~/.claude/.env.tradier
```

---

## 第 3 步: 验证配置 (1 分钟)

### 快速验证

```bash
python3 test_tradier_integration.py
```

预期输出：
```
✅ PASS - 环境设置
✅ PASS - 模块导入
✅ PASS - 配置解析
✅ PASS - Tradier API 连接      ← 现在应该成功
✅ PASS - OptionsAgent 功能
...
总计: ✅ 8 | ❌ 0 | ⏭️  0
```

### 测试单个功能

```python
from options_analyzer import OptionsAgent

agent = OptionsAgent()
result = agent.analyze('NVDA')

print(f"Options Score: {result['options_score']}/10")
print(f"Data Source: {result.get('source')}")
# 应该显示 "Tradier API" (如果 Token 有效)
```

---

## ✅ 完成！

现在您可以：

1. **使用 OptionsBee 分析期权**
   ```python
   agent = OptionsAgent()
   result = agent.analyze('TSLA')
   ```

2. **生成包含期权的完整报告**
   ```bash
   python3 generate_ml_report.py
   ```

3. **查看 HTML 中的期权分析章节**
   ```bash
   open analysis-NVDA-ml-*.html
   ```

---

## 🆘 常见问题

### Q: "TRADIER_API_TOKEN 未设置"？
**A**: 重新运行 `python3 setup_tradier.py`

### Q: Token 无效（401 错误）？
**A**:
1. 检查 Token 是否完整复制
2. 访问 Tradier Dashboard 重新生成 Token
3. 确保使用了 **Sandbox Token**（不是 Production）

### Q: 网络超时？
**A**: 系统会自动降级到 yfinance 或样本数据

### Q: 我想切回 yfinance？
**A**: 只需不设置 TRADIER_API_TOKEN，系统自动使用备用源

---

## 📊 验证清单

- [ ] 已访问 https://tradier.com/developer
- [ ] 已注册开发者账户
- [ ] 已创建应用
- [ ] 已复制 Sandbox Token
- [ ] 已运行 `python3 setup_tradier.py`
- [ ] 已运行 `python3 test_tradier_integration.py` 通过
- [ ] 已测试 `agent.analyze('NVDA')` 成功

---

## 📚 更多信息

- **详细指南**: `TRADIER_API_SETUP.md`
- **测试套件**: `test_tradier_integration.py`
- **代码实现**: `options_analyzer.py`
- **配置参考**: `config.py`

---

**🎉 享受 Alpha Hive 的期权分析能力！**
