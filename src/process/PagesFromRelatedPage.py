
import re

import time
from datetime import datetime

from util import LoggerConfig
from util.ConfigProcessor import ConfigProcessor

logger = LoggerConfig.setConfig()
path_page = ConfigProcessor.config_file_storage('path_page')

class PagesFromRelatedPage :

    def processor (driver,thread_name,dao) :
        logger.info("Processing finds related page from page")
        execute_process_to_db(driver,thread_name,dao)
        driver.quit()

def execute_process_to_db (driver,thread_name,dao) :

    # go to a page , data from db
    pages = dao.get_page()

    loop = 0
    for page in pages :
        logger.info(thread_name+" From Db : "+page[0])
        try :
            driver.get(page[0])
            time.sleep(3)

            # find all related link to the page
            elems = driver.find_elements_by_xpath("//div[@class='_5ay5']//a[@href]")
            for elem in elems:
                regex = r'(https://www.facebook.com/)([^/]*)(/)$'
                regex2 = r'(https://www.facebook.com/)([^/]*)([/?ref=py_c]*)$'
                url = elem.get_attribute("href").replace('?ref=py_c','')
                if re.match(regex,url) or re.match(regex2,url) :
                    # check the url exist or not

                    is_exist = dao.is_url_page_exist(url)
                    if is_exist == 0 :
                        #     write to db
                        row = (url)
                        dao.add_page(row)
                        loop = loop + 1
                        logger.info(thread_name+" Write : "+url+" total write : "+str(loop))

        except (Exception) :
            logger.info('Invalid URL ')

        time.sleep(2)


def execute_process (driver,thread_name) :
    # go to a page , data from file
    open(path_page).readline()

    for line in open(path_page) :
        logger.info(thread_name+" From file : "+line)
        try :
            driver.get(line)
            time.sleep(3)

            # find all related link to the page
            elems = driver.find_elements_by_xpath("//div[@class='_5ay5']//a[@href]")
            loop = 0
            for elem in elems:
                regex = r'(https://www.facebook.com/)([^/]*)(/)$'
                regex2 = r'(https://www.facebook.com/)([^/]*)([/?ref=py_c]*)$'
                url = elem.get_attribute("href").replace('?ref=py_c','')
                if re.match(regex,url) or re.match(regex2,url) :
                    # check the url exist or not in file

                    if ConfigProcessor.is_url_exists_in_file(path_page, url) == 0 :
                        #     write to file
                        ConfigProcessor.write_to_file(path_page, "\n" + url)

                        loop = loop + 1
                        logger.info(thread_name+ " Write "+url+" to file, total write : "+str(loop))

        except (Exception) :
            logger.info('Invalid URL ')

        time.sleep(2)
