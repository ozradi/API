#!/usr/bin/env python3

import json
from loguru import logger
from hackernews_fetcher import HackerNewsReader

if __name__ == "__main__":
    reader = HackerNewsReader()
    # all_stories = reader.getStories()

    with open('example/mock_stories.json') as json_file:
        all_stories = json.load(json_file)

    logger.debug("done getting stories, filtering")
    filtered_stories = reader.filterStories(all_stories)