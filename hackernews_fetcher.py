import pip._vendor.requests 
import json
from loguru import logger
import os
import requests

class HackerNewsReader():

    def getStories(self):
        logger.debug("start")
        r = pip._vendor.requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
        newstories = r.json()
        dataFromStories = {}
        numOfStories = min(len(newstories), 10)
        logger.debug("fetching " + str(numOfStories) + " sotries. Iterating...")
        counter = 0
        for item in newstories: 
            url = "https://hacker-news.firebaseio.com/v0/item/" + str(item) + ".json?print=pretty"
            # print("getting" + url)
            current = pip._vendor.requests.get(url)
            # print("text: " + current.text)
            currentAsJSON = json.loads(current.text)
            # print(currentAsJSON)
            currentItemId = currentAsJSON["id"]
            currentItemScore = currentAsJSON["score"]
            currentItemTitle = currentAsJSON["title"]
            currentItemTime = currentAsJSON["time"]

            dataFromStories[counter] = {currentItemId, currentItemTitle, currentItemTime, currentItemScore}
            logger.debug("now as JSON")
            logger.debug(currentAsJSON)
            counter+=1
            if counter == numOfStories:
                break
        logger.debug("test")
        # logger.debug(currentAsJSON)
        return dataFromStories

    def filterStories(self, stories):
        # counter = 1
        logger.debug("start filtering")
        # logger.debug(stories)
        
        url = os.environ.get("OPA_URL", "http://localhost:8181")
        logger.debug("OPA query: ")
        logger.debug(url)
        response = requests.post(url, data=stories)
        logger.debug(response.json)
        logger.debug(response._content)
        logger.debug("completed filtering")
