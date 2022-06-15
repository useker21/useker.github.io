import tweepy
from credentials import BEARER_TOKEN
import logging
import time
from sqlalchemy import create_engine


HOST = 'postgres_tweet'
PORT = '5432' #port inside the container
DATABASE = 'postgres'
USER = 'postgres'
PASSWORD = 'postgres'

conn_string = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(conn_string)

create_query = '''
CREATE TABLE get_tweets(
    id SERIAL PRIMARY KEY,
    user_name TEXT, 
    tweet_date TEXT,
    tweet_text TEXT);
'''
engine.execute('''DROP TABLE IF EXISTS get_tweets;''')
engine.execute(create_query)


client = tweepy.Client(bearer_token=BEARER_TOKEN)

if client:
    logging.critical("\nAuthentication OK")
else:
    logging.critical('\nVerify your credentials')

katejarmul=client.get_user(username='kjam', user_fields=['name', 'id', 'created_at', 'description', 'location'])

user= katejarmul.data

katejarmul_tweets=client.get_users_tweets(id=user.id, tweet_fields=['id', 'text', 'created_at'], max_results=100)


if __name__ == '__main__':

    for tweet in katejarmul_tweets.data:

        tweet_text=tweet.text
        tweet_text_clear=tweet_text.replace("'", '').replace('"', '').replace('%', '')
        insert_query = f"INSERT INTO get_tweets (user_name,tweet_date, tweet_text) VALUES ('{user.name}', '{tweet.created_at}', '{tweet_text_clear}')"
        engine.execute(insert_query)
        logging.critical(f"Tweet written in database {DATABASE} in host {HOST}")
        time.sleep(2)