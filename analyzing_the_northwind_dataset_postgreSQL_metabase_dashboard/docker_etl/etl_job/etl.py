import pymongo
import time

# Wait for mongodb
time.sleep(10)

# Establish a connection to the MongoDB server
client = pymongo.MongoClient(host="mongodb", port=27017)

# Select the database to use within the MongoDB container
db = client.twitter

# Get tweets from mongodb
docs = db.my_coll.find()


# Clean data 


import pandas as pd
pd.set_option("max_colwidth", 100)
import re

tweets = [doc['text'] for doc in docs]
df = pd.DataFrame(tweets, columns=['tweet_text'])

# Actual cleaning of the data

new_line='\n\n|\n'
mentions_regex= '@[A-Za-z0-9]+'  
url_regex='https?:\/\/\S+' 
hashtag_regex= '#'
rt_regex= 'RT\s'

def clean_tweets(tweet):
    tweet = re.sub(new_line, '', tweet)  # removes line breaks
    tweet = re.sub(mentions_regex, '', tweet)  # removes @mentions
    tweet = re.sub(hashtag_regex, '', tweet) # removes hashtag symbol
    tweet = re.sub(rt_regex, '', tweet) # removes RT to announce retweet
    tweet = re.sub(url_regex, '', tweet) # removes most URLs
    return tweet

df.tweet_text = df.tweet_text.apply(clean_tweets)

# Perform sentiment analysis

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()
pol_scores = df['tweet_text'].apply(analyser.polarity_scores).apply(pd.Series)


df['compound'] = pol_scores['compound']

df.reset_index(inplace = True)

#################################
### Load data into postgreSQL ###
#################################

from sqlalchemy import create_engine

  # Create connection to postgres databases

HOST = 'postgres'
PORT = '5432' #port inside the container
DATABASE = 'postgres'
USER = 'postgres'
PASSWORD = 'postgres'

conn_string = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(conn_string, echo=True)

# Create table in postgres
engine.execute('''DROP TABLE IF EXISTS tweets_2;''')
engine.execute('''CREATE TABLE tweets_2 (text TEXT, sentiment NUMERIC);''')

# Load data into table
df.to_sql('tweets_2', engine, if_exists='replace', index=False)
engine.execute('ALTER TABLE tweets_2 ADD PRIMARY KEY ("index")')