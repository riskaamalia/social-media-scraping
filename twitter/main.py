import threading
from time import sleep

import random
import configuration
import logging
import twitterApi

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.insert(0, dir_path)
from sea_utils import common_utils
from sea_utils import set_proxy

common_utils.setup_logging('twitter.log')
# set_proxy.set()

try :
    country = sys.argv[1]
except Exception as e :
    country = 'my'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

class twitter (threading.Thread):

   def __init__(self, thread_ID, name):
      threading.Thread.__init__(self)
      self.thread_ID = thread_ID
      self.name = name

   def run(self):
      logging.info ("Starting " + self.name)
      #print "Starting " + self.name

      # execute process here
      execute_twitter_api(self.thread_ID)

def execute_twitter_api (thread_id) :
    while True :
        if thread_id != 3 :

            keywords = configuration.get_keywords()
            logging.info('Total keyword : '+str(len(keywords)))
            count_keyword = 1
            for keyword in keywords:
                logging.info(str(count_keyword)+".) Find with keyword : " + keyword)
                #print "Find with keyword : " + keyword
                keyword = keyword.replace(' ','%20')
                twitterApi.search_7_days(keyword, thread_id, country)

                time_loop = 10 + random.randint(5, 60)
                logging.info('Sleep for a while in ... s : ' + str(time_loop))
                sleep(time_loop)
                count_keyword = count_keyword + 1
        else :
            twitterApi.trending_topic(country)

        logging.info('start again, sleep for a while ...')
        sleep(300)


thread1 = twitter(1,'next_result')
thread1.start()
sleep(5)
thread2 = twitter(2,'refresh_url')
thread2.start()
sleep(5)
thread3 = twitter(3,'trending_topic')
thread3.start()
