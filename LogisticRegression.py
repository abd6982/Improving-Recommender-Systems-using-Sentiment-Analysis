#Imports
import numpy as np
import pandas as pd
from nltk.corpus import stopwords, brown
from nltk.stem import PorterStemmer, WordNetLemmatizer
from bs4 import BeautifulSoup
import re
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

#Import IMDb labeled data for training the classifier
data = pd.read_csv('labeledTrainData.tsv', delimiter = '\t', quoting = 3)

#Drop id column
data.drop(['id'], axis = 1, inplace=True)

#Remove the HTML tags from text, convert text to lowercase and then remove all symbols and digits use RE
data["review"] = [re.sub("[^A-Za-z]", " ", BeautifulSoup(w, 'html.parser').get_text()).lower().split() for w in data["review"]]

#Remove stopwords and perform lemmatization to restore words to their root form
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
data["review"] = [[lemmatizer.lemmatize(w) for w in sentence if lemmatizer.lemmatize(w) not in stop_words] for sentence in data["review"]]
review_train = [" ".join(w) for w in data["review"]]

#Now we import the reviews fetched from IMDb for prediction
#We remove the unwanted column and assign column names
reviews = pd.read_csv('final.csv', encoding='latin-1')
reviews.drop(['Unnamed: 0'], axis = 1, inplace = True)
reviews.columns = np.array(['movie title', 'reviews'])
reviews = reviews[:1000]

#Remove symbols and digits from the text and convert them to lowercase
reviews["reviews"] = [re.sub("[^A-Za-z]", " ", ' '.join(w.split('\\n'))).lower().split() for w in reviews["reviews"]]

#Remove stopwords and perform lemmatization to restore words to their root form
reviews["reviews"] = [[lemmatizer.lemmatize(w) for w in sentence if lemmatizer.lemmatize(w) not in stop_words] for sentence in reviews["reviews"]]
review_test = [" ".join(w) for w in reviews["reviews"]]

#Join the training and test data to form bag of words with equal number of features
final_data = review_train + review_test

#Instantiate TfidfVectorizer for converting the text to a bag of words model and apply tfidf
vectorizer = TfidfVectorizer()

#Get the bag of words model
X = vectorizer.fit_transform(final_data)

#Get labels from data
y = data["sentiment"]

#Instantiate Logistic Regression Classifier
model = LogisticRegression()

#Train the classifier
model.fit(X[:25000], y)

#Perform classification and check accuracy
res = model.predict(X[:25000])
print(accuracy_score(res, y))
print(classification_report(res, y))

#Predict sentiment probabilities of the test data
senti = model.predict_proba(X[25000:])

#Write the probability of positive sentiment in a csv file
reviews["sentiment"] = pd.Series([x[1] for x in senti])
reviews.to_csv('sentiment_data_unigram.csv', index=False)

