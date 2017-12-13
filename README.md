# Improving-Recommender-Systems-using-Sentiment-Analysis
This project is aimed at Improving Item-based Collaborative Filtering System using Sentiment Analysis of user reviews.
The collaborative filtering system uses a similarity score to find the best recommendations.

The movielens 100k dataset by Grouplens has been used for the recommender system. IMDb 25000 labeled reviews for sentiment classification was used for training the sentiment classifier. The movielens dataset was truncated to 1000 items.

# How it Works?

First, we extract reviews for every movie in the items data and perform sentiment analysis to get overall opinion of users for that movie. Logistic Regression is used for this purpose which gives probabilites for negative and positive class in the range [0, 1]. The positive probabilities are stored.
Then an item based collaborative filtering system is set up using the movielens dataset. It makes a dictionary of similar movies for every movie in the itemset using the similarity score. Pearson correlation has been used to find the similarity between items.
For recommendation to a user, ratings are predicted for all items similar to the items previously rated by the user. A weighted average sum of the rating, similarity score and sentiment score has been used. Then the movies with highest predicted ratings are recommended.

# How to Use?

1. First the movielens dataset is cleaned and truncated to 1000 items. The file **'TruncateData.py'** performs this task and saves the **'u.user'** file as **'users_trunc.csv'** and **'u.item'** file as **'items_trunc.csv'**. These files can be found in the data folder.

2. Then for every item in the items, we fetch reviews from IMDb. The file **'ReviewFetch.py'** performs this task. It fetches 50 reviews from the site with a gap of a few seconds between requests and saves the reviews corresponding to movie titles in the file **'final.csv'**. The file was not uploaded due to 25MB limit on the file size but can be reproduced using the script.

3. Then comes the task of sentiment classification. Logistic Regression was used for the classifier. First we clean and preprocess the IMDb labeled training data and review fetched from IMDb, create a bag of words model, apply tf-idf, train the logistic regression classifier on the 25000 labeled items and predict the probabilities of the rest 1000 items. The positive probabilities are stored in the file **'sentiment_scores.csv'** which can be found in the data folder. The whole operation can be found in the file **'LogisticRegression.py'**.

4. The file **'Recommender.py'** does the final job of recommending the items. It loads the users and items data and the sentiment scores. Then calculates similar items for every item and recommends the most similar items according to the items previously rated by the user. The file paths have been **hardcoded** in the script which can be changed.

# How to Test?
In the file **'Recommender.py'** are two recommendation functions. One which is the traditional recommender (getRecommendedItems) and the other one uses sentiment scores (getRecommendedItemsSentiment). The third integer argument in the function is the user id which can be changed to a different user. For user ids refer to the **'users_trunc.csv'** file. Line **138** has been commented which gives recommendations without sentiment. Line **141** gives recommendations using sentiment. The results from both these call can be compared.

But it takes time everytime to load data and make dictionary of similar items. To speed things up, a **'RecommenderTest.py'** file has been set up in the **Test** folder. The other three files are the pickle objects of the loaded data and dictionary of similar items. It gives the same results but much faster.
