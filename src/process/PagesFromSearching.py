import re
import time
from selenium.common.exceptions import NoSuchElementException

from util import LoggerConfig
from util.FileProcessor import FileProcessor

logger = LoggerConfig.setConfig()
path_page = FileProcessor.config('path_page')

class PagesFromSearching :

    def processor (driver,thread_name) :
        logger.info("Processing finds page from queries")
        execute_process(driver, "berita", "pages",thread_name)
        driver.quit()


def execute_process (driver, keyword, tab, thread_name) :
        list_url = []

        if not keyword :
            keyword = "berita"

        if not tab :
            tab = "pages"

        driver.get("https://www.facebook.com/search/"+tab+"/?q="+keyword)

        first_scroll = 0
        last_scroll = driver.get_window_size()['height']
        scroll_loop = 1
        total_write_loop = 1

        while True :

            # find all related link
            elems = driver.find_elements_by_xpath("//div[@id='browse_result_area']//a[@href]")
            for elem in elems:
                regex = r'(https://www.facebook.com/)([^/]*)([/?ref=br_rs]*)$'
                url = elem.get_attribute("href").replace('?ref=br_rs','')
                if re.match(regex,url) and url not in list_url :
                        list_url.append(url)


            if list_url.__len__() != 0 :

                logger.info(thread_name+" Get url page from search")
                for list in list_url :
                    if FileProcessor.is_url_exists(path_page, list) == 0 :
                        if total_write_loop == 0 :
                            FileProcessor.write(path_page, list)
                        else :
                            FileProcessor.write(path_page, "\n" + list)

                        logger.info(thread_name+" Write "+list+" to file from recommendation page, total write : "+str(total_write_loop))
                        total_write_loop= total_write_loop+1

            # scroll until end , the end id is phm _64f
            logger.info(thread_name+" scroll "+str(last_scroll*scroll_loop)+" == "+str(scroll_loop))
            driver.execute_script("window.scrollTo("+str(first_scroll)+","+str(last_scroll*scroll_loop)+");")
            first_scroll = last_scroll * (scroll_loop - 1)
            scroll_loop = scroll_loop + 1

            time.sleep(2)

            try :
                driver.find_element_by_xpath("//div[@class='_24j']")
                logger.info(thread_name+" Finish Loop")
                break
            except NoSuchElementException:
                continue
