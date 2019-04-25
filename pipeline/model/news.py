class Article(object) :
    def __init__(self) :
        pass

    # News Headline/Title
    def setTitle(self, title) :
        self.title = title

    # News Content/Body
    def setBody(self, content) :
        self.content = content
    
    # Date at which this article was published
    def setPublishDate(self, date) :
        self.date = date
    
    # Author of this news article.
    def setAuthor(self, author) : 
        self.author = author

    # Source of this Article (Example : bbc)
    def setSource(self, source) :
        self.source = source

    # Set the URL
    def setArticleURL(self, url) :
        self.url = url
    
    def describe(self) :
        print("")

    def setFromJSON(self, article):
        self.setSource(article['source']['name'])
        self.setAuthor(article['author'])
        self.setTitle(article['title'])
        self.setBody(article['content'])
        self.setPublishDate(article['publishedAt'])
        self.setArticleURL(article['url'])
