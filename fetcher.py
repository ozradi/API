#!/usr/bin/env python3

import json
from loguru import logger
from hackernews_fetcher import HackerNewsReader

if __name__ == "__main__":
    reader = HackerNewsReader()

    #for debug purposes, loading all stories from a mock, instead of from Hackernews
    with open('example/mock_input.json') as json_file:
        all_stories = json.load(json_file)
    # all_stories = reader.getStories()

    with open('example/mock_data.json') as json_file:
        dataFormat = json.load(json_file)

    # with open('example/mock_data.json') as json_file:
    #     dataFormat = json.load(json_file)
    policy = "package example popular_articles[results] { some article; input.articles[article].score >= 100; results := article}"

    # logger.debug(policy)
    # logger.debug(dataFormat)
    # logger.debug(all_stories)
    logger.debug("done loading, now filtering")
    filtered_stories = reader.filterStories(dataFormat, all_stories, policy)