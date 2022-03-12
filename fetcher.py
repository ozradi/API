#!/usr/bin/env python3

import json
from loguru import logger
from hackernews_fetcher import HackerNewsReader

DEBUG = 1
MAX_STORIES = 5
JSON_PREFIX = "articles"

if __name__ == "__main__":
    reader = HackerNewsReader()

    # for debug purposes, loading all stories from a mock, instead of from Hackernews
    if DEBUG == 0:
        with open('example/mock_input.json') as json_file:
            all_stories = json.load(json_file)
    else:
        all_stories = reader.getStories(MAX_STORIES)
        all_stories = "{\"" + JSON_PREFIX + "\": " + json.dumps(all_stories) + "}"

    logger.debug("Done loading, now filtering")
    filtered_stories = reader.filterStories(all_stories)

    logger.debug(filtered_stories)

    all_stories_as_json = json.loads(all_stories)
    for item in filtered_stories:
        logger.debug(all_stories_as_json[JSON_PREFIX][item])