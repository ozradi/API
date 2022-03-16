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
            all_articles = json.load(json_file)
    else:
        all_articles = reader.getArticles(MAX_STORIES)
    
    logger.debug("Done fetching, now filtering based on OPA policy")
    filtered_articles = reader.filterArticlesPopularity(all_articles)
    
    logger.debug("Done filtering, now printing filtered stories")
    return generateHtml(filtered_articles, all_articles, "")

@app.get("/bytopic", response_class=HTMLResponse)
def showNewsByTopic(q: Optional[str] = None):
    reader = HackerNewsReader()

    if DEBUG == 0:
    # for debug purposes, loading all stories from a mock, instead of from Hackernews
        with open('example/mock_input.json') as json_file:
            all_articles = json.load(json_file)
    else:
        all_articles = reader.getArticles(MAX_STORIES)
    
    logger.debug("Done fetching, now filtering based on OPA policy")
    filtered_articles = reader.filterArticlesTopics(all_articles, q)
    
    logger.debug("Done filtering, now printing filtered stories:")
    return generateHtml(filtered_articles, all_articles, q)

def generateHtml(content, all_articles, q):
    logger.debug("generating HTML started")
    website = HTML_TAG + HEAD_TAG + TITLE_TAG + "Filtered HN" + TITLE_CLOSE_TAG + HEAD_CLOSE_TAG + BODY_TAG
    
    logger.debug(all_articles)
    if content == "":
        website += "didn't find articles on your topic " + q
    else:
        for item in content:
            logger.debug(item)
            currentArticle = all_articles[int(item)-1]
            link = " <a target=\"_blank\" href=\"" + currentArticle.url + "\">read more</a>" if currentArticle.url != "N/A" else ""
            upvotes = "[" + str(currentArticle.score) + " upvotes] "
            
            website += P_TAG + upvotes + currentArticle.title + link + P_CLOSE_TAG + BR_TAG

    website += BODY_CLOSE_TAG + HTML_CLOSE_TAG
    logger.debug("generating HTML ended")
    return website