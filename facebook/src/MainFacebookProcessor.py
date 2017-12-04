import threading
import logging
from process import GraphApiPages
from process import GraphApiSearchPages
from process import GraphApiVideoPage
from time import sleep
from util.ConfigProcessor import ConfigProcessor
from database.sql import sql

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.insert(0, dir_path)
from sea_utils import common_utils
from sea_utils import set_proxy

common_utils.setup_logging('facebook.log')
# proxy = set_proxy.set()
try :
    country = sys.argv[1]
except :
    country = 'id'

class MainFacebookProcessor (threading.Thread):

   def __init__(self, thread_ID, name):
      threading.Thread.__init__(self)
      self.thread_ID = thread_ID
      self.name = name

   def run(self):
      logging.info ("Starting " + self.name)

      # execute process here
      execute_process(self.name,self.thread_ID)

def execute_process (thread_name,thread_id) :
   logging.info("Processor :"+thread_name)
   config_processor = ConfigProcessor()
   # token and limit
   token = config_processor.facebook_token("token",country)
   limit = config_processor.facebook_token("limit",country)
   # dao for db
   dao = sql()

   keyword = config_processor.config_facebook_keyword()
   keyword_video = config_processor.config_video_keyword()

   while True :
       if thread_id == 2 :
            GraphApiPages.processor(dao,token,limit)
       elif thread_id == 3 :
            GraphApiSearchPages.processor(dao,keyword,token,limit)
       elif thread_id == 4 :
            GraphApiVideoPage.processor(dao,keyword_video,token,limit)

       logging.info('starting again ....')


thread2 = MainFacebookProcessor(2, "2-Thread-Graph-Posts")
thread2.start()

thread3 = MainFacebookProcessor(3, "3-Thread-Graph-Pages")
thread3.start()

if country == 'id' :
    thread4 = MainFacebookProcessor(4, "4-Thread-Graph-Video-Pages")
    thread4.start()
