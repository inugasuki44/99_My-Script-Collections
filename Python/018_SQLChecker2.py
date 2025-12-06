import argparse
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# --- グローバル変数として定義 ---
# ペイロードはシングルクォーテーション1文字
payload = "'"
# 検知対象のエラーメッセージリスト
sql_errors = [
    "You have an error in your SQL syntax",
    "Unclosed quotation mark",
    "SQL syntax error",
    "mysql_fetch_array()"
]

# --- 脆弱性チェック関数を定義 ---
def check_vulnerability(session, attack_url):
    """指定されたURLに対してSQLインジェクションの脆弱性チェックを行う"""
    print(f"\n    [+] Testing URL: {attack_url}")
    try:
        # セッションを使ってリクエストを送信
        response = session.get(attack_url)
        response.raise_for_status()

        print(f"    [~] Response Status Code: {response.status_code}")

        vulnerability_found = False
        print("\n    --- Starting error message check ---")

        for error_message in sql_errors:
            if error_message in response.text:
                print(f"    [!!!] Found potential SQL Injection vulnerability: '{error_message}'")
                vulnerability_found = True
                break
        
        if not vulnerability_found:
            print("    [+] No SQL Injection vulnerability found in this parameter.")

        return vulnerability_found

    except requests.exceptions.RequestException as e:
        print(f"    [!] An error occurred during the request: {e}")
        return False

# --- メインのスクリプト実行部分 ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple SQL Injection checker for DVWA.")
    parser.add_argument("url", help="The full URL of the target page to test (e.g., http://<ip>/vulnerabilities/sqli/).")
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
        # 1. GETリクエストでログインページからCSRFトークンを取得
        print("    [~] Fetching CSRF token from login page...")
        login_page_response = session.get(login_url)
        login_page_response.raise_for_status()

        # 2. 文字列操作でトークンを抽出
        token_part = login_page_response.text.split('user_token\' value=\'')[1]
        user_token = token_part.split("'")[0]
        print(f"    [~] Found CSRF token: {user_token}")

        # 3. ログインデータにCSRFトークンを追加
        login_data = {
            "username": username,
            "password": password,
            "user_token": user_token,
            "Login": "Login"
        }

        # 4. トークンを含めてPOSTリクエストを送信
        print("    [~] Submitting login form with CSRF token...")
        login_response = session.post(login_url, data=login_data)
        login_response.raise_for_status()

        # 5. ログイン成功の確認
        if "Welcome" in login_response.text or "logout.php" in login_response.text:
            print("[+] Successfully logged in to DVWA.")
        else:
            print("[!] Failed to log in to DVWA. The response did not indicate a successful login.")
            exit()

    except (requests.exceptions.RequestException, IndexError) as e:
        print(f"[!] An error occurred during DVWA login: {e}")
        print("[!] Could not get a valid CSRF token. Is the URL correct and DVWA running?")
        exit()
    
    # --- 脆弱性チェックの実行 ---
    parsed_result = urlparse(args.url)
    query_string = parsed_result.query
    query_params = parse_qs(query_string)

    if not query_params:
        print("[!] No query parameters found in the URL. Exiting.")
        exit()

    print(f"[*] Found {len(query_params)} query parameters to test.")
    print(f"[*] Using Payload: {payload}")

    overall_vulnerable = False
    for param_to_test, value_list in query_params.items():
        print(f"\n[*] Testing parameter: \"{param_to_test}\"" )

        params_copy = query_params.copy()
        original_value = value_list[0]
        params_copy[param_to_test] = [original_value + payload]
        
        new_query_string = urlencode(params_copy, doseq=True)
        
        revised_parsed_result = parsed_result._replace(query=new_query_string)
        attack_url = urlunparse(revised_parsed_result)
        
        # ログインセッションを渡して脆弱性チェックを実行
        if check_vulnerability(session, attack_url):
            overall_vulnerable = True

    print("\n" + "="*40)
    if overall_vulnerable:
        print("[!!!] SUMMARY: The target URL appears to be vulnerable to SQL Injection.")
    else:
        print("[+] SUMMARY: No SQL Injection vulnerabilities were found.")
    print("="*40)