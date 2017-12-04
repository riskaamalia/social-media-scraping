import re
import logging
import SendToDb

from datetime import datetime
from util.UrlProcessor import UrlProcessor
from util.ConfigProcessor import ConfigProcessor
from time import sleep

config_processor = ConfigProcessor()
loop_max = config_processor.config_loop()

def processor (driver,dao,keyword) :
    for kw in keyword :
        try :
            logging.info("Processing finds posts from queries with keyword : "+kw)
            execute_process_to_db(driver, kw.replace(" ","%20"),dao)
        except Exception as e :
            logging.exception(str(e.message))
    driver.quit()

def execute_process_to_db (driver, keyword, dao) :

        driver.get("https://www.facebook.com/search/posts/?q="+keyword)

        scroll_loop = 1
        first_scroll = 0
        total_write = 0
        last_scroll = driver.get_window_size()['height']

        # add this in config to be set , the total loop , and until page go to the very bottom
        while scroll_loop < loop_max :
            # find all related link from posts
            elems = driver.find_elements_by_xpath("//div[@id='browse_result_area']//a[@href]")

            for elem in elems:
                url = elem.get_attribute("href")
                regex = r'(https://l.facebook.com/)(.*)$'
                if re.match(regex,url) :
                    try :
                        real_url = UrlProcessor().get_real_url(url)

                        url = UrlProcessor().get_article_source(real_url)

                        is_exist = dao.is_url_domain_exist(url)
                        if is_exist == 0 :
                            SendToDb.send(real_url,keyword)
                            row = ( url,real_url,"from search",keyword,str(datetime.now().strftime('%Y-%m-%d')) )
                            dao.add_source(row)
                            total_write = total_write + 1
                            logging.info("Write : "+real_url+" total write : "+str(total_write))
                    except Exception as e :
                        logging.info(e.message)
                        logging.info("Next .....")

            sleep(5)
            logging.info("Scroll "+str(last_scroll*scroll_loop)+" == "+str(scroll_loop))
            driver.execute_script("window.scrollTo("+str(first_scroll)+","+str(last_scroll*scroll_loop)+");")
            first_scroll = last_scroll * (scroll_loop - 1)

            scroll_loop = scroll_loop + 1

            try :
                driver.find_element_by_xpath("//div[@class='_24j']")
                logging.info("Finish Loop")
                break
            except Exception as e:
                logging.info('no ending page')
