from flask import Flask, request, render_template
import sklearn
import pickle
import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/predict", methods=["POST"])
def predict():
    # loading the dataset
    data = pd.read_csv("LanguageDetection.csv")
    y = data["Language"]

    # label encoding
    y = le.fit_transform(y)

    # loading the model and cv
    model = pickle.load(open("model.pkl", "rb"))
    cv = pickle.load(open("transform.pkl", "rb"))

    if request.method == "POST":
        # taking the input
        text = request.form["text"]
        # preprocessing the text
        text = re.sub(r'[!@#$(),\n"%^*?\:;~`0-9]', '', text)
        text = re.sub(r'[[]]', '', text)
        text = text.lower()
        dat = [text]
        # creating the vector
        vect = cv.transform(dat).toarray()
        
        # check if all elements in the vector are 0
        if np.all(vect == 0):
            my_pred = "unknown"
        else:
            # prediction
            my_pred = model.predict(vect)
            my_pred = le.inverse_transform(my_pred)[0]

    return render_template("home.html", pred="The above text is in {}".format(my_pred))

if __name__ == "__main__":
    app.run(debug=True)