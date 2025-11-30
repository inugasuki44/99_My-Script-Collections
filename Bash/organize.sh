#!/bin/bash

# ============================================
# 日付ディレクトリ作成スクリプト
# ============================================

# 1. 保存先の親ディレクトリを指定
TARGET_DIR="/home/<your_user>/archive"

# 2. 今日の日付を「YYYY-MM-DD」形式で取得
TODAY=$(date +%F)

# 3. 日付ディレクトリとサブディレクトリを一括作成
mkdir -p "$TARGET_DIR/$TODAY"/{logs,files,backups}

echo "ディレクトリを作成しました: $TARGET_DIR/$TODAY"
