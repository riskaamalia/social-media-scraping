import urllib2
import sys
import os
from BeautifulSoup import BeautifulSoup
dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, dir_path)

def insert (ip) :
    location = dir_path + "/config/proxy.log"

    acess_file = open(location,'a+')
    check_read = acess_file.read().splitlines()

    is_exist = False
    for check in check_read :
        if ip == check :
            is_exist = True
            break

    if is_exist == False :
        acess_file.write(ip+'\n')

    acess_file.close()

    return is_exist

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def run (country_code) :
    req = urllib2.Request('https://www.proxynova.com/proxy-server-list/country-'+country_code+'/',headers=hdr)
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page)
    body_table = soup.findAll("td")
    ip = ''

    for b in body_table :
        test = b.find("script")
        if test is not None :
            ip = test.text.replace("document.write('23","").replace("'.substr(2) + '","").replace("');","").strip()
        elif len(b.text) < 5 and len(b.text) > 1 :
            port = b.text
            proxy = ip+":"+port

            # test proxy quality first
            pp = urllib2.ProxyHandler({'http': proxy,
                                       'https': proxy}
                                      )
            auth = urllib2.HTTPBasicAuthHandler()
            opener = urllib2.build_opener(pp, auth, urllib2.HTTPHandler)
            urllib2.install_opener(opener)

            try :
                # test first
                urllib2.urlopen('http://google.com', timeout=60)
                print ip + ":" + port + ' : ' + str(insert(proxy))
            except :
                proxy_handler = urllib2.ProxyHandler({})
                opener = urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)

# my , th , vn
run(sys.argv[1])