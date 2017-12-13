# Imports
#import pickle
import numpy as np
import pandas as pd

# Function to load data and create item based dictionary
def loadData():
    users_df = pd.read_csv('D:\\Data\\users_trunc.csv', encoding='latin-1')
    items_df = pd.read_csv('D:\\Data\\items_trunc.csv', encoding='latin-1')

    movies = {}
    for i in range(len(items_df)):
        movies[items_df.iloc[i]['item_id']] = items_df.iloc[i]['movie title']
        
    prefs = {}
    for i in range(len(users_df)):
        prefs.setdefault(users_df.iloc[i]['user id'], {})
        prefs[users_df.iloc[i]['user id']][movies[users_df.iloc[i]['item_id']]] = float(users_df.iloc[i]['rating'])

    items = {}
    for i in range(len(users_df)):
        items.setdefault(users_df.iloc[i]['item_id'], {})
        items[users_df.iloc[i]['item_id']][users_df.iloc[i]['user id']] = float(users_df.iloc[i]['rating'])
    for i in range(len(items_df)):
        items[items_df.iloc[i]['movie title']] = items.pop(items_df.iloc[i]['item_id'])
    return items, prefs

# Function to calculate pearson correlation coefficient
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1
    # Find the number of elements
    n = len(si)
    # if they are no ratings in common, return 0
    if n == 0: return 0
    # Add up all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    # Sum up the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it], 2) for it in si])
    # Sum up the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    # Calculate Pearson score
    num = pSum - (sum1 * sum2 / n)
    den = np.sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0
    r = num/den
    return r

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs, person, n = 5, similarity = sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    # Sort the list so the highest scores appear at the top
    scores.sort( )
    scores.reverse( )
    return scores[0: n]

# Function to create a dictionary of items showing which other items they are most similar to
def calculateSimilarItems(prefs, n = 10):
    result={}
    c = 0
    for item in prefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0: print("{} / {}".format(c, len(prefs)))
        # Find the most similar items to this one
        scores = topMatches(prefs, item, n, similarity=sim_pearson)
        result[item] = scores
    return result

#Function to get item based recommendations
def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (item, rating) in userRatings.items( ):
        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings: continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item) for item, score in scores.items( )]
    # Return the rankings from highest to lowest
    rankings.sort( )
    rankings.reverse( )
    return rankings

#Function to get improved item based recommendations by using sentiment scores
def getRecommendedItemsSentiment(prefs, itemMatch, user):
    sentiment_scores = pd.read_csv('D:\\Data\\sentiment_scores.csv', encoding='latin-1')
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (item, rating) in userRatings.items( ):
        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings: continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating * sentiment_scores[sentiment_scores['movie title'] == item2]['sentiment'].iloc[0]
            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item) for item, score in scores.items( )]
    # Return the rankings from highest to lowest
    rankings.sort( )
    rankings.reverse( )
    return rankings


#Load the dataset
items, prefs = loadData()

#Calculate similar items
itemsim = calculateSimilarItems(items, n = 50)

"""
pickle.dump(items, open( "items.p", "wb" ) )
pickle.dump(prefs, open( "prefs.p", "wb" ) )
pickle.dump(itemsim, open( "itemsim.p", "wb" ) )
"""

#Get recommendations
#print(getRecommendedItems(prefs, itemsim, 6)[0: 10])

#Get improved recommendations
print(getRecommendedItemsSentiment(prefs, itemsim, 4)[0: 10])
