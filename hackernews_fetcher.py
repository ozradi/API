from ast import Constant
import pip._vendor.requests 
import json
from loguru import logger
import requests

HACKER_NEWS_URL = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
HACKERNEWS_ID = "id"
HACKERNEWS_BY = "by"
HACKERNEWS_SCORE = "score"
HACKERNEWS_TITLE = "title"
HACKERNEWS_TIME = "time"
HACKERNEWS_TYPE = "type"
HACKERNEWS_URL = "url"
class HackerNewsReader():
    
    def getStories(self, maxStories):
        logger.debug("Start getting stories")
        r = pip._vendor.requests.get(HACKER_NEWS_URL)
        newstories = r.json()
        dataFromStories = {}
        numOfStories = min(len(newstories), maxStories)
        logger.debug("Fetching " + str(numOfStories) + " sotries. Iterating...")
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
            currentItemURL = currentAsJSON[HACKERNEWS_URL] if HACKERNEWS_URL in currentAsJSON else "http://www.google.com"

            dataFromStories[counter] = {
                HACKERNEWS_ID: currentItemId, 
                HACKERNEWS_TITLE: currentItemTitle, 
                HACKERNEWS_TIME: currentItemTime, 
                HACKERNEWS_SCORE: currentItemScore,
                HACKERNEWS_BY: currentItemBy,
                HACKERNEWS_TYPE: currentItemType,
                HACKERNEWS_URL: currentItemURL
                }
            counter += 1
            if counter-1 == numOfStories:
                break
        return dataFromStories

    def filterStories(self, input):
        logger.debug("Start filtering")

        storiesAsJson = input

        logger.debug("====Using the GET API to apply the policy on the data====")
        data = "{\"input\": " + storiesAsJson + "}"
        response = requests.post("http://localhost:8181/v1/data", data=data)
        filtered_articles = response.json()

        logger.debug("Completed filtering")
        return filtered_articles["result"]["example"]["popular_articles"]