import datetime
import urllib2
import json
import time
import logging

from BeautifulSoup import BeautifulSoup

class UrlProcessor :

    def get_article_source (self,article_url) :
        return article_url.split("/")[2].replace("\\","")

    def get_real_url (self,facebook_url) :
        response = urllib2.urlopen(facebook_url)
        full_url = BeautifulSoup(response.read()).find('script')
        url = str(full_url).split("(\"")[1].split("\")")[0].replace("\\","")

        return url

    def get_json_body(self,url):
        req = urllib2.Request(url)
        success = False
        while success is False:
            try:
                response = urllib2.urlopen(req)
                if response.getcode() == 200:
                    success = True
            except Exception as e:
                logging.exception (str(e))
                logging.info ("Error for URL %s: %s" % (url, datetime.datetime.now()))
                success = True
                return None

        return json.loads(response.read())


# url = UrlProcessor().get_real_url("https://l.facebook.com/l.php?u=http%3A%2F%2Fwww.antarantb.com%2Fberita%2F33101%2Fkkp-tebar-33700-ekor-benih-ikan-laut-di-lombok-timur&h=ATMEupULx0HdkGbtaOHrOQljcboTLnX5mAdsYGhPMNh884Rs5XHoFuTPg3tGdPiD_P8reFcx3tH8qnc9TqciJhPbmUG-48EpWOORkbpysltmNhYfx_UNwfiJHds2VKtQutdDOKgiHFjuUB2vzw&enc=AZPNwH3yUorR5GZzSLlXWJBdIhsFrU7TibhkCipZbVgK2duCTUrq9ltcDq_4D2IQtq5uIg8o09dzQtmUSkDHn0TYO7XK_77UB3Qwa45cCsrcMJzu1suRQwx0ShoQHwTqm91pMCTF_vKp_vsQ2LaKC1QdLV956_E921GXY0vjXUjP7OcDPFuelKf-jr6AUtscAXIqEzV911ChrtrSjxg1qs6N&s=1")
# print url
