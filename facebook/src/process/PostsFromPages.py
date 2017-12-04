import re
import time
import logging
import SendToDb

from datetime import datetime
from util.UrlProcessor import UrlProcessor
from util.ConfigProcessor import ConfigProcessor

config_processor = ConfigProcessor()
loop_max = config_processor.config_loop()

class PostsFromPages :

    def processor (self,driver,dao) :
        logging.info("Processing finds posts from page")
        execute_process_to_db(driver,dao)
        driver.quit()

def execute_process_to_db (driver,dao) :

    # go to a page , data from db
    fb_pages = dao.get_page()
    total_write = 0
    count_page_source = 0

    for fb_page in fb_pages :
        logging.info("From Fb Page : "+fb_page[0])
        try :
            driver.get(fb_page[0]+"posts/")
            time.sleep(5)

            scroll_loop = 1
            first_scroll = 0
            last_scroll = driver.get_window_size()['height']

            # add this in config to be set , the total loop , and until page go to the very bottom
            while scroll_loop < loop_max :
                # find all related link to the page
                elems = driver.find_elements_by_xpath("//div[@class='_2pie _14i5 _1qkq _1qkx']//a[@href]")

                for elem in elems:
                    url = elem.get_attribute("href")
                    regex = r'(https://l.facebook.com/)(.*)$'
                    if re.match(regex,url) :
                        real_url = UrlProcessor().get_real_url(url)

                        url = UrlProcessor().get_article_source(real_url)

                        # return 0 if not exist
                        is_exist = dao.is_url_domain_exist(real_url)
                        if is_exist == 0 :
                            SendToDb.send(real_url,fb_page[1])
                            # from sqlite is a tuple , so fb_page [0]
                            row = ( url,real_url,fb_page[0],fb_page[1],str(datetime.now()) )
                            dao.add_source(row)
                            total_write = total_write + 1
                            logging.info("Write : "+real_url+" total write : "+str(total_write))


                logging.info("Scroll "+str(last_scroll*scroll_loop)+" == "+str(scroll_loop))
                driver.execute_script("window.scrollTo("+str(first_scroll)+","+str(last_scroll*scroll_loop)+");")
                first_scroll = last_scroll * (scroll_loop - 1)
                scroll_loop = scroll_loop + 1

        except Exception as e:
            print e
            logging.info('Invalid URL ')

        time.sleep(2)
        count_page_source += 1
        logging.info(str(count_page_source)+" page source is readed")


