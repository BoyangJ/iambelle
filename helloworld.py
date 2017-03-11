#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy, time, sys
import configparser
 
argfile = str(sys.argv[1])

# get Twitter app auth info
Config = configparser.ConfigParser()
Config.read("config.ini")

CONSUMER_KEY = Config['AuthInfo']['CONSUMER_KEY']
CONSUMER_SECRET = Config['AuthInfo']['CONSUMER_SECRET']
ACCESS_KEY = Config['AuthInfo']['ACCESS_KEY']
ACCESS_SECRET = Config['AuthInfo']['ACCESS_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
 
filename=open(argfile,'r')
f=filename.readlines()
filename.close()




for line in f:
    api.update_status(line)
    time.sleep(900)#Tweet every 15 minutes
