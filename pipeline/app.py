# Flask Imports
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

# Custom Imports 
# 'model' folder contains all the custom classes (This is the model in MVC architecture)
from model.news import Article

# 'machinelearning' folder contains all the ML Models and Pipeline code
from machinelearning.pipeline import Pipeline

# Imports to help load the vectors and models
import pickle
from sklearn.externals import joblib

# MUST be initialized when the server loads up.
# Please do not destroy or overwrite. (check __main__)
vectors = {"news" : None, "toxic" : None}

app = Flask(__name__)

# Path
PATH = app.root_path

# Home Page
@app.route("/")
def index():
    # articles = pickle.load(open("../articles.pl","rb"))
    # p = Pipeline(articles[0], vectors, PATH)
    # print(p.beginProcess())
    return render_template("index.html")

# Classifier Function
@app.route('/classify', methods=['POST'])
def handle_data():
    article = Article()

    article.setTitle(request.form['title'])
    article.setBody(request.form['content'])
    
    if 'date' in request.form : article.setPublishDate(request.form['date'])
    if 'source' in request.form : article.setSource(request.form['source'])
    if 'author' in request.form : article.setAuthor(request.form['author'])

    p = Pipeline(article, vectors, PATH)
    result = p.beginProcess()
    resultString = "Fake vs Real Classifer Result: <b><i>" +result["isReal"] + "</b></i><br> Toxicity Classifier Result: <b><i>" + result['isToxic'] + "</b></i><br> Similarity Measure: <b><i>" + result['similarity'] + "</b></i>"
    return render_template("result.html",result = resultString);


# Main Function
if __name__ == "__main__":
    
    PATH = PATH.split("/")
    PATH.pop()
    PATH = '/'.join(PATH)
    PATH = 'D:/Academic/Data Science/NewsClassifier'
    print("PATH:" + PATH)
    vectors['news'] = pickle.load(open(str(PATH + '/vectors/News/vector-2.pl'),"rb"))
    vectors['toxic'] = pickle.load(open(str(PATH + '/vectors/Toxic/vector-1.toxic'),"rb"))

    app.run()
   
