import requests
import json
from loguru import logger
from data_types.article import Article, ArticleEncoder
from data_types.topics import topics
from opa_files.opa_tags import OPA_TAGS

HACKER_NEWS_URL = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
ARTICLES_PREFIX = "articles"
HACKER_NEWS_ARTICLE_URL = "https://hacker-news.firebaseio.com/v0/item/XXX.json?print=pretty"
HACKER_NEWS_ARTICLE_PLACEHOLDER = "XXX"
class HackerNewsReader():
    
    def getArticle(self, item):
        logger.debug("Start getting article: " + str(item))
        currentItemId = currentItemBy = currentItemScore = currentItemTitle = currentItemTime = currentItemType = currentItemURL = ""
        url = HACKER_NEWS_ARTICLE_URL.replace(HACKER_NEWS_ARTICLE_PLACEHOLDER, str(item))
        current = requests.get(url)
        currentAsJSON = json.loads(current.text)
        currentItemId = currentAsJSON[Article.HACKERNEWS_ID] if Article.HACKERNEWS_ID in currentAsJSON else 0
        currentItemBy = currentAsJSON[Article.HACKERNEWS_BY] if Article.HACKERNEWS_BY in currentAsJSON else "Unknown"
        currentItemScore = currentAsJSON[Article.HACKERNEWS_SCORE] if Article.HACKERNEWS_SCORE in currentAsJSON else 0
        currentItemTitle = currentAsJSON[Article.HACKERNEWS_TITLE] if Article.HACKERNEWS_TITLE in currentAsJSON else ""
        currentItemTime = currentAsJSON[Article.HACKERNEWS_TIME] if Article.HACKERNEWS_TIME in currentAsJSON else ""
        currentItemType = currentAsJSON[Article.HACKERNEWS_TYPE] if Article.HACKERNEWS_TYPE in currentAsJSON else ""
        currentItemURL = currentAsJSON[Article.HACKERNEWS_URL] if Article.HACKERNEWS_URL in currentAsJSON else "N/A"
        return Article(currentItemId, currentItemBy,currentItemScore,currentItemTitle,currentItemTime,currentItemType,currentItemURL)

    def getArticles(self, maxArticles):
        logger.debug("Start getting articles")
        stories_ids_list = requests.get(HACKER_NEWS_URL)
        newstories = stories_ids_list.json()
        articles = []
        numOfStories = min(len(newstories), maxArticles)
        logger.debug("Fetching " + str(numOfStories) + " articles. Iterating...")
        articlesCounter = 1
        for item in newstories:
            articles.append(self.getArticle(item))
            articlesCounter += 1
            if articlesCounter-1 == numOfStories:
                break
        logger.debug("ended getting articles")

        logger.debug(articles)
        
        # To return a new list, use the sorted() built-in function...
        articles = sorted(articles, key=lambda x: x.score, reverse=True)

        logger.debug(articles)
        return articles

    def queryOPA(self, input, data):
        logger.debug("====Using the GET API to apply the policy on the data====")
        
        # wrapping stories with json prefix
        inputAsJSON = "{\""+ OPA_TAGS.OPA_INPUT + "\": {\"" + ARTICLES_PREFIX + "\": {"
        counter = 1
        # converting the input to JSON, OPA's supported format
        for item in input:
            itemAsJson = ArticleEncoder().encode(item)
            if counter < len(input):
                itemAsJson += ","
            inputAsJSON += "\"" + str(counter) + "\":" + itemAsJson
            counter += 1
        
        inputAsJSON += "}}}"
        logger.debug(inputAsJSON)
        try:
            response = requests.post(OPA_TAGS.OPA_URL, inputAsJSON)
        except:
            logger.debug("Can't access OPA. Is it up?")
            return "Can't access OPA. Is it up?"
        if(response.status_code == 200):
            logger.debug("completed" + str(response.json()))
            return response.json()[OPA_TAGS.OPA_RESULT][OPA_TAGS.REGO_NAMESPACE]
        else:
            logger.debug("error querying OPA!")
            return "error querying OPA!"

    def filterArticlesPopularity(self, input):
        logger.debug("Start filtering based on popularity")

        filtered_articles = self.queryOPA(input, "")
        
        logger.debug("Completed filtering")
        if OPA_TAGS.OPA_POPULAR_ARTICLES in filtered_articles:
            return filtered_articles[OPA_TAGS.OPA_POPULAR_ARTICLES]
        return filtered_articles

    def filterArticlesTopics(self, input, topic):
        logger.debug("Start filtering based on topics: " + topic)

        with open(OPA_TAGS.OPA_DATA_FILE_PATH) as json_file:
            data = json.load(json_file)

        filtered_articles = self.queryOPA(input, data)
        
        logger.debug("Completed filtering")
        topic_tag = "relevant_to_" + topic
        if topic_tag in filtered_articles:
            logger.debug("Found articles on " + topic)
            return filtered_articles[topic_tag]
        else:
            no_results = "I didn't get articles on " + topic + ". Available topics: " + str(topics.list()).lower()
            logger.debug(no_results)
            return ""
