import json
from config import (
    RAW_RESULT_JSON_FILE,
    PROCESSED_RESULT_JSON_FILE,
    RESULTS_KEY,
    SCORE_KEY
)


def extract_username_and_submissionid(entry_key):
    """
    Extract username and submission_id from a key like 'username-1122'
    """
    username_and_submissionid = entry_key.split("-")
    return username_and_submissionid[0], username_and_submissionid[1]


def main():
    """
    Processes raw result data to find each user's best submission.  
    Groups submissions by username, selects the highest-scoring one,  
    and saves the summarized results to a JSON file.
    """
    with open(RAW_RESULT_JSON_FILE, "r") as f:
        data = json.load(f)

    results = data.get(RESULTS_KEY)
    if not results:
        raise KeyError(f"[-] Key '{RESULTS_KEY}' not found in JSON file.")

    # Group results by username
    grouped = {}
    for key, value in results.items():
        username, submission_id = extract_username_and_submissionid(key)
        value["submission_id"] = submission_id
        if username not in grouped:
            grouped[username] = []
        grouped[username].append(value)

    # Find best score for each user
    best_entries = []
    for username, submissions in grouped.items():
        # Get highest score submission
        best = max(submissions, key=lambda x: float(x.get(SCORE_KEY, 0)))
        fact_sheet = best.get("fact_sheet_answers", {})
        best_entries.append({
            "username": username,
            "submission_id": best.get("submission_id", ""),
            "method_name": fact_sheet.get("method_name", "Unknown"),
            "score": float(best.get(SCORE_KEY, 0)),
        })

    # Save result
    with open(PROCESSED_RESULT_JSON_FILE, "w") as f:
        json.dump(best_entries, f, indent=2)

    print(f"[+] Saved best results for {len(best_entries)} users to {PROCESSED_RESULT_JSON_FILE}")


if __name__ == "__main__":
    main()
