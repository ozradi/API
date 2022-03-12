import pip._vendor.requests 
import json
from loguru import logger
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

    def filterStories(self, data, input, policy):
        logger.debug("start filtering")

        # queryDataUrl = "http://localhost:8181/v1/data/articles"
        # urlForData = os.environ.get("OPA_URL", queryDataUrl)
        # logger.debug("OPA query data URL: " + urlForData)        
        # response = requests.put(urlForData, data=storiesAsJson)
        # logger.debug(response)
        # logger.debug(response.content)

        storiesAsJson = json.dumps(input)

        logger.debug("====inserting policy to OPA====")
        response = requests.put("http://localhost:8181/v1/policies/example", policy, headers={'content-type':'text/plain'})

        logger.debug("====inserting input data in data/system/main path====")
        data = "{\"input\": " + storiesAsJson + "}"

        logger.debug("====Using the GET API to apply the policy on the data====")
        response = requests.post("http://localhost:8181/v1/data", data=data)
        logger.debug(response)
        filtered_articles = response.json()

        logger.debug("completed filtering")
        logger.debug(filtered_articles)
        # logger.debug(filtered_articles['example'])
        return filtered_articles