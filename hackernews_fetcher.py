from ast import Constant
from unittest import case
from attr import asdict
import pip._vendor.requests 
import json
from loguru import logger
import requests
from article import Article, ArticleEncoder
import topics

HACKER_NEWS_URL = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
HACKERNEWS_ID = "id"
HACKERNEWS_BY = "by"
HACKERNEWS_SCORE = "score"
HACKERNEWS_TITLE = "title"
HACKERNEWS_TIME = "time"
HACKERNEWS_TYPE = "type"
HACKERNEWS_URL = "url"
JSON_PREFIX = "articles"

class HackerNewsReader():
    
    def getArticles(self, maxArticles):
        logger.debug("Start getting articles")
        r = pip._vendor.requests.get(HACKER_NEWS_URL)
        newstories = r.json()
        articles = []
        numOfStories = min(len(newstories), maxArticles)
        logger.debug("Fetching " + str(numOfStories) + " articles. Iterating...")
        counter = 1
        for item in newstories:
            currentItemId = currentItemBy = currentItemScore = currentItemTitle = currentItemTime = currentItemType = currentItemURL = ""
            url = "https://hacker-news.firebaseio.com/v0/item/" + str(item) + ".json?print=pretty"
            current = pip._vendor.requests.get(url)
            currentAsJSON = json.loads(current.text)
            currentItemId = currentAsJSON[HACKERNEWS_ID] if HACKERNEWS_ID in currentAsJSON else 0
            currentItemBy = currentAsJSON[HACKERNEWS_BY] if HACKERNEWS_BY in currentAsJSON else "Unknown"
            currentItemScore = currentAsJSON[HACKERNEWS_SCORE] if HACKERNEWS_SCORE in currentAsJSON else 0
            currentItemTitle = currentAsJSON[HACKERNEWS_TITLE] if HACKERNEWS_TITLE in currentAsJSON else ""
            currentItemTime = currentAsJSON[HACKERNEWS_TIME] if HACKERNEWS_TIME in currentAsJSON else ""
            currentItemType = currentAsJSON[HACKERNEWS_TYPE] if HACKERNEWS_TYPE in currentAsJSON else ""
            currentItemURL = currentAsJSON[HACKERNEWS_URL] if HACKERNEWS_URL in currentAsJSON else "N/A"

            articles.append(Article(currentItemId, currentItemBy,currentItemScore,currentItemTitle,currentItemTime,currentItemType,currentItemURL))
            counter += 1
            if counter-1 == numOfStories:
                break
        return articles

    def filterArticlesPopularity(self, input):
        logger.debug("Start filtering based on popularity")

        # wrapping stories with json prefix and converting the return value to json
        articlesAsJson = "{\"" + JSON_PREFIX + "\": {"
        counter = 1
        for item in input:
            itemAsJson = ArticleEncoder().encode(item)
            if counter < len(input):
                itemAsJson += ","
            articlesAsJson += "\"" + str(counter) + "\":" + itemAsJson
            counter += 1
        articlesAsJson += "}}"

        logger.debug("====Using the GET API to apply the policy on the data====")
        data = "{\"input\": " + articlesAsJson + "}"
        # logger.debug("This is the data sent to opa: " + data)
        response = requests.post("http://localhost:8181/v1/data", data=data)
        filtered_articles = response.json()

        # logger.debug("Completed filtering with " + str(filtered_articles))
        logger.debug("Completed filtering")
        return filtered_articles["result"]["example"]["popular_articles"]

    def filterArticlesTopics(self, input, topic):
        logger.debug("Start filtering based on topics: " + topic)

        if topic == 1:
            with open('example/data.json') as json_file:
                data = json.load(json_file)["biology"]
        elif topic == 2:
            with open('example/data.json') as json_file:
                data = json.load(json_file)["crypto"]
        elif topic == 3:
            with open('example/data.json') as json_file:
                data = json.load(json_file)["space"]
        elif topic == 4:
            with open('example/data.json') as json_file:
                data = json.load(json_file)["tfaang"]
        else: 
            data = ""
            
        storiesAsJson = input

        logger.debug("====Using the GET API to apply the policy on the data====")
        input = "{\"input\": " + storiesAsJson + "}"
        if data != "":
            data_for_opa = {input, data} 
        else: 
            data_for_opa = input
        response = requests.post("http://localhost:8181/v1/data", data_for_opa)
        filtered_articles = response.json()

        logger.debug("Completed filtering")
        logger.debug(filtered_articles["result"]["example"])
        topic_tag = "relevant_to_" + topic
        if topic_tag in filtered_articles["result"]["example"]:
            logger.debug("Found articles on " + topic)
            return filtered_articles["result"]["example"][topic_tag]
        else:
            logger.debug("didn't get articles on " + topic)
            return ""