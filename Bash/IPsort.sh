#!/bin/bash

# --- IPアドレス集計スクリプト (結果をファイルに出力) ---

# 出力先のファイルパスを定義
RESULT_FILE="/home/<your_user>/archive/day3/result.txt"

# 引数でログファイルが指定されているかチェック
if [ -z "$1" ]; then
  echo "エラー: 解析対象のログファイルを指定してください。" >&2
  echo "使い方: $0 <ログファイル>" >&2
  exit 1
fi

LOG_FILE="$1"

# ファイルが存在するかチェック
if [ ! -f "$LOG_FILE" ]; then
  echo "エラー: ファイル '$LOG_FILE' が見つかりません。" >&2
  exit 1
fi

# メインの処理
# 処理結果をリダイレクトでファイルに上書き保存
grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' "$LOG_FILE" | sort | uniq -c | sort -nr > "$RESULT_FILE"

echo "集計結果を $RESULT_FILE に出力しました。"