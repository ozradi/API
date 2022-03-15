# import data.utils
package example

# Example - https://play.openpolicyagent.org/p/ioxt45pdrG
# Example - https://play.openpolicyagent.org/p/yI54xspChS

releavant_to_biology[articles]{
	some count
	title_lower = lower(input[count].title)
    some data_part
    contains(title_lower, data.biology[data_part])
    articles := count
}

relevant_to_crypto[articles]{
	some count
	title_lower = lower(input[count].title)
    some data_part
    contains(title_lower, data.crypto[data_part])
    articles := count
}

relevant_to_space[articles]{
	some count
	title_lower = lower(input[count].title)
    some data_part
    contains(title_lower, data.space[data_part])
    articles := count
}

relevant_to_tfaang[articles]{
	some count
	title_lower = lower(input[count].title)
    some data_part
    contains(title_lower, data.tfaang[data_part])
    articles := count
}

popular_articles[results] {
	some article
    input.articles[article].score >= 100
	results := article
}
