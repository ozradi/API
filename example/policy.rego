# import data.utils
package example

# Example - https://play.openpolicyagent.org/p/ioxt45pdrG

popular_articles[results] {
	some article
    input.articles[article].score >= 100
	results := article
}