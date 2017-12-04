from time import sleep
from BeautifulSoup import BeautifulSoup

import random
import urllib2
import configuration
import logging
import database
import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.insert(0, dir_path)
from sea_utils import common_utils
from sea_utils import set_proxy
from sea_utils import keywords_perday

common_utils.setup_logging('bing.log')
proxy = set_proxy.set()

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def use_selenium (keyword) :
    status = 0
    try :
        exist = True
        count=1
        req = urllib2.Request('https://www.bing.com/search?q=' + keyword.replace(" ", "%20") + "&first=" + str(count),headers=hdr)
        # limit to 10 page
        while exist and count < 100 :
            keyword = keyword.lower()
            page = urllib2.urlopen(req).read()
            soup = BeautifulSoup(page)

            results = soup.findAll('h2')

            for result in results :
                try :
                    url = result.contents[0].attrs[0][1].lower()
                    title = str(result.contents[0].contents).lower()

                    logging.info(str(count)+'.) '+title)
                    # print str(count)+'.) '+url
                    database.send(url,keyword)
                    count=count+1
                except Exception as e :
                    logging.exception(str(e.message))

            # go to next page
            try :
                if len(results) != 0 :
                    time_loop = 10 + random.randint(1, 30)
                    logging.info('Sleep for a while in ... s : '+str(time_loop))
                    sleep(time_loop)
                    logging.info("go to next page "+str(count/10 ))
                    # print "go to next page "+str(count/10 )
                    req = urllib2.Request('https://www.bing.com/search?q=' + keyword.replace(" ", "%20") + "&first=" + str(count),headers=hdr)
                else :
                    exist = False
            except(Exception) :
                logging.info("Finish next, total sites : "+str(count))
                # print "Finish next, total sites : "+str(count)
                exist = False
    except Exception as e :
        status = 1
        logging.exception(str(e.message))


    return status

keywords = configuration.get_keywords()
logging.info('Total keyword : '+str(len(keywords)))
count_keyword = 1
for keyword in keywords :
    if keywords_perday.check('bing',keyword) == False :
        logging.info(str(count_keyword)+".) Find with keyword : " + keyword)
        status = use_selenium(keyword)
        if status == 1:
            if proxy is not None :
                set_proxy.delete_ip(proxy)
            logging.info('bot detected, sleep in 100 seconds')
            sleep(100)

        time_loop = 10 + random.randint(5, 60)
        logging.info('Sleep for a while in ... s : '+str(time_loop))
        sleep(time_loop)
        count_keyword = count_keyword + 1

logging.info('Exit Process...')
database.close()
