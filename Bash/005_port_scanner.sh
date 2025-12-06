#!/bin/bash

# --- ポートスキャンツール ---

# 引数が1つもなければ使い方を表示して終了
if [ $# -eq 0 ]; then
  echo "使い方: $0 <IPアドレス> <ポート1> <ポート2> ..."
  exit 1
fi

# 1. 最初の引数をIPアドレスとして変数に保存
IP_ADDR="$1"
# 2. 引数リストを一つずらす（IPアドレスをリストから消す）
shift

# --- レポート出力開始 ---
echo "" # 見やすさのための改行
echo "--- Port Scan Report for $IP_ADDR ---"

# 3. 残りの全引数（ポート番号）に対してループ処理
for PortNum in $@
do
  # 4. ncコマンドでポートチェック（-vの出力は不要なため捨てる）
  nc -zvw1 "$IP_ADDR" "$PortNum" &> /dev/null

  # 5. 終了ステータスで結果を判定
  if [ $? -eq 0 ]; then
    echo "  Port $PortNum : Open"
  else
    echo "  Port $PortNum : Closed"
  fi
done

echo "------------------------------------"
echo "" # 見やすさのための改行