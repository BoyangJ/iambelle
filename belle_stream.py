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



class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    # a listener for tweets received from the stream
    # on receiving a tweet, close and open the serial port to flash
    def on_data(self, data):
        ser.close()
        ser.open()
        return True

    def on_error(self, status):
        print(status)



if __name__ == '__main__':
    # serial port configuration for the arduino
    ser = serial.Serial('/dev/cu.usbmodem1411', 1200)
    
    l = StdOutListener()

    # follow the Belle Bot (@iambellebot) account for new tweets
    stream = Stream(auth, l)
    stream.filter(follow=['840653820447211520'])



