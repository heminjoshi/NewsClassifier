import requests
import sys
# Add path to model folder.
sys.path.insert(0, '../../model/')

# URL Class.
from model.url import URL

class newsapi(object) :
    def __init__(self, key = "7d10aefda84a4dca9afa6f6a6a1b863c") :
        self.key = key;
    
    # Get news that contains the 'query' for the given 'date'
    def get_news(self, query, date) :

        url = URL("https://newsapi.org/v2/everything?")

        if(query) : url.addParam(str("q=" + query + "&"))
        if(date) : url.addParam(str('from=' + date + '&'))
        
        url.addParam('sortBy=popularity&language=en&')
        url.addParam('apiKey=' + self.key)

        return requests.get(url.toString()).json()
    
    # Get list of reliable sources
    def get_sources(self) :
        url = "https://newsapi.org/v2/sources?language=en&apiKey=" + self.key
        return requests.get(url).json()