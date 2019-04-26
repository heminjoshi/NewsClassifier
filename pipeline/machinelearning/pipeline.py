# Step 1 - Classify using Fake, vs Real dataset classifier
# Step 2 - Classify using Toxic vs Non Toxic dataset classifier
# Step 3 - News API
# Step 4 - Results

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

import sys
sys.path.insert(0, '../../api/')
from api.newsapi import newsapi

sys.path.insert(0, '../../model/')
from model.news import Article

MATCH_THRESHOLD = 70.0
class Pipeline(object) :
    def __init__(self, article, vectors, path) :
        # Set Article
        self.article = article

        # Set TF-IDF Vectors
        self.vectors = vectors

        # Set Root Path
        self.root = path

    def beginProcess(self) :
        # Classify on Real vs Fake classifier
        self.isRealResult = self.newsDatasetClassifier(self.article, self.vectors['news'])

        # Classify on Toxic vs Non Toxic Classifier
        self.isToxicResult = self.toxicDatasetClassifier(self.article, self.vectors["toxic"])

        # Get News matching current article and get the similarity scores. [If 1, then perfect match].
        self.similarity = self.getSimilarNews(self.article)

        return {"isReal" : self.isRealResult, "isToxic" : self.isToxicResult, "similarity" : self.similarity}
        

    def newsDatasetClassifier(self, article, vectorizer) :
        # Load Model
        model = pickle.load(open(str(self.root + "/models/News/NB/news_model-2.pl"),"rb"))

        # Vectorize
        text = vectorizer.transform([article.content])

        # Predict
        result = model.predict(text)[0]

        # Return Result (Mapped from numeric to text)
        if result == 0 : return 'Fake'
        else : return 'Real'

    def toxicDatasetClassifier(self, article, vectorizer) :
        # Load Model
        model = pickle.load(open(str(self.root + "/models/Toxic/model-1.toxic"),"rb"))

        # Vectorize
        text = vectorizer.transform([article.content])

        # Predict
        result = model.predict(text)[0]

        # Return Result (Mapped from numeric to text)
        if result == 0 : return "Not Toxic"
        else : return "Toxic"

    def getSimilarNews(self, article) :
        # Get all the similar news articles
        response = newsapi().get_news(article.title, article.date)['articles']

        if not response or len(response) == 0 :
            return 'No match found'

        # Convert them to Article() object
        articleObjects = []
        for eachArticle in response:
            # If any empty news received, then do not add.
            if not eachArticle['content'] :
                continue
            # Create Article object
            articleObject = Article()

            # Assign current article JSON to this article object
            articleObject.setFromJSON(eachArticle)
            
            # Add the article object to list of all article objects
            articleObjects.append(articleObject)

        # Similarity Memo
        similarity = {}
        
        # Iterate over article objects
        for eachArticle in articleObjects :
            
            # Build a TF-IDF for testing article and current (iterating) article
            tfidf = TfidfVectorizer().fit_transform([eachArticle.content, article.content])
            
            # Generate Score
            similarity[eachArticle] = (tfidf * tfidf.T).A

        # Find the article that has highest match with test article
        maxMatchScore , maxMatchArticle = -1, None

        for k,v in similarity.items():

            score = sum(v.flatten())

            if score > maxMatchScore :
                maxMatchScore = score
                maxMatchArticle = k
            
        if not maxMatchArticle :
            self.isRealResult = 'Fake'
            return 'No match found'

        # if maxMatchScore * 25 < MATCH_THRESHOLD :
            # self.isRealResult = 'Fake'

        return str(round(maxMatchScore * 25, 2)) + "% match with article : " + str(maxMatchArticle.url)
       

        


