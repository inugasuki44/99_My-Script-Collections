#!/usr/bin/env python3
# post_sender.py

import requests
import json

target_url = "https://httpbin.org/post"

# POSTリクエストで送信するデータ
form_data = {
    'user': "inugasuki44",
    'password': "nekomosuki"
}

print(f"--- Sending POST request to {target_url} ---")

try:
    # `requests.post`を使い、`data`引数にデータを渡す
    response = requests.post(target_url, data=form_data)
    
    # 4xx/5xxエラーが発生した場合に例外を発生させる
    response.raise_for_status()

    # レスポンスがJSON形式であることを想定し、Pythonの辞書に変換
    data = response.json()

    # 読みやすいように整形して表示
    print("\n--- Server Response ---")
    print(json.dumps(data, indent=2))

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")