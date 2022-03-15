#!/usr/bin/env python3

from typing import Optional
from fastapi import FastAPI
import json
from loguru import logger
from prompt_toolkit import HTML
from hackernews_fetcher import HackerNewsReader
from fastapi.responses import HTMLResponse

DEBUG = 1
MAX_STORIES = 50
JSON_PREFIX = "articles"
SLEEP_TIME = 10
HTML_TAG = "<html>"
HTML_CLOSE_TAG = "</html>"
HEAD_TAG = "<head>"
HEAD_CLOSE_TAG = "</head>"
TITLE_TAG = "<title>"
TITLE_CLOSE_TAG = "</title>"
BODY_TAG = "<body>"
BODY_CLOSE_TAG = "</body>"
P_TAG = "<p>"
P_CLOSE_TAG = "</p>"
BR_TAG = "<br/>"
TAB_SPACE = "\t"

app = FastAPI()

@app.get("/")
def read_root(): 
    return {"hello, world"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/more_than_100", response_class=HTMLResponse)
def showNews():
    reader = HackerNewsReader()
    if DEBUG == 0:
    # for debug purposes, loading all stories from a mock, instead of from Hackernews
        with open('example/mock_input.json') as json_file:
            all_stories = json.load(json_file)
    else:
        all_stories = reader.getStories(MAX_STORIES)
        # wrapping stories with json prefix and converting the return value to json
        all_stories = "{\"" + JSON_PREFIX + "\": " + json.dumps(all_stories) + "}"
    
    all_stories_as_json = json.loads(all_stories)

    filtered_stories = reader.filterStoriesPopularity(all_stories)
    logger.debug("Done fetching, now filtering based on OPA policy")
    logger.debug("Done filtering, now printing filtered stories:")
    website = HTML_TAG + HEAD_TAG + TITLE_TAG + "Filtered HN" + TITLE_CLOSE_TAG + HEAD_CLOSE_TAG + BODY_TAG
    for item in filtered_stories:
        article = P_TAG + all_stories_as_json[JSON_PREFIX][item]["title"] + " " + "<a target=\"_blank\" href=\"" + \
        all_stories_as_json[JSON_PREFIX][item]["url"] + "\">read more</a>" + P_CLOSE_TAG
        article += TAB_SPACE + "&nbsp;&nbsp;&nbsp;" + str(all_stories_as_json[JSON_PREFIX][item]["score"]) + " upvotes"
        logger.debug(article)
        website += article + BR_TAG + BR_TAG

    website += BODY_CLOSE_TAG + HTML_CLOSE_TAG
    return website

@app.get("/bytopic", response_class=HTMLResponse)
def showNewsByTopic(q: Optional[str] = None):
    reader = HackerNewsReader()

    if DEBUG == 0:
    # for debug purposes, loading all stories from a mock, instead of from Hackernews
        with open('example/mock_input.json') as json_file:
            all_stories = json.load(json_file)
    else:
        all_stories = reader.getStories(MAX_STORIES)
        # wrapping stories with json prefix and converting the return value to json
        all_stories = "{\"" + JSON_PREFIX + "\": " + json.dumps(all_stories) + "}"
    
    all_stories_as_json = json.loads(all_stories)

    filtered_stories = reader.filterStoriesTopics(all_stories, q)
    logger.debug("Done fetching, now filtering based on OPA policy")
    logger.debug("Done filtering, now printing filtered stories:")
    website = HTML_TAG + HEAD_TAG + TITLE_TAG + "Filtered HN" + TITLE_CLOSE_TAG + HEAD_CLOSE_TAG + BODY_TAG
    for item in filtered_stories:
        article = P_TAG + all_stories_as_json[JSON_PREFIX][item]["title"] + " " + "<a target=\"_blank\" href=\"" + \
        all_stories_as_json[JSON_PREFIX][item]["url"] + "\">read more</a>" + P_CLOSE_TAG
        article += TAB_SPACE + "&nbsp;&nbsp;&nbsp;" + str(all_stories_as_json[JSON_PREFIX][item]["score"]) + " upvotes"
        logger.debug(article)
        website += article + BR_TAG + BR_TAG

    website += BODY_CLOSE_TAG + HTML_CLOSE_TAG
    return website