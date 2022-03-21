# import data.utils
package example

# Example - https://play.openpolicyagent.org/p/ioxt45pdrG
# Example - https://play.openpolicyagent.org/p/yI54xspChS

popular_articles[results] {
	some article_id
    input.articles[article_id].score >= 100
	results := article_id
}

releavant_to_biology[articles]{
	some article_id
	title_lower = lower(input.articles[article_id].title)
    some data_part
    contains(title_lower, data.biology[data_part])
    articles := article_id
}

relevant_to_crypto[articles]{
	some article_id
	title_lower = lower(input.articles[article_id].title)
    some data_part
    contains(title_lower, data.crypto[data_part])
    articles := article_id
}

relevant_to_space[articles]{
	some article_id
	title_lower = lower(input.articles[article_id].title)
    some data_part
    contains(title_lower, data.space[data_part])
    articles := article_id
}

relevant_to_faang[articles]{
	some article_id
	title_lower = lower(input.articles[article_id].title)
    some faang_item
    contains(title_lower, data.faang[data_part])
    articles := article_id
}

relevant_to_topic[topic]{
    some article_id
	title_lower = lower(input.articles[article_id].title)
    some item
    contains(title_lower, data[topic][item])
    articles := article_id
}