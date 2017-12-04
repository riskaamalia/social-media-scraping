import os
import socket
import logging
import sys
import urllib2
from BeautifulSoup import BeautifulSoup

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

parent1 = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
path = os.path.abspath(os.path.join(parent1, os.pardir))
file_location = path + '/config/proxy.log'

def get_host_name () :
    hostname = socket.gethostname()
    return hostname

# for malaysia IP
def set () :
    logging.info('change proxy')
    proxiest = []
    is_change = True
    try :
        file = open(file_location, 'r')
        proxiest = file.read().splitlines()
    except :
        is_change = False
    if is_change :
        # load from proxy_malaysia.log in config file

        for proxy in proxiest :
            try :
                # test proxy quality first
                pp = urllib2.ProxyHandler({'http': proxy,
                                                    'https': proxy}
                                                )
                auth = urllib2.HTTPBasicAuthHandler()
                opener = urllib2.build_opener(pp, auth, urllib2.HTTPHandler)
                urllib2.install_opener(opener)

                # test first
                urllib2.urlopen('http://python.org', timeout=60)

                # os.environ['http_proxy'] = proxy
                # os.environ['HTTP_PROXY'] = proxy
                # os.environ['https_proxy'] = proxy
                # os.environ['HTTPS_PROXY'] = proxy

                logging.info('change proxy : '+proxy)

                return proxy
            except Exception as e:
                logging.exception(str(e.message)[0:10])
                logging.info('not use this proxy : '+proxy)
                proxy_handler = urllib2.ProxyHandler({})
                opener = urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)

                if proxy is not None:
                    delete_ip(proxy)
    return None

def delete_ip (ip) :
    file = open(file_location, 'r')
    proxiest = file.read().splitlines()
    full_ip_results = ''
    is_delete = False
    for proxy in proxiest :
        if ip != proxy :
            full_ip_results = full_ip_results + proxy + '\n'
        else :
            is_delete = True

    file.close()

    if is_delete == True :
        file = open(file_location, 'w')
        file.write(full_ip_results)

# set()
# req = urllib2.Request('https://www.google.com/search?q=berita',headers=hdr)
# page = urllib2.urlopen(req).read()
# soup = BeautifulSoup(page)
#
# results = soup.findAll("h3")
#
# for result in results:
#     if len(result.contents) > 1:
#         url = result.contents[1].attrs[1][1]
#     elif len(result.contents) == 1:
#         url = result.contents[0].attrs[0][1]
#
#     title = result.text.lower()
#     print url
#     print title