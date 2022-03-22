# Hacker News Filter 
## Overview

This project queries Hackernews for stories, then filters them based on popularity and interests using OPA.

See the demo to see it in action, clone to run it yourself, and configure it as desired

## Demo

<img src="media/hackernews-filter-demo.gif" alt="Hackernews Filter Demo">

In the demo, you can see three steps:
1. Run OPA - as explained in the next section, we run a local copy of OPA
2. Run HN Filter - in this step we simply start the server
3. Example - in this step we open localhost and click on fetching popular stories


## Quickstart

To run this project, start by installing & running OPA:
### Building OPA:

Create an virtualenv and install the requirements:

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
## Configuration

### To configure the filters:

### Filter by popularity
Popular stories are stories that have more than 100 upvotes.
To change the min. score for a story to be counted as popuplar open policy.rego and change the value

### Filter by topic
Stories can be filtered based on their topic as well.
The policy code checks for keywords in the title of the article.
The supported interests are listed in data\topics.py
* To alter what keywords define a topic, update data.json and restart OPA (no need to restart the server)
* To add a new topic of interest, add it both in data\topics.json, and in the data/topics.py file, then restart OPA and restart the server
### Project configuration

* OPA runs on port 8181
* The HN Filter runs on port 8000

## Tech stack

Hackernews articles are returned from Hacker news API - https://github.com/HackerNews/API

OPA policy is here - https://github.com/open-policy-agent/opa