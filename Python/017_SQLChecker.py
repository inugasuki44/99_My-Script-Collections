import argparse
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# --- グローバル変数として定義 ---
payload = "'"
sql_errors = [
    "You have an error in your SQL syntax",
    "Unclosed quotation mark",
    "SQL syntax error",
    "mysql_fetch_array()"
]

# --- check_vulnerability 関数を定義 ---
def check_vulnerability(attack_url):
    print(f"\n    [+] Testing URL: {attack_url}")
    try:
        response = requests.get(attack_url)
        response.raise_for_status()

        print(f"    [~] Response Status Code: {response.status_code}")
        print(f"    [~] Response Body (first 500 chars):\\n{response.text[:500]}...") # 長い場合は最初の500文字だけ表示

        vulnerability_found = False
        print("\n    --- エラーメッセージのチェックを開始します ---")

        for error_message in sql_errors:
            print(f"    [~] Searching for '{error_message}' in response...")

            if error_message in response.text:
                print(f"    [!!!] Found potential SQL Injection vulnerability: '{error_message}'")
                vulnerability_found = True
                break
            else:
                print(f"    [.] '{error_message}' not found.")

        print("    --- チェック終了 ---")

        if vulnerability_found:
            print("\n    [!!!] SQLインジェクションの脆弱性がある可能性があります！")
            return True
        else:
            print("\n    [+] SQLインジェクションの脆弱性は見つかりませんでした。")
            return False

    except requests.exceptions.RequestException as e:
        print(f"    [!] An error occurred during the request: {e}")
        return False

# --- メインのスクリプト実行部分 ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple SQL Injection checker.")
    parser.add_argument("url", help="The full URL to test.")
    args = parser.parse_args()

    print(f"[*] Target URL: {args.url}")

    parsed_result = urlparse(args.url)
    query_string = parsed_result.query
    query_params = parse_qs(query_string)

    if not query_params:
        print("[!] No query parameters found in the URL. Exiting.")
        exit()

    print(f"[*] Found {len(query_params)} query parameters.")
    print(f"[*] Using Payload: {payload}")

    for param_to_test, value_list in query_params.items():
        print(f"\n[*] Testing parameter: \"{param_to_test}\"")

        params_copy = query_params.copy()
        original_value = value_list[0]
        params_copy[param_to_test] = [original_value + payload]

        new_query_string = urlencode(params_copy, doseq=True)

        revised_parsed_result = parsed_result._replace(query=new_query_string)
        attack_url = urlunparse(revised_parsed_result)

        is_vulnerable = check_vulnerability(attack_url)
