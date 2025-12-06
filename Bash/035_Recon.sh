#!/bin/bash

echo "--- Starting LFI/RFI Recon Scan ---"

while read url; do
  # curlでURLの内容を取得し、パイプ(|)でgrepに渡す
  # grepが-q(quiet)モードでパターンに一致した場合(終了コード0)、thenブロックが実行される
  if curl -s "$url" | grep -q -E "page=|file=|include="; then
    echo "Potential vulnerability found: $url"
  fi
done < targets.txt

echo "--- Scan Complete ---"
