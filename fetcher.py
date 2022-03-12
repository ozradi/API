#!/usr/bin/env python3

import json
from loguru import logger
from hackernews_fetcher import HackerNewsReader

DEBUG = 1
MAX_STORIES = 5
JSON_PREFIX = "articles"

if __name__ == "__main__":
    reader = HackerNewsReader()

    logger.debug("Fetching articles")

    if DEBUG == 0:
        # for debug purposes, loading all stories from a mock, instead of from Hackernews
        with open('example/mock_input.json') as json_file:
            all_stories = json.load(json_file)
    else:
        all_stories = reader.getStories(MAX_STORIES)
        # wrapping stories with json prefix and converting the return value to json
        all_stories = "{\"" + JSON_PREFIX + "\": " + json.dumps(all_stories) + "}"

    logger.debug("Done fetching, now filtering based on OPA policy")
    filtered_stories = reader.filterStories(all_stories)
    logger.debug("Done filtering, now printing filtered stories:")

    all_stories_as_json = json.loads(all_stories)
    for item in filtered_stories:
        logger.debug(all_stories_as_json[JSON_PREFIX][item])