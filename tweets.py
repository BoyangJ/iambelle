#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy, time, sys
import configparser
import code
import os

from image_rec import authorTweet

# get Twitter app auth info
Config = configparser.ConfigParser()
Config.read("config.ini")

# used by Heroku
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_KEY = os.environ['ACCESS_KEY']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

# used for local testing
#CONSUMER_KEY = Config['AuthInfo']['CONSUMER_KEY']
#CONSUMER_SECRET = Config['AuthInfo']['CONSUMER_SECRET']
#ACCESS_KEY = Config['AuthInfo']['ACCESS_KEY']
#ACCESS_SECRET = Config['AuthInfo']['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def compliment_photo(tweets_list):
    for status in tweets_list:
        # only consider tweets with photos
        if 'media' in status.entities:
            if status.entities['media'][0]['type'] == 'photo':
                # photo tweet found, send to image analyzer
                tweet_body = authorTweet(status.entities['media'][0]['media_url_https'])

                # if image analyzer returns '', the image is not suitable
                if tweet_body is '':
                    continue

                # prepend the @handle of the recipient
                full_tweet = "@%s " % status.user.screen_name
                full_tweet = full_tweet + tweet_body

                # favorite and reply to the selected tweet
                if reply_to_tweet(status.id, full_tweet):
                    return


# retrieves tweets made in Victoria, BC and selects one to compliment
def get_local_tweets():
    # get the location code for Victoria BC using lat/long
    victoria = api.reverse_geocode(48.4284, -123.3656)
    victoria_id = victoria[0].id

    # retrieve the 100 most recent tweets made in Victoria
    query = "place:%s" % victoria_id
    vic_tweets = [status for status in tweepy.Cursor(api.search, tweet_mode='extended', q=query).items(100)]

    compliment_photo(vic_tweets)
                

# retrieves a user's 20 most recent tweets
# parameter u_id can either be a twitter @handle, or an id
def get_user_tweets(u_id):

    # retrieves a user's 20 most recent tweets
    user_tweets = api.user_timeline(u_id, tweet_mode='extended', include_rts=False);

    compliment_photo(user_tweets)
    

# tweets a reply to tweet with id=t_id
# parameter t_id must be a Twitter status id.
def reply_to_tweet(t_id, tweet):
    try:
        api.create_favorite(t_id)
        api.update_status(tweet, t_id)
        return True
    except tweepy.TweepError as e:
        print ("\n", e)
        return False


