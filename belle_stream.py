#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
import tweepy, time, sys
import configparser
import code
import os
import serial

# get Twitter app auth info
Config = configparser.ConfigParser()
Config.read("config.ini")

#CONSUMER_KEY = os.environ['CONSUMER_KEY']
#CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
#ACCESS_KEY = os.environ['ACCESS_KEY']
#ACCESS_SECRET = os.environ['ACCESS_SECRET']

CONSUMER_KEY = Config['AuthInfo']['CONSUMER_KEY']
CONSUMER_SECRET = Config['AuthInfo']['CONSUMER_SECRET']
ACCESS_KEY = Config['AuthInfo']['ACCESS_KEY']
ACCESS_SECRET = Config['AuthInfo']['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)



class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        ser.close()
        ser.open()
        return True

    def on_error(self, status):
        print(status)



if __name__ == '__main__':
    ser = serial.Serial('/dev/cu.usbmodem1411', 1200)
    
    l = StdOutListener()
    #auth = OAuthHandler(consumer_key, consumer_secret)
    #auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(follow=['840653820447211520'])



