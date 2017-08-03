
import re

import time

from util import LoggerConfig
from util.FileProcessor import FileProcessor

logger = LoggerConfig.setConfig()
path_page = FileProcessor.config('path_page')

class PagesFromRelatedPage :

    def processor (driver,thread_name) :
        logger.info("Processing finds related page from page")
        execute_process(driver,thread_name)
        driver.quit()


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

                    if FileProcessor.is_url_exists(path_page, url) == 0 :
                        #     write to file
                        FileProcessor.write(path_page, "\n" + url)

                        loop = loop + 1
                        logger.info(thread_name+ " Write "+url+" to file, total write : "+str(loop))

        except (Exception) :
            logger.info('Invalid URL ')

        time.sleep(2)
