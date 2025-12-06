#!/bin/bash

# 引数が空かチェック
if [ -z "$1" ]; then
    echo "Usage: $0 <URL>"
    exit 1
fi

TARGET_URL="$1"
# curlを一度だけ実行し、結果を変数に保存する
header_output=$(curl -sIL "$TARGET_URL")

# チェック対象のヘッダーを配列で定義
headers_to_check=(
  "Strict-Transport-Security"
  "Content-Security-Policy"
  "X-Frame-Options"
  "X-Content-Type-Options"
)

echo "--- Security Header Report for $TARGET_URL ---"

# 配列の各ヘッダーに対してループ処理
for header in "${headers_to_check[@]}"; do

    # 保存したcurlの出力結果からgrepで検索
    # -q オプションでgrep自体の出力は抑制する
    if echo "$header_output" | grep -iq "$header"; then
        echo "✅ Found: $header"
    else
        echo "❌ Not Found: $header"
    fi
    
done

echo "------------------------------------------"
echo "All done!"