"""
🐝 Gmail API 邮件通知模块
使用 Google Gmail API 发送邮件告警（比 SMTP 更可靠）
"""

import os
import json
import base64
from pathlib import Path
from typing import List, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as GoogleCredentials
from google.auth.oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery as discovery


class GmailAPINotifier:
    """使用 Gmail API 发送邮件"""
    
    def __init__(self, credentials_file: str):
        """初始化 Gmail API 通知器"""
        self.credentials_file = credentials_file
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """使用凭证文件进行身份验证"""
        credentials_path = Path(self.credentials_file)
        
        if not credentials_path.exists():
            raise FileNotFoundError(f"凭证文件不存在: {self.credentials_file}")
        
        # Gmail API 需要的权限
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        
        try:
            # 检查是否已有授权的令牌
            token_file = Path.home() / '.alpha_hive_gmail_token.json'

            if token_file.exists():
                # 使用现有令牌
                creds = GoogleCredentials.from_authorized_user_file(str(token_file), SCOPES)
                if not creds.valid:
                    if creds.expired and creds.refresh_token:
                        creds.refresh(Request())
            else:
                # 首次授权 - 需要用户交互
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)

                # 保存令牌供后续使用
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
            
            # 创建 Gmail API 服务
            self.service = discovery.build('gmail', 'v1', credentials=creds)
            print("✅ Gmail API 认证成功")
            
        except Exception as e:
            print(f"❌ 认证失败: {e}")
            raise
    
    def send(self, sender_email: str, recipient_emails: List[str], 
             subject: str, html_body: str, text_body: str = None) -> Dict[str, Any]:
        """
        发送邮件
        
        Args:
            sender_email: 发件人邮箱
            recipient_emails: 收件人列表
            subject: 邮件主题
            html_body: HTML 格式邮件内容
            text_body: 纯文本格式邮件内容（可选）
        
        Returns:
            发送结果字典
        """
        try:
            # 创建邮件
            message = MIMEMultipart('alternative')
            message['subject'] = subject
            message['from'] = sender_email
            message['to'] = ', '.join(recipient_emails)
            
            # 添加纯文本部分（如果提供）
            if text_body:
                message.attach(MIMEText(text_body, 'plain'))
            
            # 添加 HTML 部分
            message.attach(MIMEText(html_body, 'html'))
            
            # 编码邮件
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # 发送
            send_message = {
                'raw': raw_message
            }
            
            result = self.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()
            
            print(f"✅ 邮件已发送: {result.get('id')}")
            return {
                'success': True,
                'message_id': result.get('id'),
                'to': recipient_emails
            }
            
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return {
                'success': False,
                'error': str(e)
            }


def send_alert_email(alert: Dict, config: Dict) -> Dict[str, Any]:
    """
    发送告警邮件
    
    Args:
        alert: 告警信息字典
        config: 邮件配置
    
    Returns:
        发送结果
    """
    try:
        notifier = GmailAPINotifier(config['credentials_file'])
        
        # 构建邮件内容
        subject = f"[{alert.get('level', 'INFO')}] {alert.get('message', '告警')}"
        
        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f5f5f5;">
            <div style="background-color: white; padding: 20px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
              <h2 style="color: #2c3e50;">🐝 Alpha Hive 告警</h2>
              <p><strong>级别:</strong> {alert.get('level')}</p>
              <p><strong>消息:</strong> {alert.get('message')}</p>
              <p><strong>时间:</strong> {alert.get('timestamp')}</p>
              
              <div style="background-color: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px;">
                <h3>详情:</h3>
                <pre>{json.dumps(alert.get('details', {}), ensure_ascii=False, indent=2)}</pre>
              </div>
              
              <p style="color: #999; font-size: 12px;">
                Alpha Hive 智能告警系统
              </p>
            </div>
          </body>
        </html>
        """
        
        # 发送
        result = notifier.send(
            sender_email=config['sender_email'],
            recipient_emails=config['recipient_emails'],
            subject=subject,
            html_body=html_body
        )
        
        return result
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    # 测试
    print("🧪 Gmail API 邮件通知测试\n")
    
    config = {
        'credentials_file': '/Users/igg/.alpha_hive_gmail_credentials.json',
        'sender_email': 'iggissexy0511@gmail.com',
        'recipient_emails': ['iggissexy0511@gmail.com']
    }
    
    test_alert = {
        'level': 'MEDIUM',
        'message': 'Gmail API 连接测试',
        'timestamp': '2026-02-24T12:00:00',
        'details': {'test': 'This is a test alert using Gmail API'}
    }
    
    result = send_alert_email(test_alert, config)
    print(f"\n发送结果: {result}")

