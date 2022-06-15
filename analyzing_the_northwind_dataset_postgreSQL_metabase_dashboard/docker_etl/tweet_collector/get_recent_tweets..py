import tweepy
from credentials import BEARER_TOKEN
import logging
import pymongo
import time

# Connect to mongoDB 
client_mongo = pymongo.MongoClient(host="mongodb", port=27017)
db = client_mongo.twitter
dbcoll = db.my_tweets

def get_recent_tweets(username):

    '''The function is defined to get recent tweets for chosen account '''

# Authentication

    client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

    if client:
        logging.critical("\nAuthentication OK")
    else:
        logging.critical('\nVerify your credentials')


# Get User Information

    response = client.get_user(
    username=f'{username}',
    user_fields=['name',
                 'id',
                 'created_at',
                 'location',
                 'profile_image_url'
                ]
                            )
    user= dict(response.data)

# Search recent tweets 

    search_query = f'{username} -is:retweet -is:reply -is:quote lang:en -has:links'

    cursor = tweepy.Paginator(
        method=client.search_recent_tweets,
        query=search_query,
        tweet_fields=['author_id', 'text', 'created_at', 'lang', 'public_metrics'],
                             ).flatten(limit=1)

# Append some features and Create a list for recent tweets

    recent_tweets=[]
    for tweet in cursor:
        tweet=dict(tweet)
        tweet['username']= user['name']
        tweet['image']=user['profile_image_url']
        recent_tweets.append(tweet)

    return recent_tweets


# Insert the tweets to the collection

if __name__ == '__main__':

    i=1
   
    for tweet in get_recent_tweets('MikeTyson'):

      if dict(tweet) is not list(dbcoll.find()):
        
        dbcoll.insert_one(dict(tweet))
        logging.critical(f" #{i}: Tweet was inserted in the colletion")
        time.sleep(5)
        i+=1

      else: logging.critical('The tweet was inserted before')
    





