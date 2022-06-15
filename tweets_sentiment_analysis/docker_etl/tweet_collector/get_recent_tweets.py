import tweepy
from credentials import BEARER_TOKEN
import logging
import pymongo
import time

# Authentication

client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

if client:
    logging.critical("\nAuthentication OK")
else:
    logging.critical('\nVerify your credentials')

# Search recent tweets 

search_query = 'Mike Tyson -is:retweet -is:reply -is:quote lang:en'

cursor = tweepy.Paginator(
    method=client.search_recent_tweets,
    query=search_query,
    tweet_fields=['author_id', 'text', 'created_at','lang', 'public_metrics'],
                             ).flatten(limit=50)


# Connect to mongoDB 
client_mongo = pymongo.MongoClient(host="mongodb", port=27017)
db = client_mongo.twitter


# Insert tweets into mongodb

i=1
for tweet in cursor:
    db.my_coll.insert_one(dict(tweet))
    logging.critical(f" #{i}: Tweet was inserted in the colletion")
    time.sleep(2)
    i+=1