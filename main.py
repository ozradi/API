#!/usr/bin/env python3

from typing import Optional
from fastapi import FastAPI
import json
from loguru import logger
from data_types.topics import topics
from hackernews_fetcher import HackerNewsReader
from fastapi.responses import HTMLResponse

from data_types.html_tags import HTML_TAGS

DEBUG = 1
MAX_STORIES = 30
JSON_PREFIX = "articles"
TITLE =  "Filtered HN"
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root(): 
    logger.debug("generating HTML started")
    website = HTML_TAGS.HTML_TAG + HTML_TAGS.HEAD_TAG + HTML_TAGS.TITLE_TAG + TITLE + HTML_TAGS.TITLE_CLOSE_TAG + HTML_TAGS.HEAD_CLOSE_TAG + HTML_TAGS.BODY_TAG
    website += HTML_TAGS.P_TAG + "Hello, world! Welcome to your Hackernews filter" + HTML_TAGS.P_CLOSE_TAG
    website += HTML_TAGS.P_TAG + "Want to see only liked articles? Simply change the route to include /popular (or " + HTML_TAGS.A_TAG_NEW_TAB + "/popular\">click here" + HTML_TAGS.A_CLOSE_TAG + ")" + HTML_TAGS.P_CLOSE_TAG
    website += HTML_TAGS.P_TAG + "Want to see articles on a specific topic? Simply change the route to include /bytopic?topic=" + HTML_TAGS.P_CLOSE_TAG
    website += HTML_TAGS.P_TAG + "Supported topics are: "
    counter = 0
    for topic in topics.list():
        link = HTML_TAGS.A_TAG + "/bytopic?topic=" + topic.lower() + "\">" + topic.lower() + HTML_TAGS.A_CLOSE_TAG
        logger.debug(link)
        website += link
        if counter < len(topics):
            website += ", "
            counter += 1
    website += HTML_TAGS.P_CLOSE_TAG
    website += HTML_TAGS.BODY_CLOSE_TAG + HTML_TAGS.HTML_CLOSE_TAG
    logger.debug("generating HTML ended")
    return website

@app.get("/popular", response_class=HTMLResponse)
def showNews():
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
    return generateHtml(filtered_articles, all_articles, "")

@app.get("/bytopic", response_class=HTMLResponse)
def showNewsByTopic(topic: Optional[str] = None):
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
    return generateHtml(filtered_article_ids, all_articles, topic)

def generateHtml(filtered_article_ids, all_articles, topic):
    logger.debug("generating HTML started")
    website_content = HTML_TAGS.HTML_TAG + HTML_TAGS.HEAD_TAG + HTML_TAGS.TITLE_TAG + TITLE + HTML_TAGS.TITLE_CLOSE_TAG + HTML_TAGS.HEAD_CLOSE_TAG + HTML_TAGS.BODY_TAG
    
    if filtered_article_ids == "" or len(filtered_article_ids) == 0:
        counter = 1
        website_content += "I didn't get articles on " + topic + "." + HTML_TAGS.BR_TAG + "Available topics: " 
        for topic in topics.list():
            link = HTML_TAGS.A_TAG + "/bytopic?topic=" + topic.lower() + "\">" + topic.lower() + HTML_TAGS.A_CLOSE_TAG
            website_content += link
            if counter < len(topics):
                website_content += ", "
                counter += 1
    elif filtered_article_ids == "Can't access OPA. Is it up?":
        website_content += filtered_article_ids
    else:
        for item in filtered_article_ids:
            currentArticle = all_articles[int(item)-1]
            currentUpvotes = "[" + str(currentArticle.score) + " upvotes] "
            currentLink = " " + HTML_TAGS.A_TAG_NEW_TAB + currentArticle.url + "\">Link" + HTML_TAGS.A_CLOSE_TAG if currentArticle.url != "N/A" else ""
            
            website_content += HTML_TAGS.P_TAG + currentUpvotes + currentArticle.title + currentLink + HTML_TAGS.P_CLOSE_TAG

    website_content += HTML_TAGS.A_TAG + "/\">home" + HTML_TAGS.A_CLOSE_TAG
    website_content += HTML_TAGS.BODY_CLOSE_TAG + HTML_TAGS.HTML_CLOSE_TAG
    logger.debug("Generating HTML ended")
    return website_content