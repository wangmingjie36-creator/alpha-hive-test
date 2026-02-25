#!/bin/bash

# 🐝 Alpha Hive - 实时系统控制脚本
# 管理数据采集、报告生成、定时任务的启动和停止

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

usage() {
    echo "用法: ./run_realtime.sh [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  fetch              采集实时数据"
    echo "  report             生成优化报告"
    echo "  daemon start       启动后台守护进程"
    echo "  daemon stop        停止后台守护进程"
    echo "  daemon status      查看守护进程状态"
    echo "  daemon logs        查看守护进程日志"
    echo "  push               上传到 GitHub"
    echo "  full               执行完整流程（采集+报告+上传）"
    echo "  clean              清理缓存"
    echo "  check              系统健康检查"
    echo ""
    echo "示例:"
    echo "  ./run_realtime.sh fetch"
    echo "  ./run_realtime.sh daemon start"
    echo "  ./run_realtime.sh full"
}

# 采集数据
fetch_data() {
    echo -e "${YELLOW}📊 采集实时数据...${NC}"
    python3 data_fetcher.py
    if [ -f "realtime_metrics.json" ]; then
        echo -e "${GREEN}✅ 数据采集成功${NC}"
    else
        echo -e "${RED}❌ 数据采集失败${NC}"
        return 1
    fi
}

# 生成报告
generate_reports() {
    echo -e "${YELLOW}📝 生成优化报告...${NC}"
    python3 generate_report_with_realtime_data.py
    report_count=$(ls -1 alpha-hive-*-realtime-*.html 2>/dev/null | wc -l)
    if [ $report_count -gt 0 ]; then
        echo -e "${GREEN}✅ 生成了 $report_count 份报告${NC}"
    else
        echo -e "${RED}❌ 报告生成失败${NC}"
        return 1
    fi
}

# 启动后台守护进程
start_daemon() {
    echo -e "${YELLOW}🚀 启动后台守护进程...${NC}"

    # 检查是否已运行
    if pgrep -f "scheduler.py daemon" > /dev/null; then
        echo -e "${YELLOW}⚠️ 守护进程已在运行${NC}"
        return 0
    fi

    # 启动新进程
    nohup python3 scheduler.py daemon > logs/scheduler.log 2>&1 &
    sleep 1

    if pgrep -f "scheduler.py daemon" > /dev/null; then
        pid=$(pgrep -f "scheduler.py daemon" | head -1)
        echo -e "${GREEN}✅ 守护进程已启动 (PID: $pid)${NC}"
    else
        echo -e "${RED}❌ 启动失败${NC}"
        return 1
    fi
}

# 停止后台守护进程
stop_daemon() {
    echo -e "${YELLOW}⏹️ 停止后台守护进程...${NC}"

    if pgrep -f "scheduler.py daemon" > /dev/null; then
        pkill -f "scheduler.py daemon"
        sleep 1

        if ! pgrep -f "scheduler.py daemon" > /dev/null; then
            echo -e "${GREEN}✅ 守护进程已停止${NC}"
        else
            echo -e "${RED}❌ 停止失败${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}ℹ️ 守护进程未运行${NC}"
    fi
}

# 查看守护进程状态
status_daemon() {
    echo -e "${YELLOW}📊 守护进程状态...${NC}"

    if pgrep -f "scheduler.py daemon" > /dev/null; then
        pid=$(pgrep -f "scheduler.py daemon" | head -1)
        echo -e "${GREEN}✅ 运行中 (PID: $pid)${NC}"
        echo ""
        echo "进程信息:"
        ps -p $pid -o pid,user,cpu,%mem,rss,start,time,cmd
    else
        echo -e "${RED}❌ 未运行${NC}"
    fi

    # 显示最后更新时间
    if [ -f "realtime_metrics.json" ]; then
        echo ""
        echo "数据更新时间:"
        python3 -c "
import json
from datetime import datetime
with open('realtime_metrics.json') as f:
    data = json.load(f)
    ts = datetime.fromisoformat(data[list(data.keys())[0]]['timestamp'])
    delta = datetime.now() - ts
    print(f'  {int(delta.total_seconds())}秒前')
" 2>/dev/null || true
    fi
}

