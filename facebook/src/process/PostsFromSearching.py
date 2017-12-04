import re
import time
from datetime import datetime

from util import LoggerConfig
from util.ConfigProcessor import ConfigProcessor
from util.UrlProcessor import UrlProcessor

logger = LoggerConfig.setConfig()
path = ConfigProcessor.config_file_storage('path_source')

class PostsFromSearching :

    def processor (driver,thread_name,dao,keyword) :
        logger.info("Processing finds posts from queries")
        execute_process_to_db(driver,keyword,thread_name, dao)
        driver.quit()

def execute_process_to_db (driver, keyword, thread_name, dao) :

        if str(keyword).__len__() == 0 :
            keyword = "berita"

        driver.get("https://www.facebook.com/search/posts/?q="+keyword)

        scroll_loop = 1
        first_scroll = 0
        total_write = 0
        last_scroll = driver.get_window_size()['height']

        while scroll_loop < 10 :
            # find all related link from posts
            elems = driver.find_elements_by_xpath("//div[@id='browse_result_area']//a[@href]")

            for elem in elems:
                try :
                    url = elem.get_attribute("href")
                    regex = r'(https://l.facebook.com/)(.*)$'
                    if re.match(regex,url) :
                        real_url = UrlProcessor.get_real_url(url)

                        url = UrlProcessor.get_article_source(real_url)

                        is_exist = dao.is_url_source_exist(real_url)
                        if is_exist == 0 :
                            # from sqlite is a tuple , so fb_page [0]
                            row = ( url,real_url,"from search",str(datetime.now()) )
                            dao.add_source(row)
                            total_write = total_write + 1
                            logger.info(thread_name+" Write : "+real_url+" total write : "+str(total_write))

                except (Exception) :
                    logger.info(thread_name+' Invalid URL ')

            logger.info(thread_name+" scroll "+str(last_scroll*scroll_loop)+" == "+str(scroll_loop))
            driver.execute_script("window.scrollTo("+str(first_scroll)+","+str(last_scroll*scroll_loop)+");")
            first_scroll = last_scroll * (scroll_loop - 1)
            scroll_loop = scroll_loop + 1

            time.sleep(1)

        time.sleep(2)

def execute_process (driver, keyword, tab, thread_name) :

        if not keyword :
            keyword = "berita"

        if not tab :
            tab = "posts"

        driver.get("https://www.facebook.com/search/"+tab+"/?q="+keyword)

        scroll_loop = 1
        first_scroll = 0
        total_write = 0
        last_scroll = driver.get_window_size()['height']

        while scroll_loop < 10 :
            # find all related link from posts
            elems = driver.find_elements_by_xpath("//div[@id='browse_result_area']//a[@href]")

            for elem in elems:
                try :
                    url = elem.get_attribute("href")
                    regex = r'(https://l.facebook.com/)(.*)$'
                    if re.match(regex,url) :
                        # logger.info("From facebook : "+url)
                        real_url = UrlProcessor.get_real_url(url)

                        # logger.info("Article Source : "+real_url)
                        url = UrlProcessor.get_article_source(real_url)

                        # logger.info("Potential Source : "+url)

                        if ConfigProcessor.is_url_exists_in_file(path, real_url) == 0 :
                            ConfigProcessor.write_to_file(path, "\n" + url + "\t" + real_url)
                            total_write = total_write + 1
                            logger.info(thread_name+" Write : "+real_url+" total write : "+str(total_write))
                        # else :
                        #     logger.info("Write : url exist")

                except (Exception) :
                    logger.info(thread_name+' Invalid URL ')

            logger.info(thread_name+" scroll "+str(last_scroll*scroll_loop)+" == "+str(scroll_loop))
            driver.execute_script("window.scrollTo("+str(first_scroll)+","+str(last_scroll*scroll_loop)+");")
            first_scroll = last_scroll * (scroll_loop - 1)
            scroll_loop = scroll_loop + 1

            time.sleep(1)

        time.sleep(2)
