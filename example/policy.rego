# import data.utils
package popular

# popular articles is a filtering rule:
# - As an input, the rule gets "results" which are the articles
# - Then, iterate all articles and check their score
# - If it's above the threshold, i.e. 100, adds the current article to the articles
# - Eventually, returns the filtered articles saved in the "results" param
# Example - https://play.openpolicyagent.org/p/ioxt45pdrG

popular_articles[results] {
	some article
    input.articles[article].score >= 100
	results := article
}