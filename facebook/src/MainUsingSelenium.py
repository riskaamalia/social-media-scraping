import logging
import sys
import os
import threading

from process import LoginFacebook
from process import PostsFromSearching
from util import DriverConfig
from util.ConfigProcessor import ConfigProcessor
from database.sql import sql
from process import VideoSearch
from time import sleep

dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.insert(0, dir_path)
from sea_utils import common_utils
from sea_utils import set_proxy

common_utils.setup_logging('facebook_selenium.log')
proxy = set_proxy.set()
try :
    country = sys.argv[1]
except :
    country = 'my'

class MainUsingSelenium (threading.Thread):
    def __init__(self, thread_ID, name):
        threading.Thread.__init__(self)
        self.thread_ID = thread_ID
        self.name = name

    def run(self):
        logging.info("Starting " + self.name)

        # execute process here
        execute_process(self.name, self.thread_ID)

def execute_process (name,thread_id) :
   driver = DriverConfig.defineDriver(proxy, country)
   try :
      config_processor = ConfigProcessor()

      # dao for db sqlite
      dao = sql()

      keyword = config_processor.config_facebook_keyword()
      keywords_video = config_processor.config_video_keyword()
      # set driver configuration

      if len(keyword) > 0 and thread_id == 1 :
         # log in facebook
         username = config_processor.config_facebook_username(country)
         password = config_processor.config_facebook_password(country)
         LoginFacebook.login(driver, username, password)

         logging.info("Facebook selenium search post in county : "+country)
         PostsFromSearching.processor(driver,dao,keyword)
      elif len(keywords_video) > 0 and thread_id == 2 :
          # log in facebook
          username = config_processor.config_facebook_username(country)
          password = config_processor.config_facebook_password(country)
          LoginFacebook.login(driver, username, password)

          logging.info("Facebook selenium search video in county : " + country)
          VideoSearch.processor(driver, dao, keywords_video)

   except Exception as e :
      logging.exception(str(e.message))
      logging.info('sleep for 30 minutes ...')
      if proxy is not None :
          set_proxy.delete_ip(proxy)
      driver.close()
      sleep(1800)

      execute_process(name,thread_id)


thread1 = MainUsingSelenium(1, "1-Thread-Facebook-Page")
thread1.start()

if country == 'id' :
    thread2 = MainUsingSelenium(2, "2-Thread-Facebook-Video")
    thread2.start()