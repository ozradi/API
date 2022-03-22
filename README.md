# Hacker News Filter 
## Quickstart

To run this project, start by installing & running OPA:

### Installing OPA:
  ```
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
  ```

### Running OPA:
```
  opa run -s opa_files/policy.rego opa_files/data.json --log-level debug --log-format text
```
Note that we are running OPA with 2 files:
* policy.rego - this file holds the filtering logic
* data.json - this file holds a map between a topic and keywords relevant to the topic

Run the project with:
```
  uvicorn main:app --reload
```

## Overview

This project queries Hackernews for stories, then uses OPA to filter the stories based on user's selection - popularity or topic
## Tech stack

Hackernews articles are returned from Hacker news API - https://github.com/HackerNews/API
OPA policy is here - https://github.com/open-policy-agent/opa

