Description
================================================================================
This crawler/server will crawl the BBC website (bbc.com) and serve up the resulting articles via a RESTful api,
which allows retrieval of all articles, as well as retrieval of articles by words occurring in the body.

BBCSpider crawls the bbc front page to scrape articles, and then follows the article links to scrape additional data
(the article header and body). The data is stored via the IndexerPipeline and MongoWriterPipeline pipeline stages using
a bulk query (initially it was doing individual queries and bringing up a new mongo connection each time; that did not
go well...).

While MongoWriterPipeline simply stores article data in the 'articles' collection, the IndexerPipeline creates an index
(stored in 'words') by mapping the words occuring in the body of an article to the article's url via the following structure:
{
    'word': 'someWord',
    'urls': ['http://www.articleContainingWord.com', 'http://www.anotherArticleContainingWord.com', ...]
}
A result retrieved from the index can then be used to look up relevant articles in 'articles' by their url.

When indexing, words are added to url arrays via '$addToSet' so re-running the spider will add to the existing collections
and index rather than overwriting them. In prod, the spider could be run every day as a cron job.

In terms of cleaning the page of ads, that did not seem necessary as the crawler uses xpath to extract the body of articles
which appear clear of advertising content.

To use the spider in 'local' mode, a server should be serving up a local version of the bbc website at localhost:8090.
I use http-server to serve the local site, and I used a Firefox plugin to download the site (following to a depth of
one link) but the result turned out to be too large to include in the repo. A remaining todo is to see whether clearing
out irrelevant content such as images will make the size more manageable for the repo.

My python skills are fairly rudimentary, so pardon any non-idiomatic use. Due to time limitations the test suite is far
smaller than I would like, for production code I would usually unit test each class and then do at least one end-to-end
test, and usually also some smaller integration tests between the more important components. If I get the time I'll add
some more tests over the coming days; my unfamiliarity with Python and the test framework have made the work a bit tougher
(still haven't figured out how to mock a 'self' reference, even with unittest's @patch.


Usage
================================================================================
- To switch from crawl-local (using ./bbcsite to crawl) to remote (crawling bbc.com) manually replace start_urls in BBCSpider.py.
    Better alternative coming soon.

- To switch from local mongodb (default port etc) to the compose.io version or vice versa, comment in the appropriate
    file in './config/environment.cfg'. (Yep, the password for my trial account db is out on github, heh). Prod = compose.io

- Run the crawler: crawlBBC

- Run the server: startServer

- Run the tests:

- RESTful calls:
> GET http://localhost:8091/articles
    returns all articles crawled (warning, this could be big)
> GET http://localhost:8091/articles/words
    returns all words in the index (words that have been found in articles) and the urls in which they occur
> GET http://localhost:8091/articles/words/{word}
    returns all articles for the provided word (should probably be "/articles?word={word}" instead)
