#!/bin/bash

# 🐝 Alpha Hive - 实时数据集成一键部署脚本
# 自动完成所有初始化和配置

set -e  # 任何错误都停止执行

echo "=================================="
echo "🐝 Alpha Hive 实时数据集成部署"
echo "=================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. 检查 Python 版本
echo -e "${YELLOW}[1/7] 检查 Python 版本...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python 版本: $python_version"
echo ""

# 2. 创建必要目录
echo -e "${YELLOW}[2/7] 创建目录结构...${NC}"
mkdir -p cache
mkdir -p logs
mkdir -p backups
echo "✅ 目录已创建: cache/, logs/, backups/"
echo ""

# 3. 安装依赖
echo -e "${YELLOW}[3/7] 安装 Python 依赖...${NC}"
pip3 install -q requests yfinance pytrends beautifulsoup4 2>/dev/null || true
pip3 install -q schedule APScheduler 2>/dev/null || true
echo "✅ 依赖安装完成"
echo ""

# 4. 验证配置文件
echo -e "${YELLOW}[4/7] 验证配置文件...${NC}"
if [ -f "config.py" ]; then
    echo "✅ config.py 存在"
else
    echo -e "${RED}❌ config.py 不存在${NC}"
    exit 1
fi

if [ -f "data_fetcher.py" ]; then
    echo "✅ data_fetcher.py 存在"
else
    echo -e "${RED}❌ data_fetcher.py 不存在${NC}"
    exit 1
fi
echo ""

# 5. 首次数据采集
echo -e "${YELLOW}[5/7] 执行首次数据采集...${NC}"
python3 data_fetcher.py > logs/initial_fetch.log 2>&1
if [ -f "realtime_metrics.json" ]; then
    echo "✅ 数据采集成功"
    echo "📊 数据摘要:"
    python3 -c "
import json
with open('realtime_metrics.json') as f:
    data = json.load(f)
    for ticker in data:
        metrics = data[ticker]['crowding_input']
        print(f'  • {ticker}: StockTwits {metrics[\"stocktwits_messages_per_day\"]:,}/天')
" 2>/dev/null || true
else
    echo -e "${RED}❌ 数据采集失败${NC}"
    exit 1
fi
echo ""

# 6. 生成首个实时报告
echo -e "${YELLOW}[6/7] 生成首个实时报告...${NC}"
python3 generate_report_with_realtime_data.py > logs/initial_report.log 2>&1
report_count=$(ls -1 alpha-hive-*-realtime-*.html 2>/dev/null | wc -l)
if [ $report_count -gt 0 ]; then
    echo "✅ 生成了 $report_count 份实时报告"
    ls -lh alpha-hive-*-realtime-*.html | awk '{print "  • " $9 " (" $5 ")"}'
else
    echo -e "${RED}❌ 报告生成失败${NC}"
    exit 1
fi
echo ""

# 7. 启动定时任务（可选）
echo -e "${YELLOW}[7/7] 配置定时任务...${NC}"
echo ""
echo "选择启动方式："
echo "  1) 后台守护进程（推荐）"
echo "  2) Cron 定时任务"
echo "  3) 跳过自动启动"
echo ""
read -p "请选择 [1-3]: " choice

case $choice in
    1)
        echo "🔄 启动后台守护进程..."
        nohup python3 scheduler.py daemon > logs/scheduler.log 2>&1 &
        sleep 2
        if pgrep -f "scheduler.py" > /dev/null; then
            echo "✅ 后台进程已启动"
            echo "   查看日志: tail -f logs/scheduler.log"
        else
            echo -e "${RED}❌ 启动失败${NC}"
        fi
        ;;
    2)
        echo "🔄 显示 Cron 配置..."
        python3 scheduler.py cron | head -30
        echo ""
        echo "请手动执行: crontab -e"
        ;;
    3)
        echo "⏭️ 跳过自动启动"
        echo "后续可以运行: python3 scheduler.py daemon"
        ;;
esac

echo ""
echo "=================================="
echo "✅ 部署完成！"
echo "=================================="
echo ""
echo "📊 生成的文件："
echo "  • realtime_metrics.json - 实时数据"
echo "  • alpha-hive-*.html - 优化报告"
echo ""
echo "📚 后续步骤："
echo "  1. 查看报告: open alpha-hive-NVDA-realtime-*.html"
echo "  2. 查看数据: cat realtime_metrics.json | jq '.NVDA'"
echo "  3. 查看日志: tail -f logs/scheduler.log"
echo ""
echo "📖 详细文档: cat REALTIME-INTEGRATION-SUMMARY.md"
echo ""
