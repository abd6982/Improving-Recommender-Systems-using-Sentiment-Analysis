#Imports
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint

#Column names
columns = ['movie id','movie title','release date',
'video release date','IMDb URL','unknown','Action',
'Adventure','Animation','Childrens','Comedy','Crime',
'Documentary','Drama','Fantasy','Film-Noir','Horror',
'Musical','Mystery','Romance ','Sci-Fi','Thriller',
'War' ,'Western']

#Load the item data
items = pd.read_csv('D:/Workspace/Jupyter/Python/data/movielens/u.item', sep = '|', encoding = 'latin-1', names = columns)

#This function take title of movie in the form of a string and returns a list of all the reviews
def getReviews(title):
    
    #Get the url of the movie
    url = 'http://www.imdb.com/search/title?title='
    html_page = requests.get(url + '%20'.join(title.split()))
    html_soup = BeautifulSoup(html_page.text, 'html.parser')
    title_url = 'http://www.imdb.com' + html_soup.find_all('div', class_ = 'lister-item mode-advanced')[0].h3.a['href']
    
    #Get the review url
    review_url = title_url.split('?')[0] + 'reviews?start=0'
    
    #Get all the reviews
    reviews = list()
    review_count = 10
    page_marker = 10
    while(review_count >= 10):
        review_page = requests.get(review_url)
        r_soup = BeautifulSoup(review_page.text, 'html.parser')
        temp = r_soup.find_all('div', id = 'tn15content')[0].find_all('p')
        review_count = len(temp)
        for i in range(review_count):
            if temp[i].text != '*** This review may contain spoilers ***' and temp[i].text != 'Add another review':
                reviews.append(temp[i].text)
        review_url = '='.join([review_url.split('=')[0], str(int(review_url.split('=')[1]) + 10)])
        sleep(randint(1,3))
    return reviews

#This function uses loops over all movie titles in the dataset and uses getReviews() to fetch reviews and build a list
def getReviewData(title_df):
    review_data = list()
    for title in title_df['movie title']:
        print(title.split('(')[0])
        review_data.append([title.split('(')[0], getReviews(title.split('(')[0])])
    return review_data

#Utility function for fetching URLs for movies by URL which were not found during search
def getReviewsURL(title_url):
    #Get the review url
    review_url = title_url.split('?')[0] + 'reviews?start=0'

    #Get all the reviews
    reviews = list()
    review_count = 10
    page_marker = 10
    total_reviews = 0
    while(review_count >= 10):
        review_page = requests.get(review_url)
        r_soup = BeautifulSoup(review_page.text, 'html.parser')
        temp = r_soup.find_all('div', id = 'tn15content')[0].find_all('p')
        review_count = len(temp)
        for i in range(review_count):
            if temp[i].text != '*** This review may contain spoilers ***' and temp[i].text != 'Add another review':
                reviews.append(temp[i].text)
                total_reviews += 1
            if total_reviews == 50: return reviews
        review_url = '='.join([review_url.split('=')[0], str(int(review_url.split('=')[1]) + 10)])
        sleep(randint(1,3))
    return reviews

#Get all the reviews and write the data into a csv file
data = getReviewData(items)
pd.to_csv('review_data.csv')

