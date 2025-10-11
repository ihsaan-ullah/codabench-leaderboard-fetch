import os
import shutil
import subprocess
from datetime import datetime
from config import (
    HTML_OUTPUT_FILE as SOURCE_HTML_FILE,
    TARGET_REPO_DIR,
    TARGET_HTML_FILE,
    BRANCH_PREFIX
)
TARGET_PATH = os.path.join(TARGET_REPO_DIR, TARGET_HTML_FILE)


def run(cmd, cwd=None, capture=False):
    """
    Run a shell command and optionally capture output.
    """
    print(f"** Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[-] Error: {result.stderr.strip()}")
        raise RuntimeError(result.stderr)
    if not capture:
        print(result.stdout.strip())
    return result


def main():
    """
    Updates the leaderboard HTML in a Git repository.
    Copies the source file, creates a new branch with the changes,
    commits and pushes it to remote, then cleans up the local branch.
    """
    # Step 1: Check source file
    if not os.path.exists(SOURCE_HTML_FILE):
        raise FileNotFoundError(f"[-] Source file not found: {SOURCE_HTML_FILE}")

    # Step 2: Copy file
    os.makedirs(os.path.dirname(TARGET_PATH), exist_ok=True)
    shutil.copy2(SOURCE_HTML_FILE, TARGET_PATH)
    print(f"[+] Copied {SOURCE_HTML_FILE} → {TARGET_PATH}")

    # Step 3: Git operations setup
    print("[*] Preparing repository")
    run(["git", "fetch"], cwd=TARGET_REPO_DIR)
    run(["git", "checkout", "master"], cwd=TARGET_REPO_DIR)
    run(["git", "pull", "origin", "master"], cwd=TARGET_REPO_DIR)

    # Step 3.1: Check if there are any changes after copy
    result = run(
        ["git", "status", "--porcelain", os.path.basename(TARGET_PATH)],
        cwd=TARGET_REPO_DIR,
        capture=True,
    )

    if not result.stdout.strip():
        print("[x] No changes detected — nothing to commit. Exiting.")
        return

    # Step 4: Create and push new branch
    branch_name = f"{BRANCH_PREFIX}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print(f"[*] Creating new branch '{branch_name}' for leaderboard update")
    run(["git", "checkout", "-b", branch_name], cwd=TARGET_REPO_DIR)
    run(["git", "add", os.path.basename(TARGET_PATH)], cwd=TARGET_REPO_DIR)
    run(["git", "commit", "-m", f"Update leaderboard HTML ({datetime.now().isoformat(timespec='seconds')})"], cwd=TARGET_REPO_DIR)
    run(["git", "push", "-u", "origin", f"{branch_name}:{branch_name}"], cwd=TARGET_REPO_DIR)
    print(f"[+] Branch '{branch_name}' pushed successfully.")

    # Step 5: Cleanup - Switch back to master and delete the local branch
    print("[*] Cleaning up local branch")
    run(["git", "checkout", "master"], cwd=TARGET_REPO_DIR)
    run(["git", "branch", "-D", branch_name], cwd=TARGET_REPO_DIR)
    print(f"[+] Switched back to master and deleted local branch '{branch_name}'.")


if __name__ == "__main__":
    main()
