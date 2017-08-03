
import re

import time

from util import LoggerConfig
from util.FileProcessor import FileProcessor
from util.UrlProcessor import UrlProcessor

logger = LoggerConfig.setConfig()
path = FileProcessor.config('path_source')
path_page = FileProcessor.config('path_page')

class PostsFromPages :

    def processor (driver,thread_name) :
        logger.info("Processing finds posts from page")
        execute_process(driver,thread_name)
        driver.quit()


def execute_process (driver,thread_name) :

    # get all recommendation page first TO-DO


    # go to a page , data from file , get posts
    open(path_page).readline()
    total_write = 0
    count_page_source = 0

    for line in open(path_page) :
        logger.info(thread_name+" From file : "+line)
        try :
            driver.get(line+"posts/")
            time.sleep(5)

            scroll_loop = 1
            first_scroll = 0
            last_scroll = driver.get_window_size()['height']
            while scroll_loop < 6 :
                # find all related link to the page
                elems = driver.find_elements_by_xpath("//div[@class='_2pie _14i5 _1qkq _1qkx']//a[@href]")

                for elem in elems:
                    url = elem.get_attribute("href")
                    regex = r'(https://l.facebook.com/)(.*)$'
                    if re.match(regex,url) :
                        # logger.info("From facebook : "+url)
                        real_url = UrlProcessor.get_real_url(url)

                        # logger.info("Article Source : "+real_url)
                        url = UrlProcessor.get_article_source(real_url)

                        # logger.info("Potential Source : "+url)

                        if FileProcessor.is_url_exists(path,real_url) == 0 :
                            FileProcessor.write(path,url+"\t"+real_url+"\t"+line)
                            total_write = total_write + 1

                            logger.info(thread_name+" Write : "+real_url+" total write : "+str(total_write))
                        # else :
                        #     logger.info("Write : url exist")

                logger.info(thread_name+" scroll "+str(last_scroll*scroll_loop)+" == "+str(scroll_loop))
                driver.execute_script("window.scrollTo("+str(first_scroll)+","+str(last_scroll*scroll_loop)+");")
                first_scroll = last_scroll * (scroll_loop - 1)
                scroll_loop = scroll_loop + 1

        except (Exception) :
            logger.info('Invalid URL ')

        time.sleep(2)
        count_page_source += 1
        logger.info(thread_name+" "+str(count_page_source)+" page source is readed")

        if count_page_source == 3 :
            break
