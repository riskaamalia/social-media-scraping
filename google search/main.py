from time import sleep
from BeautifulSoup import BeautifulSoup

import random
import configuration
import logging
import database
import urllib2
import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.insert(0, dir_path)
from sea_utils import common_utils

common_utils.setup_logging('google_search.log')

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

try :
    input = sys.argv[1].split(',')
    num_process = input[0]
    start=input[1]
    end=input[2]
except :
    num_process = '2'
    start='371'
    end='400'

if num_process is '1' :
    driver = configuration.defineDriver()

def use_selenium (keyword) :
    status = 0
    keyword = keyword.lower()
    driver.get('https://www.google.co.id/search?q='+keyword.replace(" ","%20"))

    exist = True
    count=1
    while exist :
        results = driver.find_elements_by_xpath("//h3[@class='r']//a[@href]")
        if len(results) > 0 :
            for result in results :
                url = result.get_attribute('href')
                title = result.text.lower()

                if keyword in title :
                    logging.info(str(count)+'.) '+title)
                    # print str(count)+'.) '+title
                    database.send(url,keyword)
                    count=count+1
                else :
                    logging.info('last result : '+url)
                    logging.info(title)
                    # print 'last result : '+url
                    # print title
                    exist = False
                    break

            # go to next page
            try :
                time_loop = 10 + random.randint(5, 50)
                logging.info('Sleep for a while in ... s : '+str(time_loop))
                sleep(time_loop)
                try :
                    driver.find_element_by_xpath("//*[text()='Berikutnya']").click()
                except :
                    driver.find_element_by_xpath("//*[text()='Next']").click()
                logging.info("go to next page "+str(count/10 ))
                # print "go to next page "+str(count/10 )
            except(Exception) :
                logging.info("Finish next, total sites : "+str(count))
                # print "Finish next, total sites : "+str(count)
                exist = False
        else :
            logging.info('empty result ...')

            return 1

    return status


def count_links (source_id, url) :
    req = urllib2.Request('https://www.google.com/search?q=site:' + url.lower() , headers=hdr)
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page)
    result = soup.find("div",id='resultStats' ).contents[0]
    # print result
    logging.info(result)
    get_total = result.split(' ')
    if 'Sekitar' in result or 'About' in result :
        total = int(get_total[1].replace('.','').replace(',',''))
    else :
        total = int(get_total[0].replace('.','').replace(',',''))
    database.insert_to_db(source_id,url,total)


if num_process is '1' :
    keywords = database.get_keyword()
    for kk in keywords :
        keyword = kk[0]
        if database.get_keyword_status(keyword) == 0 :
            logging.info("Find with keyword : "+keyword)
            status = use_selenium(keyword)
            while status == 1 :
                driver.close()
                # restart driver
                sleep(10)
                logging.info("bot detected ... restart driver in 10 second")
                driver = configuration.defineDriver()
                status = use_selenium(keyword)
            time_loop = 10 + random.randint(5, 180)
            logging.info('Sleep for a while in ... s : '+str(time_loop))
            sleep(time_loop)
            database.change_keyword_status(keyword,1)
        else :
            database.change_keyword_status(keyword,0)
elif num_process is '2' :
    start = database.get_highest_id()
    is_run = True
    # check highest id first
    end = start + 40
    logging.info("start with id : "+str(start))
    rows = database.get_from_db(start,end)
    is_bot = False
    source_id = 0
    url =''
    while is_run :
        for row in rows :
            if is_bot == False :
                source_id = row[0]
                url = row[1]

            try :
                count_links(source_id, url)

                time_loop = 90 + random.randint(5, 50)
                logging.info('Sleep for a while in ... s : ' + str(time_loop))
                sleep(time_loop)
                is_bot = False
            except Exception as e:
                logging.exception(str(e.message))
                logging.info('stop processing .. bot detected')
                logging.info('sleep for a while in 3000 seconds')
                sleep(3000)
                is_bot = True
                source_id = row[0]
                url = row[1]


        # sleep for next 40 batch, so that captcha will not come
        time_loop = 90 + random.randint(5, 100)
        logging.info('Sleep for next 40 batch in ... s : ' + str(time_loop))
        sleep(time_loop)
        start = end + 1

elif num_process is '3' :
    # only 100 per day
    rows = database.get_from_db(start,end)
    for row in rows :
        use_api(row[0], row[1])

# close chrome
logging.info('Exit Process...')
driver.close()
database.close()
