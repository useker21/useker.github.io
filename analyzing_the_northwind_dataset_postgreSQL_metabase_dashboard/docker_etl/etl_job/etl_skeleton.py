import time
import pymongo
from sqlalchemy import text, create_engine
import logging
import psycopg2
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Connect to mongoDB
client = pymongo.MongoClient(host="mongodb", port=27017)
db=client.twitter # Select the database you want to use withing the MongoDB server
dbcoll=db.my_coll

# Extract the tweets from mongodb

def extract():

    ''' Extracts tweets from mongodb'''
  
# Extract the tweets 
    extracted_tweets=list(dbcoll.find())

# Remove the duplicates
    ''' extracted_tweets=[]

    for tweet in extracted_tweets_all:
        if tweet in extracted_tweets:
            return True
        else:
            extracted_tweets.append(tweet)'''

    return extracted_tweets

# Transform the data
def transform(extracted_tweets):

    ''' Transforms data: clean text, gets sentiment analysis from text '''
 
    transformed_tweets = []

    for tweet in extracted_tweets:
        # clean text
        mentions_regex= '@[A-Za-z0-9]+'  # "+" means one or more times
        url_regex='https?:\/\/\S+' # this will catch most URLs; "?" means 0 or 1 time; "S" is anything but whitespace
        hashtag_regex= '#'
        rt_regex= 'RT\s'

        tweet['text'] = re.sub(mentions_regex, '', tweet['text'])  # removes @mentions
        tweet['text'] = re.sub(hashtag_regex, '', tweet['text']) # removes hashtag symbol
        tweet['text'] = re.sub(rt_regex, '', tweet['text']) # removes RT to announce retweet
        tweet['text'] = re.sub(url_regex, '', tweet['text']) # removes most URLs
        tweet['text'] = tweet['text'].replace('\n',' ').replace("'", '').replace("  ", ' ').replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(',', '').replace('.', '').replace('[*]', '')
        
        # calculate a sentiment
        analyser = SentimentIntensityAnalyzer()

        sentiment =  analyser.polarity_scores (tweet['text'])

        # datatype of the tweet: dictionary
        tweet['sentiment'] = sentiment['compound'] # adding a key: value pair with 'sentiment' as the key and the score as the value

        transformed_tweets.append(tweet)
        # transformed_tweets is a list of transformed dictionaries

    return transformed_tweets

# Load the data into postgresdb

def load(transformed_tweets):

   
    ''' Load final data into postgres'''
    # Create connection to postgres databases

    HOST = 'postgres'
    PORT = '5432' #port inside the container
    DATABASE = 'postgres'
    USER = 'postgres'
    PASSWORD = 'postgres'

    conn_string = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    engine = create_engine(conn_string, echo=True)
    
    engine.execute('''DROP TABLE IF EXISTS tweets;''')

    create_query = '''  CREATE TABLE tweets(                    
                        tweet_date TIMESTAMP,
                        tweet_text TEXT,
                        tweet_rt_count INT,
                        tweet_rply_count INT,
                        tweet_like_count INT,
                        lang TEXT,
                        sentiment FLOAT
                        );
    '''
   
    engine.execute(create_query)

    
    for tweet in transformed_tweets:
      
        insert_query = '''INSERT INTO tweets VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        engine.execute(insert_query,( tweet['created_at'],
                                      tweet['text'], 
                                      tweet['public_metrics']['retweet_count'],
                                      tweet['public_metrics']['reply_count'],
                                      tweet['public_metrics']['like_count'],
                                      tweet['lang'], 
                                      tweet['sentiment']                                     
                                     )
                       )
        logging.critical('---Inserted a new tweet into postgresdb---')
        


if __name__== "__main__":
    
    #run ETL job every 2 minutes

    while True:
        extracted_tweets=extract()
        transformed_tweets = transform(extracted_tweets)
        load(transformed_tweets)

        time.sleep(120)

    