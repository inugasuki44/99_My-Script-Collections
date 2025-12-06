# Day37: PythonによるLog Poisoningシミュレーションの実装

### 今回の目的
週次計画に基づき、Day37のテーマである「高度なLFI手法とログポイズニング」を実践するため、Pythonを用いて攻撃シミュレーションスクリプトをゼロから構築した。目的は、Log Poisoning攻撃がどのように成立し、LFI脆弱性がRCE（リモートコード実行）へと昇格するのか、その技術的プロセスをコードレベルで完全に理解することである。

:::note info
このチャレンジについて
目的: セキュリティエンジニアとしての技術力向上
手段: シェルスクリプト作成を通じて学習
実施する事: 自動化,監視,ツール開発基礎学習など
:::

### 目次
*   [実行結果](#実行結果)
*   [実行環境](#実行環境)
*   [開発ステップ](#開発ステップ)
*   [思考フローと問い](#思考フローと問い)
*   [開発中の気づき](#開発中の気づき)
*   [コード全文](#コード全文)
*   [コードの詳細な解説](#コードの詳細な解説)
*   [実行方法](#実行方法)
*   [まとめ](#まとめ)

### 実行結果
完成した`log_poison_sim.py`を実行した際のアウトプット。攻撃者がログを汚染し、サーバーがそれを読み込んでコマンドを抜き出すまでの一連の流れがシミュレートされている。

```text
[ATTACKER] Log file has been poisoned.
--------------------
[SERVER] Simulating LFI to include log file...
[SERVER] Malicious code found in log!
[SERVER] RCE successful. Would have executed: 'whoami'
```

### 実行環境
*   **クラウド環境:** N/A
*   **コンテナ技術:** N/A
*   **接続元（ローカルPC）:** Windows 11
*   **ターミナルソフト:** Windows Terminal
*   **接続先（サーバー）:** N/A
*   **使用言語:** Python 3
*   **外部ライブラリ:** `datetime`, `re` (いずれも標準ライブラリ)
*   **テスト対象:** N/A

### 開発ステップ
本スクリプトは、以下のステップで段階的に開発された。

1.  **設計図（Blueprint）の確認:** まず、スクリプト全体の構造を定義した設計図を確認。`poison_log_file`と`simulate_lfi_exploit`という2つの主要関数を実装する方針を固めた。
2.  **ログ汚染機能の実装:** `poison_log_file`関数を実装。f-stringを用いて、動的なタイムスタンプと攻撃コマンドを含む悪意のあるログ文字列を生成し、`with open(...)`を使ってターゲットのログファイルに追記する処理を完成させた。
3.  **LFIシミュレート機能の実装:** `simulate_lfi_exploit`関数を実装。まず、ログファイルを安全に読み込み、`re.search()`を用いてWebシェルのパターンを探索。マッチオブジェクトの有無を`if match:`で判定し、`match.group(1)`でキャプチャしたコマンドを抽出するロジックを完成させた。
4.  **メイン関数の実装:** `main`関数から上記2つの関数を順番に呼び出し、攻撃フロー全体をオーケストレーションする処理を実装した。

### 思考フローと問い
開発プロセスにおいて、Pythonの基本的な挙動に関する重要な問いが生まれた。

- **問い:** `if match:`のように、比較演算子（`==`など）なしで、なぜ`if`文は条件を判断できるのか？
- **答え:** これはPythonの「Truthiness」という概念によるもの。Pythonでは`None`、`0`、空の文字列`""`やリスト`[]`などは「Falsy（偽）」として扱われる。一方で、`re.search()`が成功時に返す「マッチオブジェクト」を含む、それ以外のほとんどのオブジェクトは「Truthy（真）」として扱われる。そのため、`if match:`は「`match`が`None`ではない（＝マッチした）」というチェックを簡潔に表現する、Python的な書き方である。

### 開発中の気づき
今回の実装を通じて、正規表現（regex）の扱いに慣れることができた。特に、`re.search()`の結果を`if`文で判定し、`match.group(1)`で特定のキャプチャグループ（今回はコマンド部分）を抜き出すという一連の流れは、テキスト処理における強力なパターンだと実感した。また、「Truthiness」の概念を再確認したことで、よりPythonらしいコードを書く意識が高まった。

### コード全文
```python
# log_poison_sim.py

import datetime
import re

# 偽のログファイルと「実行」したいコマンドの定数を定義する。
LOG_FILE = "fake_access.log"
ATTACKER_IP = "192.168.1.101"
TARGET_COMMAND = "whoami"


def poison_log_file(log_path, ip, command):
    """
    攻撃者がログを汚染するアクションをシミュレートする。
    """
    timestamp = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S %z')
    malicious_log = f'{ip} - - [{timestamp}] "GET /<?php system(\'{command}\'); ?> HTTP/1.1" 200 1234\n'

    # 'with open' でファイルを安全に追記モードで開く
    with open(log_path, 'a') as f:
        # 悪意のあるログエントリをファイルに書き込む。
        f.write(malicious_log)

    print("[ATTACKER] Log file has been poisoned.")


def simulate_lfi_exploit(log_path):
    """
    脆弱性のあるWebサーバーがポイズニングを受けたログファイルをインクルードするのをシミュレートする。
    """
    print("[SERVER] Simulating LFI to include log file...")

    log_content = ""
    try:
        # 'with open' でファイルを開き、全体を読み込む
        with open(log_path, 'r') as f:
            log_content = f.read()
    except FileNotFoundError:
        print(f"エラー: ファイル '{log_path}' が見つかりません。")
        return

    # 正規表現を使い、コンテンツからWebシェルのパターンを検索し、コマンドを抽出する。
    match = re.search(r"<\?php system\('(.*?)'\);\?>", log_content)

    if match:
        # マッチした場合、キャプチャしたコマンドを取得
        command_found = match.group(1)
        print("[SERVER] Malicious code found in log!")
        print(f"[SERVER] RCE successful. Would have executed: '{command_found}'")
    else:
        # マッチしなかった場合
        print("[SERVER] No malicious code found in log.")


def main():
    """
    シミュレーション全体を統括する。
    """
    # ステップ1: 攻撃者がログを汚染する。
    poison_log_file(LOG_FILE, ATTACKER_IP, TARGET_COMMAND)

    # 出力の可読性のために空白行を入れる。
    print("-" * 20)

    # ステップ2: 脆弱なサーバーがログをインクルードする。
    simulate_lfi_exploit(LOG_FILE)


# --- メイン実行ブロック ---
if __name__ == "__main__":
    main()
```

### コードの詳細な解説
- **`poison_log_file`**: この関数は攻撃シミュレーションの第一段階。f-stringを使って、現在時刻、攻撃者のIP、そしてPHPの`system()`関数を含むWebシェルを埋め込んだログ行を生成する。`open()`を`'a'`（追記）モードで使うことで、ログファイルに新しい攻撃の痕跡を安全に追加する。
- **`simulate_lfi_exploit`**: こちらはサーバー側のシミュレーション。まずログファイルを`'r'`（読み取り）モードで開き、全内容を変数`log_content`に格納する。次に、`re.search()`が本処理の核心部であり、正規表現 `r"<\?php system\('(.*?)'\);\?>"` を使ってログの中からWebシェルを探す。`(.*?)`の部分がキャプチャグループとなり、`match.group(1)`でコマンド部分だけを正確に抽出している。

### 実行方法
1.  上記のコードを `log_poison_sim.py` のような名前で保存する。
2.  ターミナルでそのファイルを保存したディレクトリに移動する。
3.  `python log_poison_sim.py` コマンドを実行する。
4.  実行後、同ディレクトリに `fake_access.log` ファイルが生成され、中には悪意のあるログが記録されていることを確認できる。

### まとめ
今回のチャレンジを通じて、Log Poisoning攻撃の具体的な手順をコードで再現することができた。攻撃者側の「汚染」とサーバー側の「実行」という2つの視点を実装することで、脆弱性がどのように連鎖して深刻なRCEにつながるかを明確に理解できた。特に、Pythonの`re`モジュールと「Truthiness」という言語仕様への理解が深まり、実践的なスキルが向上した。
