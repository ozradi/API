#!/usr/bin/env python3

from typing import Optional
from fastapi import FastAPI
import json
from loguru import logger
from article import Article
from hackernews_fetcher import HackerNewsReader
from fastapi.responses import HTMLResponse

DEBUG = 1
MAX_STORIES = 3
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
JSON_PREFIX = "articles"

app = FastAPI()

@app.get("/")
def read_root(): 
    return {"hello, world"}

@app.get("/more_than_100", response_class=HTMLResponse)
def showNews():
    reader = HackerNewsReader()
    if DEBUG == 0:
    # for debug purposes, loading all stories from a mock, instead of from Hackernews
        with open('example/mock_input.json') as json_file:
            all_stories = json.load(json_file)
    else:
        all_stories = reader.getArticles(MAX_STORIES)
    
    logger.debug("Done fetching, now filtering based on OPA policy")
    filtered_stories = reader.filterArticlesPopularity(all_stories)
    
    logger.debug("Done filtering, now printing filtered stories")
    website = HTML_TAG + HEAD_TAG + TITLE_TAG + "Filtered HN" + TITLE_CLOSE_TAG + HEAD_CLOSE_TAG + BODY_TAG
    logger.debug("All stories")
    logger.debug(all_stories)
    # all_stories_as_json = json.loads(all_stories)
    
    # logger.debug(all_stories_as_json)
    for item in filtered_stories:
        currentArticle = all_stories[int(item)]
        link = " <a target=\"_blank\" href=\"" + currentArticle.url + "\">read more</a>" if currentArticle.url != "N/A" else ""
        upvotes = "[" + str(currentArticle.score) + " upvotes] "
        
        website += P_TAG + upvotes + currentArticle.title + link + P_CLOSE_TAG + BR_TAG

    website += BODY_CLOSE_TAG + HTML_CLOSE_TAG
    return website

@app.get("/bytopic", response_class=HTMLResponse)
def showNewsByTopic(q: Optional[str] = None):
    reader = HackerNewsReader()

    if DEBUG == 0:
    # for debug purposes, loading all stories from a mock, instead of from Hackernews
        with open('example/mock_input.json') as json_file:
            all_articles = json.load(json_file)
    else:
        all_articles = reader.getArticles(MAX_STORIES)
        # wrapping stories with json prefix and converting the return value to json
        all_articles = "{\"" + JSON_PREFIX + "\": " + json.dumps(all_articles) + "}"
    
    all_stories_as_json = json.loads(all_articles)

    filtered_stories = reader.filterArticlesTopics(all_articles, q)

    logger.debug("Done fetching, now filtering based on OPA policy")
    logger.debug("Done filtering, now printing filtered stories:")
    website = HTML_TAG + HEAD_TAG + TITLE_TAG + "Filtered HN" + TITLE_CLOSE_TAG + HEAD_CLOSE_TAG + BODY_TAG
    if filtered_stories == "":
        website += "didn't find articles on your topic " + q
    else:
        for item in filtered_stories:
            article = P_TAG + all_stories_as_json[JSON_PREFIX][item]["title"] + " " + "<a target=\"_blank\" href=\"" + \
            all_stories_as_json[JSON_PREFIX][item]["url"] + "\">read more</a>" + P_CLOSE_TAG
            article += "&nbsp;&nbsp;&nbsp;" + str(all_stories_as_json[JSON_PREFIX][item]["score"]) + " upvotes"
            logger.debug(article)
            website += article + BR_TAG + BR_TAG

    website += BODY_CLOSE_TAG + HTML_CLOSE_TAG
    return website