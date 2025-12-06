#!/usr/bin/env python3
# this is "link_extractor.py"

import argparse
import requests
from bs4 import BeautifulSoup

# 1. ArgumentParserオブジェクトの作成
parser = argparse.ArgumentParser(description="Extracts all links from a given URL.")

# 2. 必要な引数を追加
parser.add_argument("url", help="The URL to extract links from.")

# 3. コマンドライン引数を解析
args = parser.parse_args()

print(f"\n-> Fetching content from {args.url}....")

try:
    # 4. GETリクエストを送信
    response = requests.get(args.url, timeout=10)
    
    # 5. まずHTTPエラーがないかを確認
    response.raise_for_status()
    
    # 6. レスポンスのHTMLコンテンツをBeautifulSoupオブジェクトに変換
    html_content = response.text
    soup = BeautifulSoup(html_content, "lxml")
    
    # 7. 'a'タグをすべて見つける
    all_links = soup.find_all("a")

    print(f"-> Extracting links...")
    
    # 8. 見つかった各リンクから'href'属性を抽出して表示
    for link in all_links:
        href = link.get("href")
        if href: # href属性が存在する場合のみ表示
            print(href)

    print(f"\nFound {len(all_links)} links.")

except requests.exceptions.RequestException as e :
    print(f"\nAn Error occured: {e}")

print(f"All done!")
