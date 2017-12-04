import logging
import os
from logging.handlers import TimedRotatingFileHandler

parent1 = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
path = os.path.abspath(os.path.join(parent1, os.pardir))

def get_keywords():
    location = path + "/config/keyword.log"
    f = open(location, 'r')
    value = f.read().splitlines()

    return value

def get_api_key (country) :
    if country == 'my' :
        location = path + "/src/sea_twitter/config/twitter_key_malaysia.log"
    elif country == 'th' :
        location = path + "/src/sea_twitter/config/twitter_key_thailand.log"
    elif country == 'vn' :
        location = path + "/src/sea_twitter/config/twitter_key_vietnam.log"
    else :
        location = path + "/src/sea_twitter/config/twitter_key.log"

    f = open(location, 'r')
    value = f.read().splitlines()

    return value