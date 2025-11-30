#!/bin/bash

# 1. 最初の引数が空かどうかを確認
if [ -z "$1" ]; then
    echo "Usage: $0 <URL>"
    exit 1
fi

# 2. コマンドを実行し、ヘッダーを検索
#    - URLには"$1"を使用
#    - grep -i で大文字小文字を区別しない
#    - &> /dev/null でパイプラインからの出力を抑制
curl -sIL "$1" | grep -i "X-Frame-Options" &> /dev/null

# 3. パイプラインの終了ステータスを確認
if [ $? -eq 0 ]; then
    echo "The X-Frame-Options header was found."
else
    echo "The X-Frame-Options header was not found."
fi