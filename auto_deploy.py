#!/usr/bin/env python3
"""
🚀 Alpha Hive 自动部署脚本
自动推送当日报告到 GitHub Pages 仓库
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class AlphaHiveDeployer:
    """自动部署管理器"""

    def __init__(self):
        self.report_dir = Path("/Users/igg/.claude/reports")
        self.token_file = Path.home() / ".alpha_hive_github_token"
        self.status_file = self.report_dir / "status.json"
        self.repo_url = "https://github.com/wangmingjie36-creator/alpha-hive-deploy"
        self.timestamp = datetime.now()
        self.date_str = self.timestamp.strftime("%Y-%m-%d")

    def read_github_token(self) -> Optional[str]:
        """从文件安全读取 GitHub Token"""
        if not self.token_file.exists():
            print(f"❌ 错误：GitHub token 文件不存在: {self.token_file}")
            print("   请执行以下命令设置 token:")
            print("   echo 'ghp_your_token_here' > ~/.alpha_hive_github_token")
            print("   chmod 600 ~/.alpha_hive_github_token")
            return None

        try:
            with open(self.token_file, 'r') as f:
                token = f.read().strip()
            if not token:
                print("❌ 错误：GitHub token 为空")
                return None
            return token
        except PermissionError:
            print(f"❌ 错误：无权读取 token 文件，请检查权限")
            return None

    def get_today_modified_files(self) -> List[str]:
        """获取今天修改的报告文件"""
        modified_files = []

        patterns = [
            f"alpha-hive-daily-{self.date_str}.*",
            f"alpha-hive-thread-{self.date_str}.*",
            f"alpha-hive-*-ml-enhanced-{self.date_str}.*",
            f"analysis-*-ml-{self.date_str}.*",
        ]

        for pattern in patterns:
            for file_path in self.report_dir.glob(pattern):
                if file_path.is_file():
                    modified_files.append(file_path.name)

        return modified_files

    def extract_top_opportunity(self) -> Dict[str, str]:
        """从日报中提取 Top 机会信息"""
        json_file = self.report_dir / f"alpha-hive-daily-{self.date_str}.json"

        if not json_file.exists():
            return {"ticker": "UNKNOWN", "score": "0.0"}

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                report = json.load(f)

            opportunities = report.get("opportunities", [])
            if opportunities:
                top = opportunities[0]
                return {
                    "ticker": top.get("ticker", "UNKNOWN"),
                    "score": str(top.get("opp_score", "0.0"))
                }
        except Exception as e:
            print(f"⚠️  提取报告信息失败: {e}")

        return {"ticker": "UNKNOWN", "score": "0.0"}

    def push_to_github(self, files: List[str], token: str) -> Dict[str, any]:
        """推送文件到 GitHub"""
        result = {
            "success": False,
            "message": "",
            "url": None,
            "commit_sha": None
        }

        if not files:
            result["message"] = "没有需要推送的文件"
            return result

        # 切换到报告目录
        os.chdir(self.report_dir)

        # 初始化 git（如果需要）
        if not (self.report_dir / ".git").exists():
            print("🔧 初始化 git 仓库...")
            subprocess.run(["git", "init"], capture_output=True)
            subprocess.run([
                "git", "remote", "add", "origin",
                f"https://x-access-token:{token}@github.com/wangmingjie36-creator/alpha-hive-deploy.git"
            ], capture_output=True)
        else:
            # 更新现有的 remote
            subprocess.run(
                ["git", "remote", "set-url", "origin",
                 f"https://x-access-token:{token}@github.com/wangmingjie36-creator/alpha-hive-deploy.git"],
                capture_output=True
            )

        try:
            # 添加文件
            for file in files:
                result_add = subprocess.run(
                    ["git", "add", file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result_add.returncode != 0:
                    print(f"⚠️  无法添加文件 {file}: {result_add.stderr}")

            # 获取 Top 机会信息用于 commit 消息
            top_opp = self.extract_top_opportunity()
            commit_msg = (
                f"📰 Alpha Hive 日报 {self.date_str} | "
                f"{top_opp['ticker']} {top_opp['score']}/10"
            )

            print(f"📤 提交信息：{commit_msg}")

            # 提交
            result_commit = subprocess.run(
                ["git", "commit", "-m", commit_msg, "--allow-empty"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result_commit.returncode != 0:
                if "nothing to commit" not in result_commit.stdout.lower():
                    print(f"⚠️  提交失败: {result_commit.stderr}")
                    result["message"] = f"提交失败: {result_commit.stderr}"
                    return result

            # 推送
            print("🚀 推送到 GitHub...")
            result_push = subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result_push.returncode == 0:
                result["success"] = True
                result["message"] = "✅ 推送成功"
                result["url"] = "https://wangmingjie36-creator.github.io/alpha-hive-deploy/"
                print(f"✅ 推送成功")
                print(f"📄 报告地址: {result['url']}")
            else:
                # 如果主分支不存在，尝试创建
                if "Repository not found" in result_push.stderr or "fatal" in result_push.stderr:
                    print("🔄 仓库初始化中，尝试创建主分支...")
                    result_branch = subprocess.run(
                        ["git", "branch", "-M", "main"],
                        capture_output=True,
                        text=True
                    )
                    result_push_retry = subprocess.run(
                        ["git", "push", "-u", "origin", "main", "--force"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if result_push_retry.returncode == 0:
                        result["success"] = True
                        result["message"] = "✅ 推送成功（首次初始化）"
                        result["url"] = "https://wangmingjie36-creator.github.io/alpha-hive-deploy/"
                        print("✅ 仓库初始化完成")
                    else:
                        result["message"] = f"推送失败: {result_push_retry.stderr}"
                else:
                    result["message"] = f"推送失败: {result_push.stderr}"

        except subprocess.TimeoutExpired:
            result["message"] = "操作超时"
            print("❌ 操作超时")
        except Exception as e:
            result["message"] = f"异常: {str(e)}"
            print(f"❌ 异常: {e}")

        return result

    def update_status_json(self, deploy_result: Dict) -> None:
        """更新 status.json 文件"""
        status = {}

        # 读取现有状态
        if self.status_file.exists():
            try:
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    status = json.load(f)
            except Exception as e:
                print(f"⚠️  读取状态文件失败: {e}")

        # 更新部署信息
        status["last_run"] = self.timestamp.isoformat()
        status["last_run_date"] = self.date_str
        status["deploy_status"] = "success" if deploy_result["success"] else "failed"
        status["deploy_message"] = deploy_result["message"]
        status["deploy_url"] = deploy_result["url"]

        # 写入
        try:
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(status, f, ensure_ascii=False, indent=2)
            print(f"✅ 状态已更新: {self.status_file}")
        except Exception as e:
            print(f"⚠️  更新状态失败: {e}")

    def run(self) -> bool:
        """执行部署流程"""
        print("\n" + "=" * 70)
        print("🚀 Alpha Hive 自动部署")
        print("=" * 70)

        # 1. 读取 Token
        print("\n[1/4] 读取 GitHub Token...")
        token = self.read_github_token()
        if not token:
            return False

        print("✅ Token 已读取")

        # 2. 获取需要推送的文件
        print("\n[2/4] 扫描当日报告...")
        files = self.get_today_modified_files()
        if not files:
            print("⚠️  没有今天生成的报告文件")
            print("   期望文件模式:")
            print(f"   - alpha-hive-daily-{self.date_str}.*")
            print(f"   - alpha-hive-thread-{self.date_str}.*")
            return False

        print(f"✅ 找到 {len(files)} 个文件：")
        for f in files[:5]:
            print(f"   - {f}")
        if len(files) > 5:
            print(f"   ... 及其他 {len(files) - 5} 个文件")

        # 3. 推送到 GitHub
        print("\n[3/4] 推送到 GitHub...")
        deploy_result = self.push_to_github(files, token)

        # 4. 更新状态
        print("\n[4/4] 更新状态...")
        self.update_status_json(deploy_result)

        print("\n" + "=" * 70)
        if deploy_result["success"]:
            print("✅ 部署完成！")
            if deploy_result["url"]:
                print(f"📄 报告地址: {deploy_result['url']}")
        else:
            print("⚠️  部署遇到问题，但流程已继续")
            if deploy_result["message"]:
                print(f"   信息: {deploy_result['message']}")

        print("=" * 70)

        return deploy_result["success"]


def main():
    """主入口"""
    deployer = AlphaHiveDeployer()
    deployer.run()


if __name__ == "__main__":
    main()
