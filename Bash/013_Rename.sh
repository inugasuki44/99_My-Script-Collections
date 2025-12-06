#!/bin/bash

target_dir="$1"
files_renamed=0

# 1. 引数が空かチェック
if [ -z "$target_dir" ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
elif [ ! -d "$target_dir" ]; then # 2. 引数がディレクトリかチェック
    echo "Error: '$target_dir' is not a valid directory."
    exit 1
fi

# 3. ディレクトリ内の.txtファイルをループ処理
for file_path in "$target_dir"/*.txt
do
    # 4. ワイルドカードが展開されず、ファイルが見つからなかった場合のエラーを防ぐ
    if [ -f "$file_path" ]; then
        mv "$file_path" "${file_path%.txt}.md"
        echo "Renamed '$file_path' to '${file_path%.txt}.md'"
        files_renamed=1
    fi
done

# 5. 最終的な結果を報告
if [ $files_renamed -eq 0 ]; then
    echo "No .txt files found to rename in '$target_dir'."
else
    echo "All done!"
fi
