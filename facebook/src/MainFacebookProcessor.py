import threading

from process import LoginFacebook
from process.PagesFromSearching import PagesFromSearching
from process.PagesFromRelatedPage import PagesFromRelatedPage
from process.PostsFromPages import PostsFromPages
from process.PostsFromSearching import PostsFromSearching
from util import DriverConfig
from util import LoggerConfig
from util.ConfigProcessor import ConfigProcessor
from database.SqliteDao import SqliteDao

logger = LoggerConfig.setConfig()

class MainFacebookProcessor (threading.Thread):

   def __init__(self, thread_ID, name):
      threading.Thread.__init__(self)
      self.thread_ID = thread_ID
      self.name = name

   def run(self):
      logger.info ("Starting " + self.name)

      # execute process here
      execute_process(self.name,self.thread_ID)

      logger.info ("Exiting " + self.name)

def execute_process (thread_name,thread_id) :

   logger.info("Processor :"+thread_name)
   # set driver configuration
   driver = DriverConfig.defineDriver()
   config_processor = ConfigProcessor()

   # dao for db sqlite
   dao = SqliteDao()

   # keyword , for example just get first keyword
   keyword = config_processor.config_facebook_keyword()[0]

   # log in facebook
   username = config_processor.config_facebook_username()
   password = config_processor.config_facebook_password()
   LoginFacebook.login(driver, username, password)

   if thread_id == 1 :
      # role --> get pages from recommendation and get some posts in pages that exists in db
      logger.info("Processor Pages uses : "+thread_name)
      PostsFromPages.processor(driver,thread_name,dao)

   elif thread_id == 2 :
      # role --> get pages in db and find related pages
      logger.info("Processor Related Pages uses : "+thread_name)
      PagesFromRelatedPage.processor(driver,thread_name,dao)
   elif thread_id == 3 :
      # role --> search using some query , and then go to get all related pages to query
      logger.info("Processor Search Pages uses : "+thread_name)
      PagesFromSearching.processor(driver,thread_name,dao,keyword)
   elif thread_id == 4 :
      # role --> search using some query , and then go to get all posts to query
      logger.info("Processor Search Posts uses : "+thread_name)
      PostsFromSearching.processor(driver,thread_name,dao,keyword)


# Create new threads , 1 threads for one process
thread1 = MainFacebookProcessor(1, "1-Thread-Pages")
thread2 = MainFacebookProcessor(2, "2-Thread-Related-Pages")
thread3 = MainFacebookProcessor(3, "3-Thread-Search-Pages")
thread4 = MainFacebookProcessor(4, "4-Thread-Search-Posts")

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()
