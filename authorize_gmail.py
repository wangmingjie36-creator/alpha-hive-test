#!/usr/bin/env python3
"""
Gmail API 授权脚本
第一次运行时会打开浏览器要求授权，之后自动保存令牌
"""

import os
import sys
from pathlib import Path

# 添加库路径
sys.path.insert(0, '/Users/igg/Library/Python/3.9/lib/python/site-packages')

from google.auth.oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authorize_gmail():
    """授权 Gmail 访问"""

    credentials_file = '/Users/igg/.alpha_hive_gmail_credentials.json'
    token_file = Path.home() / '.alpha_hive_gmail_token.json'

    print("🔐 Gmail API 授权流程")
    print("=" * 60)
    print()

    if not Path(credentials_file).exists():
        print(f"❌ 错误：凭证文件不存在")
        print(f"   {credentials_file}")
        return False

    try:
        print("1️⃣  正在启动授权流程...")
        print("   会在浏览器中打开授权页面")
        print()

        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_file,
            SCOPES,
            redirect_uri='http://localhost:8080'
        )

        print("2️⃣  请在浏览器中完成授权...")
        creds = flow.run_local_server(port=8080, open_browser=True)

        print("3️⃣  保存授权令牌...")
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

        print()
        print("=" * 60)
        print("✅ ✅ ✅ 授权成功！✅ ✅ ✅")
        print("=" * 60)
        print()
        print(f"📝 令牌已保存到：{token_file}")
        print()
        print("现在你可以运行邮件测试了：")
        print("  python3 /Users/igg/.claude/reports/gmail_api_send.py")
        print()

        return True

    except Exception as e:
        print(f"❌ 授权失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = authorize_gmail()
    sys.exit(0 if success else 1)
