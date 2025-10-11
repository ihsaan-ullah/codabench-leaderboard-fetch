# Config for `run_leaderboard_pipeline`
# This list consists the names of the scripts to be run by the leaderboard pipeline.
# You can comment out or remove an item from the list if you don't want to run it.
# Note: The scipts should be run in the given order as each script processes the output 
# of the previous script
SCRIPTS_TO_RUN = [
    "fetch_leaderboard_results.py",
    "process_leaderboard_results.py",
    "generate_results_html.py",
    "deploy_results_html.py",
]


# Config for `fetch_leaderboard_results`
# To fetch a leaderboard, you need a competition id and phase id from a Codabench competition
# Two apis are called to fetch a leaderboard:
# 1. `Login` (using codabench credentials from .env) to get Auth Token
# 2. `Results`` to get a leaderboard using compeition_id, phase_id and auth_token
# NOTE: Only competition organizers can fetch leaderboard results
COMPETITION_ID = <CODABENCH_COMPETITION_ID>
PHASE_ID = <CODABENCH_PHASE_ID>
BASE_URL = "https://www.codabench.org/api"
LOGIN_URL = f"{BASE_URL}/api-token-auth/"
RESULTS_URL = f"{BASE_URL}/competitions/{COMPETITION_ID}/results.json?phase={PHASE_ID}"
# We setup file name for the json file where the raw leaderboard results will be saved
RAW_RESULT_JSON_FILE = "results_raw.json"  # also used by `process_leaderboard_results.py`


# Config for `process_leaderboard_results.py`
# We setup file name for the json file where processed results will be saved 
PROCESSED_RESULT_JSON_FILE = "results_processed.json"  # also used by `generate_results_html.py`
# This key is found in the raw leaderboard result. You can get the exact key by opening the `results` API in the browser or any other API execution tool
RESULTS_KEY = "Results - Phase 1"
# This is the key of the score column that you will find in the response of the `results` API
SCORE_KEY = "Competition Phase 1-Score"


# Config for `generate_results_html.py`
# This HTML template is used to show processed result in a table
HTML_TEMPLATE_FILE = "template.html"
# HTML when populated with result is saved for further steps
HTML_OUTPUT_FILE = "results_table.html"  # also used by `deploy_results_html.py`


# Config for `deploy_results_html.py`
# NOTE: this is an optional step if you want to programmatically push the html file to a GitHub repository
# Github repo folder where we want to first copy the  result table html file
TARGET_REPO_DIR = "../FAIR-Universe.github.io"
# The html file name you want to use in the github repo. You can use the same name as `HTML_OUTPUT_FILE`
TARGET_HTML_FILE = "Leaderboard-Results-Phase-1.html"
# To push changes to github, we use a prefix for the branch name so that it can be identified easily for further processing
# e.g. an automated workflow to merge the branch
BRANCH_PREFIX = "phase-1-leaderboard-update"
