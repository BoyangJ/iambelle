import tweepy, time, sys
import configparser
import code
import os

from tweets import get_local_tweets

# get Twitter app auth info
Config = configparser.ConfigParser()
Config.read("config.ini")

# used by Heroku
#CONSUMER_KEY = os.environ['CONSUMER_KEY']
#CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
#ACCESS_KEY = os.environ['ACCESS_KEY']
#ACCESS_SECRET = os.environ['ACCESS_SECRET']

# used for local testing
CONSUMER_KEY = Config['AuthInfo']['CONSUMER_KEY']
CONSUMER_SECRET = Config['AuthInfo']['CONSUMER_SECRET']
ACCESS_KEY = Config['AuthInfo']['ACCESS_KEY']
ACCESS_SECRET = Config['AuthInfo']['ACCESS_SECRET']


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


while (1):
    get_local_tweets()
    print ("Tweeting a nice compliment :D\n")
    time.sleep(900) # Tweet every 15 minutes
