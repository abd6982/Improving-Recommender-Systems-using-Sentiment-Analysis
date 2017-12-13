import pickle
import pandas as pd

items = pickle.load( open( "items.p", "rb" ) )
prefs = pickle.load( open( "prefs.p", "rb" ) )
itemsim = pickle.load( open( "itemsim.p", "rb" ) )

#Function to get item based recommendations


def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (item, rating) in userRatings.items():
        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings:
                continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item)
                for item, score in scores.items()]
    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings

#Function to get improved item based recommendations by using sentiment scores


def getRecommendedItemsSentiment(prefs, itemMatch, user):
    sentiment_scores = pd.read_csv(
        'D:\\Data\\sentiment_scores.csv', encoding='latin-1')
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (item, rating) in userRatings.items():
        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings:
                continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating * \
                sentiment_scores[sentiment_scores['movie title']
                                 == item2]['sentiment'].iloc[0]
            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item)
                for item, score in scores.items()]
    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings


print(getRecommendedItemsSentiment(prefs, itemsim, 4)[0: 10])
