#!/bin/bash

# =============================================================
# Webサイト死活監視スクリプト (getHTTPStatus.sh)
#
# urls.txtからURLリストを読み込み、それぞれのHTTPステータスを
# 確認して結果を表示します。
# =============================================================

# --- 1. パスの設定 ---
# スクリプト自身のディレクトリを取得し、どこから実行されてもパスを解決できるようにする
SCRIPT_DIR=$(dirname "$0")
TARGET_LIST="$SCRIPT_DIR/urls.txt"


# --- 2. 事前チェック ---
# ターゲットリストが存在するかチェック
if [ ! -f "$TARGET_LIST" ]; then
  echo "エラー: ターゲットリスト '$TARGET_LIST' が見つかりません。" >&2
  exit 1
fi


# --- 3. メイン処理 ---
echo "--- サイトのステータスチェックを開始 ---"

while read -r url; do
  # 空行または'#'で始まるコメント行はスキップする
  if [ -z "$url" ] || [[ "$url" == \#* ]]; then
    continue
  fi

  # curlでHTTPステータスコードを取得。-m 5でタイムアウトを5秒に設定。
  status_code=$(curl -m 5 -s -o /dev/null -w "%{http_code}" "$url")

  # ステータスコードに応じて結果を判定・表示
  if [ "$status_code" -eq 200 ]; then
    echo -e "[\e[32mOK\e[0m]       : (\e[32m$status_code\e[0m) $url"
  elif [ "$status_code" -eq 301 ] || [ "$status_code" -eq 302 ]; then
    echo -e "[\e[33mREDIRECT\e[0m] : (\e[33m$status_code\e[0m) $url"
  elif [ "$status_code" -eq 404 ]; then
    echo -e "[\e[31mNOT FOUND\e[0m]: (\e[31m$status_code\e[0m) $url"
  else
    echo -e "[\e[31mERROR\e[0m]    : (\e[31m$status_code\e[0m) $url"
  fi

done < "$TARGET_LIST"

echo "--- チェック完了 ---"