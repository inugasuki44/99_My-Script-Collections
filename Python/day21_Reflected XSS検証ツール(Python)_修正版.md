### Day21_Reflected XSS検証ツール(ログイン対応版)

連日投稿21日目です。昨日のリベンジを果たしました。

#### 今回の目的

昨日のDay20で、`BeautifulSoup`を使ったより高度なXSS検証ツール（Verifier）のロジックは完成しました。しかし、Day18・19で実装した**ログイン機能**を組み込んでいなかったため、DVWAに弾かれてしまい、テストを実行できませんでした。

そこで、今日のチャレンジでは、Day20で作成したVerifierに、**ログイン機能とCSRFトークン処理を完全に統合**し、認証が必要なWebページに対しても自動でXSS検証を実行できる、真に実用的なツールを完成させることを目指します。

:::note info
このチャレンジについて
目的: セキュリティエンジニアとしての技術力向上
手段: シェルスクリプト作成を通じて学習
実施する事: 自動化,監視,ツール開発基礎学習など
:::

#### 目次

*   [実行結果](#実行結果)
*   [実行環境](#実行環境)
*   [開発ステップ](#開発ステップ)
*   [開発中の気づき](#開発中の気づき)
*   [コード全文](#コード全文)
*   [コードの詳細な解説](#コードの詳細な解説)
*   [実行方法](#実行方法)
*   [まとめ](#まとめ)

#### 実行結果

Day20のコードに、Day18で完成させたログイン処理を統合し、DVWAのReflected XSSページに対して実行しました。見事、ログインを突破し、脆弱性の検出に成功しました。

```bash
# これを打つと... (ターゲットはxss_rページ、パラメータはname)
$ python3 ./xss_verifier_login.py "http://<IPアドレス>/vulnerabilities/xss_r/?name=test"

# こうなる
[*] Target URL: http://<IPアドレス>/vulnerabilities/xss_r/?name=test
[*] Attempting to log in to DVWA at http://<IPアドレス>/login.php...
    [~] Fetching CSRF token from login page...
    [~] Found CSRF token: 669ce0a85b19eb03671610ac7f907496
    [~] Submitting login form with CSRF token...
[+] Successfully logged in to DVWA.
[*] Found 1 query parameters to test: ['name']
[*] Using Payload: <div id='xss_test_marker'></div>

[*] Testing parameter: "name"

    [~] Generated Attack URL: http://<IPアドレス>/vulnerabilities/xss_r/?name=test%3Cdiv+id%3D%27xss_test_marker%27%3E%3C%2Fdiv%3E
    [+] Verifying URL: http://<IPアドレス>/vulnerabilities/xss_r/?name=test%3Cdiv+id%3D%27xss_test_marker%27%3E%3C%2Fdiv%3E
    [~] Response Status Code: 200
    [!!!] Found potential XSS vulnerability! The payload was rendered as a tag.
    [!!!] Vulnerability confirmed for parameter: "name"

========================================
[!!!] SUMMARY: The target URL appears to be vulnerable to Reflected XSS.
========================================
```
**実行結果の考察:**
ログイン処理、CSRFトークン対応、そしてHTML構造の検証ロジックがすべて正しく連携し、`name`パラメータにXSS脆弱性があることを正確に突き止めることができました。

#### 実行環境

*   **クラウド環境:** AWS EC2
*   **コンテナ技術:** Docker
*   **接続元（ローカルPC）:** Windows 10
*   **ターミナルソフト:** Tera Term
*   **接続先（サーバー）:** Amazon Linux 2 (EC2インスタンス内)
*   **使用言語:** Python 3.x
*   **外部ライブラリ:** `requests`, `beautifulsoup4`
*   **テスト対象:** DVWA (Damn Vulnerable Web Application) v1.10

#### 開発ステップ

Day20で作成したコードに、Day18で完成させたログイン処理を統合しました。

1.  **`verify_xss_vulnerability`関数の修正:**
    *   ログイン状態を維持するため、`session`オブジェクトを引数として受け取るように変更しました (`def verify_xss_vulnerability(session, attack_url):`)。
    *   関数内の`requests.get()`を`session.get()`に置き換え、セッションを引き継いでリクエストを送信するようにしました。

2.  **メイン処理へのログインロジックの統合:**
    *   Day18で作成した、CSRFトークンを取得してログインする一連の処理を、`if __name__ == "__main__":`ブロックの先頭に配置しました。

3.  **関数呼び出しの修正:**
    *   メインの`for`ループの中から`verify_xss_vulnerability`関数を呼び出す際に、`session`オブジェクトを引数として渡すように修正しました。

#### 開発中の気づき

最後の最後が、ツールの本質に関わる結構おおきな気づき。

1.  **`SyntaxError`の犯人:**
    *   昨日から何度も遭遇した、`exit()`や`print()`のような正しいはずの行で発生する`SyntaxError`。体感的にだいたい原因は、**その直前の行**にありがち。今回は`split('user_token\' value=\'')`のように、シングルクォートの中でシングルクォートを使おうとしていたのが原因でした。文字列全体をダブルクォートで囲む`split("user_token' value='")`ことで解決。これは本当に忘れがちなミス。

2.  **`requests.Session()`の本当の意味:**
    *   ログイン処理を統合する際、`verify_xss_vulnerability`関数の中で安易に`requests.get()`を使ってしまい、ログインが維持されない、という問題に直面しました。メイン処理で作成した`session`オブジェクトを関数に引き渡し、`session.get()`を使うことで、初めてログイン状態が維持される。**セッションは、IDカードのように、リクエストのたびに明示的に提示し続ける必要がある感じ**

3.  **ブラウザの見た目 vs HTMLソースコード:**
    *   これ重要。手動でブラウザからペイロード`<div id='xss_test_marker'></div>`を送信すると、画面上は`Hello`としか表示されず、何も変化がないように見えました。しかし、スクリプトは「脆弱性あり」と報告する。なんぞ？これ
    *   答え：**ブラウザが見せているのはレンダリング後の「見た目」であり、スクリプトが見ているのは「HTMLソースコードそのもの」**な、違い
    *   画面に変化がなくても、HTMLソースコードの中に`<div id='xss_test_marker'></div>`というタグがそのまま埋め込まれていれば、それは**ブラウザが解釈可能な命令が注入された**ということであり、立派なXSS脆弱性。私たちの検証ツールは、この「目に見えない構造の変化」を正しく検知できていた、というわけです。診断ツールを作る上で、この視点はめちゃくちゃ重要だと感じました。

#### コード全文

```python
#!/usr/bin/env python3
import argparse
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup

# --- グローバル変数として定義 ---
payload = "<div id='xss_test_marker'></div>"

# --- 脆弱性検証関数を定義 ---
def verify_xss_vulnerability(session, attack_url):
    """指定されたURLにアクセスし、XSSペイロードが構造として反映されたかを検証する"""
    print(f"    [+] Verifying URL: {attack_url}")
    try:
        # セッションを使ってリクエストを送信
        response = session.get(attack_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        if soup.find('div', id='xss_test_marker'):
            print(f"    [!!!] Found potential XSS vulnerability! The payload was rendered as a tag.")
            return True
        else:
            print("    [+] Payload was not found as a rendered tag.")
            return False

    except requests.exceptions.RequestException as e:
        print(f"    [!] An error occurred during the request: {e}")
        return False

# --- メインのスクリプト実行部分 ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple XSS Verifier for DVWA.")
    parser.add_argument("url", help="The full URL of the target page to test (e.g., http://<ip>/vulnerabilities/xss_r/).")
    args = parser.parse_args()

    print(f"[*] Target URL: {args.url}")

    # --- DVWAログイン処理 ---
    try:
        dvwa_base_url = args.url.split('/vulnerabilities')[0]
    except IndexError:
        print("[!] Invalid URL format. Please provide the full DVWA vulnerability URL.")
        exit()

    login_url = f"{dvwa_base_url}/login.php"
    username = "admin"
    password = "password"
    
    session = requests.Session()

    print(f"[*] Attempting to log in to DVWA at {login_url}...")
    try:
        print("    [~] Fetching CSRF token from login page...")
        login_page_response = session.get(login_url)
        login_page_response.raise_for_status()

        token_part = login_page_response.text.split("user_token' value='")[1]
        user_token = token_part.split("'")[0]
        print(f"    [~] Found CSRF token: {user_token}")

        login_data = {
            "username": username,
            "password": password,
            "user_token": user_token,
            "Login": "Login"
        }

        print("    [~] Submitting login form with CSRF token...")
        login_response = session.post(login_url, data=login_data)
        login_response.raise_for_status()

        if "Welcome" in login_response.text or "logout.php" in login_response.text:
            print("[+] Successfully logged in to DVWA.")
        else:
            print("[!] Failed to log in to DVWA. The response did not indicate a successful login.")
            exit()

    except (requests.exceptions.RequestException, IndexError) as e:
        print(f"[!] An error occurred during DVWA login: {e}")
        exit()
    
    # --- 脆弱性チェックの実行 ---
    parsed_result = urlparse(args.url)
    query_string = parsed_result.query
    query_params = parse_qs(query_string)

    if not query_params:
        print("[!] No query parameters found in the URL. Exiting.")
        exit()

    print(f"[*] Found {len(query_params)} query parameters to test: {list(query_params.keys())}")
    print(f"[*] Using Payload: {payload}")

    overall_vulnerable = False
    for param_to_test, original_values in query_params.items():
        print(f"\n[*] Testing parameter: \"{param_to_test}\"")

        params_copy = query_params.copy()
        original_value = original_values[0]
        params_copy[param_to_test] = [original_value + payload]
        
        new_query_string = urlencode(params_copy, doseq=True)
        
        revised_parsed_result = parsed_result._replace(query=new_query_string)
        attack_url = urlunparse(revised_parsed_result)

        print(f"    [~] Generated Attack URL: {attack_url}")
        
        if verify_xss_vulnerability(session, attack_url):
            overall_vulnerable = True
            print(f"    [!!!] Vulnerability confirmed for parameter: \"{param_to_test}\"")

    print("\n" + "="*40)
    if overall_vulnerable:
        print("[!!!] SUMMARY: The target URL appears to be vulnerable to Reflected XSS.")
    else:
        print("[+] SUMMARY: No Reflected XSS vulnerabilities were found.")
    print("="*40)
```

#### コードの詳細な解説

このスクリプトは、Day18, 19, 20の知識を統合したものです。

*   **`verify_xss_vulnerability` 関数:**
    *   `BeautifulSoup`を使い、レスポンスのHTMLを解析します。
    *   `soup.find('div', id='xss_test_marker')`で、ペイロードがHTMLタグとして存在するかを検証します。単純な文字列検索よりも信頼性が高いのが特徴です。

*   **メインのスクリプト実行部分:**
    *   **ログイン処理:** `requests.Session()`を使ってセッションを開始し、まずGETリクエストでCSRFトークンを取得後、POSTリクエストでトークンを含めてログインします。
    *   **脆弱性チェック:** ログイン後のセッションを`verify_xss_vulnerability`関数に引き渡し、各パラメータのテストを実行します。

#### 実行方法

1.  上記のコードを`xss_verifier_login.py`のような名前でファイルに保存します。
2.  必要なPythonライブラリをインストールします。
    ```bash
    pip install requests beautifulsoup4
    ```
3.  ターミナルでスクリプトを実行します。URLに`&`が含まれる場合は、必ずURL全体をダブルクォーテーション（`"`）で囲んでください。
    ```bash
    python3 xss_verifier_login.py "http://<DVWAのIPアドレス>/vulnerabilities/xss_r/?name=test"
    ```

#### まとめ

Day21で、ついにログイン機能付きのXSS検証ツールが完成しました。Day18から続いたログインの壁、CSRFトークンの謎、あとシェルの罠を乗り越え、ツールが意図通りに脆弱性を検出した瞬間は、かなりの達成感がありました。

特に、**「ブラウザの見た目とHTMLソースコードは違う」**という気づきは、今後の診断作業において非常に重要な視点になると感じています。画面に変化がなくても、ソースコードレベルでペイロードが反映されていれば、それは脆弱性。この原則を自動で検証できるようになったのはでかい。