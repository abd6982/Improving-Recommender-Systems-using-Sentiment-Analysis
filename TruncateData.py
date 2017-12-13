#Script to create truncated versions of the original Movielens dataset

#Imports
import numpy as np
import pandas as pd

#Column names of items data
columns = ['item_id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action',
          'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
          'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

#Read items data
items = pd.read_csv('ml-100k/u.item', sep= '|', names = columns, encoding = 'latin-1')

#Column names for users data
columns_users = ['user id', 'item_id', 'rating', 'timestamp']

#Read users data
users = pd.read_csv('ml-100k/u.data', sep = '\t', names = columns_users)

#Remove the entry for which reviews were not found
items[['item_id', 'movie title']].drop([906], inplace = True)

#Truncate the items data to 1000 items and save into csv file
items = items[:1000]
items[['item_id', 'movie title']].to_csv('items_trunc.csv', header=None, index=False)

#Get item ids
item_ids = items['item_id'].unique()

#Get a list of all the entries from users data whose item ids are not present in the truncated item data
remove_list = list()
for i in range(len(users)):
    if users.iloc[i]['item_id'] not in item_ids: remove_list.append(i)
len(remove_list)

#Remove the entries and save the truncated data
users.drop(remove_list, inplace = True)
users.to_csv('users_trunc.csv', index=False)

#Assign movie titles to the sentiment score data
sentiment_scores.to_csv('sentiment_data_unigram.csv', index=False)
sentiment_scores['movie title'] = ""
for i in range(len(sentiment_scores)):
    sentiment_scores.at[i, 'movie title'] = items.iloc[i]['movie title']

#Save the updated file
sentiment_scores.to_csv('sentiment_scores.csv', index=False)