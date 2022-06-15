import tweepy
from credentials import BEARER_TOKEN
import logging
import pymongo
import time

# Connect to mongoDB
client_mongo = pymongo.MongoClient(host="mongo", port=27017)

# Create DB
db = client_mongo.twitter

# Drop collection if exists
#drop_collection=db.my_coll.drop()

#Create collection in DB
dbcoll = db.my_coll


def get_tweets():

    '''The function is defined to get tweets for chosen account '''

# Authentication

    client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

    if client:
        logging.critical("\nAuthentication OK")
    else:
        logging.critical('\nVerify your credentials')


# Get User Information

    response = client.get_user(
    username='MikeTyson',
    user_fields=['name',
                 'id',
                 'created_at',
                 'location',
                 'profile_image_url'
                ]
                            )
    user= response.data

# Get a user's timeline 

    cursor = tweepy.Paginator (
        method=client.get_users_tweets,
        id=user.id,
        exclude=['replies', 'retweets'],
        tweet_fields=['author_id', 'text', 'created_at', 'lang', 'public_metrics'] 
                              ).flatten()

# Append some features and Create a list for tweets

    tweets=[]
    for tweet in cursor:
        tweet=dict(tweet)
        tweet['username']= user['name']
        tweet['image']=user['profile_image_url']
        tweets.append(tweet)

    return tweets

# Insert tweets into MongoDB collection

if __name__ == '__main__':

    i=1
    for tweet in get_tweets():
        dbcoll.insert_one(tweet)
        logging.critical(f" #{i}: Tweet was inserted in the colletion")
        time.sleep(2)
        i+=1

    print(f'{i} tweets were inserted successfully')



# Find the tweets from mongoDB and print them

#for my_tweet in dbcoll.find():
 # print(my_tweet, end='\n\n') 

