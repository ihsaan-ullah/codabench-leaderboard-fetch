# codabench-leaderboard-fetch

This repository shows an example of how a leaderboard can be fetched from a Codabench competition, processed, and exported as an HTML. 

The example code fetches a leaderboard, saves it in json, processes the json to select the top entry per user, saves the processed json, and converts the processed json to an HTML table.


##  Set Up
To run the code, you need to first configure your codabench `username` and `password` in the `.env` file. You also have to configure the `config.py` file. In `config.py` you will find explanation for all the config variables. After carefully configuring the set up, you can proceed to the next steps below. Each step explains the role of each `.py` file and how you can run them individually or as a pipeline.

##  Entry point (Pipeline)
The entry point script is `run_leaderboard_pipeline.py`. This script uses `SCRIPTS_TO_RUN` from the `config.py` to run other scipts in proper order i.e. 
1. fetch leaderboad results
2. process leaderboard results
3. generate results html
4. deploy results html

To run the entry point script, you can use the following command:
```
python3 run_leaderboard_pipeline.py
```

NOTE: You can skip one of the scripts by updating `config.py` or you can totally skip this entry point step and run the scripts individually. See the next steps below.

## 1. Fetch Leaderboard Results
This script uses the credentials configured in `.env` file to login to Codabench to get Auth Token. It then uses the config variables from `config.py` and Auth Token to fetch the leaderboard entries. The script saves the leaderboard result in a json file.

To run `fetch_leaderboard_results` script, you can use the following command:
```
python3 fetch_leaderboard_results.py
```

NOTE: only competition organizers can fetch leaderboard results for a competition. Regular users are not permitted by the API.

## 2. Process Leaderboard Results
This script uses the config variables from `config.py` and the saved json leaderboard results to further process the leaderboard entries. Final result has only one entry per user with the highest score. The processed result is saved in a json file to be used in the HTML.

To run `process_leaderboard_results.py` script, you can use the following command:
```
python3 process_leaderboard_results.py
```

## 3. Generate Results HTML
This script uses the config variables from `config.py` and the saved processed json result to generate an HTML file with the results in a table. An HTML template file `template.html` is used for the HTML generation. This generated HTML is saved to be used by the optinal next step.

To run `generate_results_html.py` script, you can use the following command:
```
python3 generate_results_html.py
```

## 4. (Optional) Deploy Results HTML
This is an optional script and may not be needed for your use case. This script uses the config variables from `config.py` and the saved html file to copy it to a GitHub repository folder and programatically create a branch, commit changes, push changes, and finally delete the branch.

To run `deploy_results_html.py` script, you can use the following command:
```
python3 deploy_results_html.py
```

## 5. (Optional) GitHub Workflow for Branch Auto Merge 
This is an optional GitHub workflow file that you can use to auto merge leaderboard update branches created by Step 4.

To use `leaderboard-results-auto-pr-merge.yaml` workflow, add it to `.github/workflows/` in your GitHub repository
NOTE: You may need a GitHub Personal Access Token (PAT) added to the repository secrets to make this workflow work.

## Contact
For any questions contact by email: `ihsan2131@gmail.com`
