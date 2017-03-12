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

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_KEY = os.environ['ACCESS_KEY']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

#CONSUMER_KEY = Config['AuthInfo']['CONSUMER_KEY']
#CONSUMER_SECRET = Config['AuthInfo']['CONSUMER_SECRET']
#ACCESS_KEY = Config['AuthInfo']['ACCESS_KEY']
#ACCESS_SECRET = Config['AuthInfo']['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

user = api.get_user('iambellebot')


def get_local_tweets():

    victoria = api.reverse_geocode(48.4284, -123.3656)
    victoria_id = victoria[0].id

    query = "place:%s" % victoria_id
    vic_tweets = [status for status in tweepy.Cursor(api.search, tweet_mode='extended', q=query).items(100)]

    counter = 0

    for status in reversed(vic_tweets):
        if 'media' in status.entities:
            if status.entities['media'][0]['type'] == 'photo':
                print ("\nTEXT = ", status.full_text)
                print ("ID = ", status.id)
                print ("CREATED AT = ", status.created_at)
                print ("SCREEN NAME = ", status.user.screen_name)
                print ("url = twitter.com/statuses/", status.id, sep='')
                print ("media_url = ", status.entities['media'][0]['media_url_https'])
                counter = counter+1

    print ("\n***** NUM PICTURES = %d *****\n" % counter)


# retrieves a user's 20 most recent tweets
# parameter u_id can either be a twitter @handle, or an id
def get_user_tweets(u_id):

    user_tweets = api.user_timeline(u_id, tweet_mode='extended', include_rts=False);

    print ("\n***** USER %s HAS %d TWEETS *****\n" % (u_id, len(user_tweets)))
    
    counter = 0

    for status in user_tweets:
        if 'media' in status.entities:
            if status.entities['media'][0]['type'] == 'photo':
                # photo tweet found, send to image analyzer
                tweet_body = authorTweet(status.entities['media'][0]['media_url_https'])
                
                if tweet_body is '':
                    continue
                
                full_tweet = "@%s " % status.user.screen_name
                full_tweet = full_tweet + tweet_body

                reply_to_tweet(status.id, full_tweet)

                print ("FULL TWEET = ", full_tweet)
                print ("\nTEXT = ", status.full_text)
                print ("ID = ", status.id)
                print ("CREATED AT = ", status.created_at)
                print ("SCREEN NAME = ", status.user.screen_name)
                print ("url = twitter.com/statuses/", status.id, sep='')
                print ("media_url = ", status.entities['media'][0]['media_url_https'])
                counter = counter+1

    print ("\n***** NUM PICTURES = %d *****\n" % counter)


# tweets a reply to tweet with id=t_id
# parameter t_id must be a Twitter status id.
def reply_to_tweet(t_id, tweet):
    
    #screen_name = api.get_status(t_id, tweet_mode='extended').user.screen_name
    #print ("\nSCREEN NAME HERE = ", screen_name)
    
    #reply_text = generate_reply(screen_name)
    #print ("\nREPLY TEXT HERE = ", reply_text)

    try:
        api.create_favorite(t_id)
        api.update_status(tweet, t_id)
        return True
    except tweepy.TweepError:
        print ("\n Already favorited this tweet. \n")
        return False


# generates a tweet's text body
# parameter u_name must be the Twitter @handle of the recipient
def generate_reply(u_name):
    return "@%s you are pretty ☺️" % u_name





#get_user_tweets("baronbojangles")
#reply_to_tweet(840743579299414016)


#filename=open(argfile,'r')
#f=filename.readlines()
#filename.close()



#print ("\nENTITIES = ", vic_tweets[0].entities)
#print ("\nTEXT = ", vic_tweets[0].full_text)
#print ("ID = ", vic_tweets[0].id)


#print (user['screen_name'])
#print (api.get_status(123, tweet_mode='extended')['text'])


#USE tweet_mode='extended' OR ELSE YOU LOSE

#if 'media' in tweet.entities:
#    tweet['entities']['media']



#print (user.screen_name)
#print (user.followers_count)
#for friend in user.friends():
#  print (friend.screen_name)
   

#for line in f:
#    api.update_status(line)
#    time.sleep(900)#Tweet every 15 minutes




#code.interact(local=locals())
