#!/usr/bin/env python3
import requests

# チェックしたいURL
url = "https://www.google.com"

try:
    # GETリクエストを送信 (タイムアウトを5秒に設定)
    response = requests.get(url, timeout=5)

    # ステータスコードを表示
    print(f"Status code for {url}: {response.status_code}")

except requests.exceptions.RequestException as e:
    # タイムアウトや名前解決エラーなど、接続に関するエラーを処理
    print(f"Error checking {url}: {e}")