from dataclasses import dataclass
import json
from json import JSONEncoder


@dataclass
class Article:
    HACKERNEWS_ID = "id"
    HACKERNEWS_BY = "by"
    HACKERNEWS_SCORE = "score"
    HACKERNEWS_TITLE = "title"
    HACKERNEWS_TIME = "time"
    HACKERNEWS_TYPE = "type"
    HACKERNEWS_URL = "url"
    id = by = score = title = time = type = url = ""

    def __init__(self, currentItemId, currentItemBy, currentItemScore, currentItemTitle, currentItemTime, currentItemType, currentItemURL):
        self.id = currentItemId
        self.by = currentItemBy
        self.score = currentItemScore
        self.title = currentItemTitle
        self.time = currentItemTime
        self.type = currentItemType
        self.url = currentItemURL        

# subclass JSONEncoder
class ArticleEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Article):
            return {
                Article.HACKERNEWS_ID:    o.id,
                Article.HACKERNEWS_BY:    o.by,
                Article.HACKERNEWS_SCORE: o.score,
                Article.HACKERNEWS_TITLE: o.title,
                Article.HACKERNEWS_TIME:  o.time,
                Article.HACKERNEWS_TYPE:  o.type,
                Article.HACKERNEWS_URL:   o.url
            }
        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)