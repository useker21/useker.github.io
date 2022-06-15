import tweepy
from credentials import BEARER_TOKEN
import logging


# authentication

client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

if client:
    logging.critical("\nAuthentication OK")
else:
    logging.critical('\nVerify your credentials')


# Get User Information

response = client.get_user(
    username='jakevkp',
    user_fields=['created_at', 
                'description', 
                'location',
                'public_metrics'
                ]
)
user= response.data

dict(user)

# Get a user's timeline 

cursor = tweepy.Paginator(
    method=client.get_users_tweets,
    id=user.id,
    exclude=['replies', 'retweets'],
    tweet_fields=['author_id', 'created_at', 'public_metrics']
).flatten(limit=5)


for tweet in cursor:
    print(tweet.text)



