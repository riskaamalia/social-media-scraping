from time import sleep
from BeautifulSoup import BeautifulSoup
from googleapiclient.discovery import build

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

common_utils.setup_logging('google_search.log')
proxy = set_proxy.set()

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

keys = configuration.config_api()
developer_key = keys[0]
cx = keys[1]

def execute (keyword) :
    status = 0
    try :
        exist = True
        count=1
        is_berikutnya = False
        req = urllib2.Request('https://www.google.com/search?q=' + keyword.replace(" ", "%20") + "&start=" + str(count),headers=hdr)

        while exist == True :
            keyword = keyword.lower()
            page = urllib2.urlopen(req).read()
            soup = BeautifulSoup(page)

            results = soup.findAll("h3")
            get_next_names = soup.findAll('span')
            for get_next_name in get_next_names :
                if 'next' == get_next_name.text.lower() or 'berikutnya' == get_next_name.text.lower() :
                    # #print get_next_name.text.lower()
                    is_berikutnya = True

            # try to limited just 20 page so that all query can be searched
            if is_berikutnya == False or len(results) < 5 or count > 200:
                exist = False
                logging.info("Finish next, total sites : " + str(count))
                #print "Finish next, total sites : "+str(count)
            else :
                for result in results :
                    url = ''
                    try :
                        if len(result.contents) > 1 :
                            url = result.contents[1].attrs[1][1]
                        elif len(result.contents) == 1 :
                            url = result.contents[0].attrs[0][1]

                        title = result.text.lower()

                        logging.info(str(count)+'.) '+title)
                        # print str(count)+'.) '+url
                        #print url
                        if url != '' :
                            database.send(url,keyword)
                        else :
                            exist = False
                    except Exception as e:
                        #print 'not url'
                        logging.info('not url')


                    count=count+1

                # next page
                time_loop = 90 + random.randint(30, 60)
                logging.info('Sleep for a while in ... s : '+str(time_loop))
                sleep(time_loop)
                logging.info("go to next page "+str(count/10 ))
                #print "go to next page "+str(count/10 )
                req = urllib2.Request('https://www.google.com/search?q=' + keyword.replace(" ", "%20") + "&start=" + str(count),headers=hdr)

    except Exception as e :
        #print 'error : '+str(e.message)
        status = 1
        logging.exception(str(e.message))


    return status

# just 100/ day . if 1 keyword limited to 20 page (200 result) so 1 day can only from 5 keyword
# https://www.googleapis.com/customsearch/v1?q=jokowi&alt=json&cx=007245406787592388629:31pu7kcmgdk&siteSearch=kompas.com&key=AIzaSyCvBz6t0EfharKLE9EESojq73RVlMudC_M&start=11
def use_api (keyword) :
    # only until 10 page, google limited
    for page_loop in range(1,100,10) :
        logging.info('start index : '+str(page_loop))
        # print 'start index : '+str(page_loop)
        service = build("customsearch", "v1",developerKey=developer_key)
        res = service.cse().list(
            q=keyword,
            cx= cx,
            # hl='id',
            start=page_loop
        ).execute()

        items = res['items']
        for item in items :
            try :
                title = item['title']
                url = item['link']
                logging.info(title)
                # print title
                database.send(url, keyword)
            except Exception as e :
                logging.exception(str(e.message))

keywords = configuration.get_keywords()
logging.info('Total keyword : '+str(len(keywords)))
count_keyword = 1
bot_count = 0
for keyword in keywords:
    if keywords_perday.check('google_search', keyword) == False :
        logging.info(str(count_keyword)+".) Find with keyword : " + keyword)
        # print "Find with keyword : "+keyword

        try :
            # delete all proxy setting first
            proxy_handler = urllib2.ProxyHandler({})
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)

            use_api(keyword)
        except Exception as e :
            # already limited
            # print str(e.message)
            status = execute(keyword)
            if status == 1 :
                if proxy is not None:
                    set_proxy.delete_ip(proxy)
                logging.info('bot detected, sleep in 100 seconds')
                bot_count = bot_count + 1
                sleep(100)

            # system exit if bot count more than 3 times
            if bot_count > 3 :
                logging.info('Bot count more than 3 times, exit system')
                sys.exit(0)

            time_loop = 180 + random.randint(5, 50)
            logging.info('Sleep for a while in ... s : '+str(time_loop))
            sleep(time_loop)

        count_keyword = count_keyword + 1

logging.info('Exit Process...')
database.close()