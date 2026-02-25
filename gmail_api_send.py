#!/usr/bin/env python3
"""
使用 Gmail API 发送邮件
（需要先运行 authorize_gmail.py 完成授权）
"""

import sys
import base64
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 添加库路径
sys.path.insert(0, '/Users/igg/Library/Python/3.9/lib/python/site-packages')

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import googleapiclient.discovery

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailSender:
    def __init__(self):
        self.token_file = Path.home() / '.alpha_hive_gmail_token.json'
        self.service = None
        self._load_service()

    def _load_service(self):
        """加载 Gmail 服务（使用已保存的令牌）"""
        if not self.token_file.exists():
            raise FileNotFoundError(
                f"授权令牌不存在。请先运行：\n"
                f"  python3 /Users/igg/.claude/reports/authorize_gmail.py"
            )

        try:
            creds = Credentials.from_authorized_user_file(str(self.token_file), SCOPES)

            # 如果令牌过期，刷新它
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # 保存刷新后的令牌
                with open(self.token_file, 'w') as token:
                    token.write(creds.to_json())

            self.service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)
            print("✅ Gmail API 连接成功")

        except Exception as e:
            print(f"❌ 连接失败: {e}")
            raise

    def send(self, to_email, subject, html_body):
        """发送邮件"""
        try:
            # 创建邮件
            message = MIMEMultipart('alternative')
            message['subject'] = subject
            message['from'] = 'iggissexy0511@gmail.com'
            message['to'] = to_email

            message.attach(MIMEText(html_body, 'html'))

            # 编码
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = {'raw': raw_message}

            # 发送
            result = self.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()

            return {
                'success': True,
                'message_id': result.get('id')
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def main():
    print("\n🚀 Gmail API 邮件发送测试\n")

    try:
        print("1️⃣  连接 Gmail API...")
        sender = GmailSender()
        print()

        print("2️⃣  发送测试邮件...")
        result = sender.send(
            'iggissexy0511@gmail.com',
            '🎉 [Alpha Hive] Gmail API 邮件成功！',
            """
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
                  <h2 style="color: #2c3e50;">🎉 邮件系统已激活！</h2>

                  <div style="background-color: #e8f4f8; padding: 20px; border-left: 4px solid #3498db; margin: 20px 0; border-radius: 5px;">
                    <p style="margin: 0; color: #2c3e50; font-size: 18px;"><strong>✅ 系统状态：正常</strong></p>
                    <hr style="border: none; border-top: 1px solid #3498db; margin: 10px 0;">
                    <p style="margin: 5px 0; color: #555;">✅ Gmail API 认证：成功</p>
                    <p style="margin: 5px 0; color: #555;">✅ 邮件发送：成功</p>
                    <p style="margin: 5px 0; color: #555;">✅ 系统时间：2026-02-24</p>
                  </div>

                  <p style="color: #555; font-size: 16px;">
                    恭喜！Alpha Hive 邮件通知系统现已完全正常运行。
                  </p>

                  <p style="color: #555;">
                    你现在可以：<br>
                    ✅ 运行编排脚本接收实时邮件告警<br>
                    ✅ 自动监控系统状态<br>
                    ✅ 获取 P0/P1 级别的紧急通知
                  </p>

                  <p style="color: #999; font-size: 12px; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 15px;">
                    🐝 Alpha Hive 智能告警系统<br>
                    去中心化投资研究 Agent 集体
                  </p>
                </div>
              </body>
            </html>
            """
        )

        if result['success']:
            print(f"   ✅ 邮件已发送: {result['message_id']}")
            print()
            print("=" * 60)
            print("✅ ✅ ✅ 邮件系统成功激活！✅ ✅ ✅")
            print("=" * 60)
            print()
            print("📧 请检查你的 Gmail 收件箱！")
            print()
            print("下一步：运行完整的编排流程")
            print("  bash /Users/igg/.claude/scripts/alpha-hive-orchestrator.sh")
        else:
            print(f"   ❌ 发送失败: {result['error']}")

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
