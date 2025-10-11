import subprocess
import sys
from config import SCRIPTS_TO_RUN


def run_script(script):
    """
    Runs the given Python script using the current interpreter.  
    Prints the script’s output on success or displays errors and exits if it fails.
    """
    print(f"*** Running {script} ...\n")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[-] Error while running {script}:")
        print(result.stderr.strip())
        sys.exit(result.returncode)

    print(result.stdout.strip())
    print(f"\n*** Completed {script}\n")
    print("--- --- --- --- ---")


def main():
    print("\n=====================================")
    print("Starting Leaderboard Pipeline")
    print("-------------------------------------\n")
    for script in SCRIPTS_TO_RUN:
        run_script(script)
    print("\n\n=====================================")
    print("All steps completed successfully.")
    print("-------------------------------------")


if __name__ == "__main__":
    main()
