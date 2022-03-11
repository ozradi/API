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
        logger.debug("start filtering")
        # stories = "{\"articles\":{\"1\":{\"by\":\"1st story\",\"desendent\":123,\"id\":30634872,\"kids\":[30635556,30635791],\"score\":264,\"time\":1646960549,\"title\":\"Earn-IT threatens encryption and therefore user freedom\"}}}"
        stories = json.dumps(stories)

        url = os.environ.get("OPA_URL", "http://localhost:8181/")
        logger.debug("OPA query: " + url)
        response = requests.post(url, data=stories)
        logger.debug(response.reason)
        logger.debug("completed filtering")