from BeautifulSoup import BeautifulSoup
from datetime import datetime
from time import sleep
from time import time
import configuration
import logging
import urllib2
import os
import sys
import json
import database

dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.insert(0, dir_path)
from sea_utils import common_utils

common_utils.setup_logging('similarweb_api.log')

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
values = configuration.get_api_key_and_country()

api_key = values[0].split(' = ')[1]
country = values[1].split(' = ')[1]
link_categories = values[2].split(' = ')[1]
categories = []

def get_categories () :

    req = urllib2.Request(link_categories, headers=hdr)
    page = urllib2.urlopen(req).read()
    xmls = BeautifulSoup(page)

    recursive_xmls(xmls)

def recursive_xmls (xmls) :

    for xml in xmls :
        if '<' in str(xml):
            recursive_xmls(xml)
        else :
            categories.append(xml)

def get_100_topsites () :

    date = str(datetime.now().year)+'-'+str(datetime.now().month - 1)

    # use recursive
    get_categories()

    total_error = 0
    loop = 1
    total_urls = 0
    total_time = 0
    logging.info('Total categories : '+str(len(categories)))
    for cc in categories:
        start = time()
        json_results = None
        loop_result = 0
        try :
            # start time
            api_format = 'https://api.similarweb.com/v1/website/%24'+cc+'/topsites/topsites?' \
                     'api_key='+api_key+'&country='+country+'&start_date='+date+'&end_date='+date

            #get json result
            req = urllib2.Request(api_format, headers=hdr)
            page = urllib2.urlopen(req,timeout=60).read()

            json_results = json.loads(page)

            for result in json_results['top_sites'] :
                url = result['domain']

                if 'http' not in url or 'https' not in url :
                    url = 'http://'+url

                logging.info('got this site : '+url)
                try :
                    database.send(url,cc)
                except Exception as e :
                    logging.exception(str(e.message))
                loop_result = loop_result + 1
                total_error = 0
        except Exception as e:
            logging.exception(str(e.message))
            total_error = total_error + 1

            # end process
            if total_error > 4 :
                logging.info('End process ...')
                sys.exit(0)

            logging.exception('sleep in 100 seconds')
            sleep(100)

        time_execute = time()-start
        logging.info(str(loop) + '.) category : ' + cc + ' #FINISH in : '+str(time_execute)+' seconds')

        if json_results is None or loop_result == 0 :
            logging.info(str(loop) + '.) category : ' + cc + ' #EMPTY country : '+ country)

        # total urls
        total_urls = total_urls + loop_result
        # total all time
        total_time = total_time + time_execute

        loop = loop + 1

    logging.info('#ALL finish , total urls : '+str(total_urls)+' , total time in minutes : ' + str(total_time/60))

get_100_topsites()
