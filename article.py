from dataclasses import dataclass
import json
from json import JSONEncoder

from loguru import logger

JSON_PREFIX = "articles"
HACKERNEWS_ID = "id"
HACKERNEWS_BY = "by"
HACKERNEWS_SCORE = "score"
HACKERNEWS_TITLE = "title"
HACKERNEWS_TIME = "time"
HACKERNEWS_TYPE = "type"
HACKERNEWS_URL = "url"

@dataclass
class Article:
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
                HACKERNEWS_ID:    o.id,
                HACKERNEWS_BY:    o.by,
                HACKERNEWS_SCORE: o.score,
                HACKERNEWS_TITLE: o.title,
                HACKERNEWS_TIME:  o.time,
                HACKERNEWS_TYPE:  o.type,
                HACKERNEWS_URL:   o.url
            }
        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)