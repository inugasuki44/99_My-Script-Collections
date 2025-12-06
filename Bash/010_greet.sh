#!/bin/bash

# 1. ユーザーに名前を尋ね、'name'変数に入力を保存
read -p "Please enter your name: " name

# 2. 'name'変数が空であるかをチェック
if [ -z "$name" ]; then
    # もし空であれば、エラーメッセージを表示して終了
    echo "Error: No name was entered."
    exit 1
fi

# 3. 名前が入力されていれば、挨拶メッセージを表示
echo "Hello, Mr. $name!"