# 查看日志
show_logs() {
    echo -e "${YELLOW}📋 实时日志...${NC}"

    if [ -f "logs/scheduler.log" ]; then
        tail -f logs/scheduler.log
    else
        echo -e "${RED}❌ 日志文件不存在${NC}"
        return 1
    fi
}

# 上传到 GitHub
push_to_github() {
    echo -e "${YELLOW}🚀 上传到 GitHub...${NC}"

    git add alpha-hive-*-realtime-*.html realtime_metrics.json 2>/dev/null || true

    if git commit -m "🔄 实时报告更新 - $(date '+%Y-%m-%d %H:%M:%S')" 2>/dev/null; then
        if git push origin main 2>/dev/null; then
            echo -e "${GREEN}✅ 上传成功${NC}"
        else
            echo -e "${RED}❌ 推送失败${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}ℹ️ 没有新的更改${NC}"
    fi
}

# 完整流程
full_pipeline() {
    echo -e "${YELLOW}🔄 执行完整流程...${NC}"
    echo ""

    fetch_data || exit 1
    echo ""

    generate_reports || exit 1
    echo ""

    read -p "是否上传到 GitHub? [y/n]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        push_to_github
    fi

    echo ""
    echo -e "${GREEN}✅ 完整流程执行完毕${NC}"
}

# 清理缓存
clean_cache() {
    echo -e "${YELLOW}🧹 清理缓存...${NC}"

    rm -rf cache/*
    rm -f logs/*

    echo -e "${GREEN}✅ 缓存已清理${NC}"
}

# 系统健康检查
health_check() {
    echo -e "${YELLOW}🏥 系统健康检查...${NC}"
    echo ""

    # 检查文件
    echo "📁 文件检查:"
    for file in config.py data_fetcher.py generate_report_with_realtime_data.py scheduler.py; do
        if [ -f "$file" ]; then
            echo "  ✅ $file"
        else
            echo "  ❌ $file"
        fi
    done

    echo ""
    echo "📊 数据检查:"
    if [ -f "realtime_metrics.json" ]; then
        echo "  ✅ realtime_metrics.json 存在"
        python3 -c "
import json
with open('realtime_metrics.json') as f:
    data = json.load(f)
    print(f'     包含 {len(data)} 个标的')
    for ticker in data:
        print(f'     • {ticker}')
" 2>/dev/null || true
    else
        echo "  ❌ realtime_metrics.json 不存在"
    fi

    echo ""
    echo "📝 报告检查:"
    report_count=$(ls -1 alpha-hive-*-realtime-*.html 2>/dev/null | wc -l)
    echo "  共 $report_count 份报告"

    echo ""
    echo "🔄 守护进程检查:"
    if pgrep -f "scheduler.py daemon" > /dev/null; then
        echo "  ✅ 运行中"
    else
        echo "  ❌ 未运行"
    fi

    echo ""
    echo -e "${GREEN}✅ 检查完毕${NC}"
}

# 主程序
if [ $# -eq 0 ]; then
    usage
    exit 0
fi

case "$1" in
    fetch)
        fetch_data
        ;;
    report)
        generate_reports
        ;;
    daemon)
        case "$2" in
            start)
                start_daemon
                ;;
            stop)
                stop_daemon
                ;;
            status)
                status_daemon
                ;;
            logs)
                show_logs
                ;;
            *)
                echo -e "${RED}❌ 未知选项: $2${NC}"
                echo "用法: ./run_realtime.sh daemon [start|stop|status|logs]"
                exit 1
                ;;
        esac
        ;;
    push)
        push_to_github
        ;;
    full)
        full_pipeline
        ;;
    clean)
        clean_cache
        ;;
    check)
        health_check
        ;;
    *)
        echo -e "${RED}❌ 未知命令: $1${NC}"
        usage
        exit 1
        ;;
esac
