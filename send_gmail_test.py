#!/usr/bin/env python3
"""快速 Gmail API 测试脚本"""

import os
import base64
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 导入 Google 库
from google.auth.oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import googleapiclient.discovery

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate():
    """认证并返回 Gmail 服务"""
    creds = None
    token_file = Path.home() / '.alpha_hive_gmail_token.json'
    credentials_file = '/Users/igg/.alpha_hive_gmail_credentials.json'

    # 如果有现存令牌，使用它
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        # 首次需要用户授权
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        creds = flow.run_local_server(port=0)

        # 保存令牌
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return googleapiclient.discovery.build('gmail', 'v1', credentials=creds)

def send_email(service, to_email, subject, html_body):
    """发送邮件"""
    message = MIMEMultipart('alternative')
    message['subject'] = subject
    message['from'] = 'iggissexy0511@gmail.com'
    message['to'] = to_email

    message.attach(MIMEText(html_body, 'html'))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_message = {'raw': raw_message}

    result = service.users().messages().send(userId='me', body=send_message).execute()
    return result

if __name__ == '__main__':
    print("🚀 Gmail API 邮件测试\n")

    try:
        print("1️⃣  认证中...")
        service = authenticate()
        print("   ✅ 认证成功\n")

        print("2️⃣  发送邮件...")
        result = send_email(
            service,
            'iggissexy0511@gmail.com',
            '🎉 [Alpha Hive] Gmail API 测试成功！',
            """
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
                  <h2 style="color: #2c3e50;">🎉 邮件系统已激活！</h2>

                  <div style="background-color: #e8f4f8; padding: 20px; border-left: 4px solid #3498db; margin: 20px 0; border-radius: 5px;">
                    <p style="margin: 0; color: #2c3e50; font-size: 18px;"><strong>✅ 系统状态：正常</strong></p>
                    <hr style="border: none; border-top: 1px solid #3498db; margin: 10px 0;">
                    <p style="margin: 5px 0; color: #555;">🔐 Gmail API 认证：成功</p>
                    <p style="margin: 5px 0; color: #555;">📧 邮件发送：成功</p>
                    <p style="margin: 5px 0; color: #555;">⏰ 时间：2026-02-24</p>
                  </div>

                  <p style="color: #555; font-size: 16px;">
                    恭喜！Alpha Hive 邮件通知系统现已完全正常运行。
                  </p>

                  <p style="color: #999; font-size: 12px; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 15px;">
                    🐝 Alpha Hive 智能告警系统
                  </p>
                </div>
              </body>
            </html>
            """
        )
        print(f"   ✅ 邮件已发送: {result.get('id')}\n")

        print("=" * 60)
        print("✅ ✅ ✅ Gmail API 邮件系统成功！✅ ✅ ✅")
        print("=" * 60)
        print("\n📧 检查你的 Gmail 收件箱！")
        print("   应该收到来自 iggissexy0511@gmail.com 的邮件")

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
