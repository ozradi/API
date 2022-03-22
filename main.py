#!/usr/bin/env python3

from typing import Optional
from fastapi import FastAPI
import json
from loguru import logger
from hackernews_fetcher import HackerNewsReader
from fastapi.responses import HTMLResponse

from data_types.html_tags import HTML_TAGS

DEBUG = 1
MAX_STORIES = 30
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
def showNewsByTopic(topic: Optional[str] = None):
    reader = HackerNewsReader()

    if DEBUG == 0:
    # for debug purposes, loading all stories from a mock, instead of from Hackernews
        with open('example/mock_input.json') as json_file:
            all_articles = json.load(json_file)
    else:
        all_articles = reader.getArticles(MAX_STORIES)
    
    logger.debug("Done fetching, now filtering based on OPA policy")
    filtered_articles = reader.filterArticlesTopics(all_articles, topic)
    
    logger.debug("Done filtering, now printing filtered stories:")
    return generateHtml(filtered_articles, all_articles, topic)

def generateHtml(content, all_articles, topic):
    logger.debug("generating HTML started")
    website = HTML_TAGS.HTML_TAG + HTML_TAGS.HEAD_TAG + HTML_TAGS.TITLE_TAG + "Filtered HN" + HTML_TAGS.TITLE_CLOSE_TAG + HTML_TAGS.HEAD_CLOSE_TAG + HTML_TAGS.BODY_TAG
    
    logger.debug(all_articles)
    if content == "":
        website += "I didn't find articles on your topic: " + topic
    else:
        for item in content:
            currentArticle = all_articles[int(item)-1]
            upvotes = "[" + str(currentArticle.score) + " upvotes] "
            link = HTML_TAGS.A_TAG_NEW_TAB + currentArticle.url + "\">read more" + HTML_TAGS.A_CLOSE_TAG if currentArticle.url != "N/A" else ""
            
            website += HTML_TAGS.P_TAG + upvotes + currentArticle.title + link + HTML_TAGS.P_CLOSE_TAG + HTML_TAGS.BR_TAG

    website += HTML_TAGS.BODY_CLOSE_TAG + HTML_TAGS.HTML_CLOSE_TAG
    logger.debug("generating HTML ended")
    return website