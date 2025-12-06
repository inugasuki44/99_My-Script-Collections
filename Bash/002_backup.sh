#!/bin/bash

# ============================================
# ログヘッダー生成スクリプト
# ============================================

# 1. ログファイルのパスを指定
LOG_FILE="/home/<your_user>/day2/batch.log"

# 2. ログに出力する情報を変数に格納
START_TIME=$(date '+%Y-%m-%d %H:%M:%S %Z')
EXEC_USER=$(whoami)
DISK_USAGE=$(df -h / | awk 'NR==2') # ルートディレクトリの使用状況のみを抽出

# 3. ログファイルにヘッダー情報を追記
echo "==================================================" >> $LOG_FILE
echo "  Process Started: $START_TIME" >> $LOG_FILE
echo "  Executed by    : $EXEC_USER" >> $LOG_FILE
echo "  Disk Usage     : $DISK_USAGE" >> $LOG_FILE
echo "==================================================" >> $LOG_FILE

echo "ログヘッダーを $LOG_FILE に書き込みました。"