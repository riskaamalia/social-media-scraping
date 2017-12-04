
import re
import time
import logging

class PagesFromRelatedPage :

    def processor (self,driver,dao) :
        logging.info("Processing finds related page from page")
        execute_process_to_db(driver,dao)
        driver.quit()

def execute_process_to_db (driver,dao) :

    # go to a page , data from db
    pages = dao.get_page()

    loop = 0
    for page in pages :
        logging.info("From Db : "+page[0])
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
                        row = (url,"from related page")
                        dao.add_page(row)
                        loop = loop + 1
                        logging.info("Write : "+url+" total write : "+str(loop))

        except (Exception) :
            logging.info('Invalid URL ')

        time.sleep(2)
