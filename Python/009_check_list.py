#!/usr/bin/env python3
import requests

# 読み込むファイル名を指定
url_file = "urls.txt"

print(f"--- Checking URLs from {url_file} ---")

try:
    # 'with open' でファイルを安全に読み込む
    with open(url_file, 'r') as f:
        # ファイル内の各行に対してループ処理
        for line in f:
            # 行の前後にある不要な改行やスペースを削除
            url = line.strip()

            # 空行やコメント行はスキップ
            if not url or url.startswith('#'):
                continue

            try:
                # 各URLに対してリクエストを送信
                response = requests.get(url, timeout=5)
                print(f"✅ OK ({response.status_code}): {url}")

            except requests.exceptions.RequestException as e:
                # 接続に失敗した場合、エラーの1行目だけを表示
                error_message = str(e).split('\n')[0]
                print(f"❌ ERROR: {url} ({error_message})")

except FileNotFoundError:
    # urls.txtが見つからなかった場合のエラー処理
    print(f"エラー: ファイル '{url_file}' が見つかりません。")

print("--- All checks complete ---")