from ast import Constant
import pip._vendor.requests 
import json
from loguru import logger
import requests

MAX_STORIES = 5
class HackerNewsReader():

    def getStories(self):
        logger.debug("start")
        r = pip._vendor.requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
        newstories = r.json()
        dataFromStories = {}
        numOfStories = min(len(newstories), MAX_STORIES)
        logger.debug("fetching " + str(numOfStories) + " sotries. Iterating...")
        counter = 1
        for item in newstories: 
            url = "https://hacker-news.firebaseio.com/v0/item/" + str(item) + ".json?print=pretty"
            current = pip._vendor.requests.get(url)
            currentAsJSON = json.loads(current.text)
            currentItemId = currentAsJSON["id"]
            currentItemBy = currentAsJSON["by"]
            currentItemScore = currentAsJSON["score"]
            currentItemTitle = currentAsJSON["title"]
            currentItemTime = currentAsJSON["time"]
            currentItemType = currentAsJSON["type"]
            currentItemURL = currentAsJSON["url"]

            dataFromStories[counter] = {
                "id": currentItemId, 
                "title": currentItemTitle, 
                "time": currentItemTime, 
                "score": currentItemScore,
                "by": currentItemBy,
                "type": currentItemType,
                "url": currentItemURL
                }
            counter += 1
            if counter-1 == numOfStories:
                break
        return dataFromStories

    def filterStories(self, input):
        logger.debug("start filtering")

        storiesAsJson = input

        logger.debug("====Using the GET API to apply the policy on the data====")
        data = "{\"input\": " + storiesAsJson + "}"
        response = requests.post("http://localhost:8181/v1/data", data=data)
        logger.debug(response)
        filtered_articles = response.json()

        logger.debug("completed filtering")
        return filtered_articles["result"]["example"]["popular_articles"]