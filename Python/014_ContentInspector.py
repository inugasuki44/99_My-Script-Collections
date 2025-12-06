#!/usr/bin/env python3

  

import argparse

import requests # HTTPリクエストを行うためのライブラリ

  

# 1. ArgumentParserオブジェクトの作成

# 説明文は--helpオプション実行時に表示されます

parser = argparse.ArgumentParser(description="指定されたURLのコンテンツから特定のキーワードを検索するツールです。")

  

# 2. 必要な引数を追加

# 'url'と'keyword'は位置引数として必須

parser.add_argument('url', help='チェック対象のURLを指定します (例: https://example.com)')

parser.add_argument('keyword', help='ページ内で検索するキーワードを指定します')

  

# 3. コマンドライン引数を解析

args = parser.parse_args()

  

print(f"\n-> Fetching content from {args.url}...")

  

try:

    # 4. 指定されたURLにGETリクエストを送信

    # タイムアウトを設定し、応答がない場合に長時間待たないようにする

    response = requests.get(args.url, timeout=10)

    # 5. HTTPステータスコードがエラー（4xx, 5xx）だった場合に例外を発生させる

    response.raise_for_status()

  

    print(f"-> Searching for the keyword '{args.keyword}'...")

  

    # 6. レスポンスのHTMLテキスト内にキーワードが存在するかチェック

    if args.keyword in response.text:

        print(f"\n✅ Found the keyword '{args.keyword}'.")

    else:

        print(f"\n❌ Did not find the keyword '{args.keyword}'.")

  

except requests.exceptions.RequestException as e:

    # 7. リクエスト中に発生したあらゆるエラー（接続エラー、タイムアウト、HTTPエラーなど）を捕捉

    print(f"\nAn error occurred: {e}")