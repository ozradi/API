#!/usr/bin/env python3

from re import template
from typing import Optional
from fastapi import FastAPI, Request
import json
from loguru import logger
from data_types.topics import topics
from hackernews_fetcher import HackerNewsReader
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

DEBUG = 1
MAX_STORIES = 10
JSON_PREFIX = "articles"
TITLE =  "Filtered HN"
app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request): 
    return templates.TemplateResponse("homepage.html", {"request": request, "topics": topics.list()})

@app.get("/popular", response_class=HTMLResponse)
def showNews(request: Request):
    reader = HackerNewsReader()
    if DEBUG == 0:
    # for debug purposes, loading all stories from a mock, instead of from Hackernews
        with open('opa_files/mock_input.json') as json_file:
            all_articles = json.load(json_file)
    else:
        all_articles = reader.getArticles(MAX_STORIES)
    
    logger.debug("Done fetching, now filtering based on OPA policy")
    filtered_articles = reader.filterArticlesPopularity(all_articles)
    
    logger.debug("Done filtering, now printing filtered stories")
    return generateHtml(request, filtered_articles, all_articles, "")

@app.get("/bytopic", response_class=HTMLResponse)
def showNewsByTopic(request: Request, topic: Optional[str] = None):
    reader = HackerNewsReader()

    if DEBUG == 0:
    # for debug purposes, loading all stories from a mock, instead of from Hackernews
        with open('opa_files/mock_input.json') as json_file:
            all_articles = json.load(json_file)
    else:
        all_articles = reader.getArticles(MAX_STORIES)
    
    logger.debug("Done fetching, now filtering based on OPA policy")
    filtered_article_ids = reader.filterArticlesTopics(all_articles, topic)
    
    logger.debug("Done filtering, now printing filtered stories:")
    return generateHtml(request, filtered_article_ids, all_articles, topic)

def generateHtml(request, filtered_article_ids, all_articles, topic):
    logger.debug("generating HTML started")
    displayArticles = []
    templateResponse = ""
    if filtered_article_ids == "" or len(filtered_article_ids) == 0:
        error = "I didn't get articles on " + topic + ". 😔" 
        templateResponse = templates.TemplateResponse("not_found.html", {"request": request, "error": error, "topics": topics.list()})
    elif filtered_article_ids == "Can't access OPA. Is it up?":
        error = "Can't access OPA. Is it up?"
        templateResponse = templates.TemplateResponse("not_found.html", {"request": request, "error": error, "topics": topics.list()})
    else:
        logger.debug("got results")
        for item in filtered_article_ids:
            displayArticles.append(all_articles[int(item)-1])
        templateResponse = templates.TemplateResponse("results.html", {"request": request, "articles": displayArticles})

    logger.debug("generating HTML ended")
    return templateResponse