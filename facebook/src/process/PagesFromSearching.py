import re
import time
import logging

from selenium.common.exceptions import NoSuchElementException

class PagesFromSearching :

    def processor (self,driver,dao,keyword) :
        for kw in keyword :
            logging.info("Processing finds pages from queries with keyword : "+kw)
            execute_process_to_db(driver, kw,dao)
        driver.quit()

def execute_process_to_db (driver, keyword,dao) :
        list_url = []

        if str(keyword).__len__() == 0 :
            keyword = "berita"

        driver.get("https://www.facebook.com/search/pages/?q="+keyword.replace(" ","%20"))

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

                logging.info("Get url page from search")
                for list in list_url :

                    is_exist = dao.is_url_page_exist(list)
                    if is_exist == 0 :
                        row = (list,keyword)
                        dao.add_page(row)

                        logging.info("Write "+list+" to file from recommendation page, total write : "+str(total_write_loop))
                        total_write_loop= total_write_loop+1

            # scroll until end , the end id is phm _64f
            logging.info("Scroll "+str(last_scroll*scroll_loop)+" == "+str(scroll_loop))
            driver.execute_script("window.scrollTo("+str(first_scroll)+","+str(last_scroll*scroll_loop)+");")
            first_scroll = last_scroll * (scroll_loop - 1)
            scroll_loop = scroll_loop + 1

            time.sleep(2)

            try :
                driver.find_element_by_xpath("//div[@class='_24j']")
                logging.info("Finish Loop")
                break
            except NoSuchElementException:
                continue
