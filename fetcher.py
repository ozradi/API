#!/usr/bin/env python3

import json
from loguru import logger
from hackernews_fetcher import HackerNewsReader

DEBUG = 1

if __name__ == "__main__":
    reader = HackerNewsReader()

    # for debug purposes, loading all stories from a mock, instead of from Hackernews
    if DEBUG == 0:
        with open('example/mock_input.json') as json_file:
            all_stories = json.load(json_file)
    else:
        all_stories = reader.getStories()
        all_stories = "{\"articles\": " + json.dumps(all_stories) + "}"

    logger.debug(all_stories)

    logger.debug("done loading, now filtering")
    filtered_stories = reader.filterStories(all_stories)

    logger.debug(filtered_stories)

    all_stories_as_json = json.loads(all_stories)
    for item in filtered_stories:
        logger.debug(all_stories_as_json["articles"][item])