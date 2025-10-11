import os
import requests
import json
from dotenv import load_dotenv
from config import (
    LOGIN_URL,
    RESULTS_URL,
    RAW_RESULT_JSON_FILE
)
# Load environment variables
load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def main():
    """
    Logs in to obtain an authentication token, fetches results from the API,  
    and saves them as a JSON file. Exits if login or data retrieval fails.
    """

    # Login to get token
    login_payload = {
        "username": USERNAME,
        "password": PASSWORD
    }
    login_response = requests.post(LOGIN_URL, data=login_payload)

    if login_response.status_code != 200:
        print(f"[-] Login failed: {login_response.status_code} {login_response.text}")
        exit(1)

    token = login_response.json().get("token")
    if not token:
        print("[-] No token found in login response.")
        exit(1)

    print(f"[+] Logged in successfully as {USERNAME}")

    # Fetch results
    headers = {
        "Authorization": f"Token {token}",
        "Accept": "application/json",
    }

    results_response = requests.get(RESULTS_URL, headers=headers)

    if results_response.status_code != 200:
        print(f"[-] Failed to fetch results: {results_response.status_code}")
        print(results_response.text)
        exit(1)

    # Save results to file
    with open(RAW_RESULT_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(results_response.json(), f, indent=4)

    print(f"[+] Results saved to {RAW_RESULT_JSON_FILE}")


if __name__ == "__main__":
    main()
