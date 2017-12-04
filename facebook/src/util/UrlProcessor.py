import urllib

from bs4 import BeautifulSoup


class UrlProcessor :

    def get_article_source (article_url) :
        return article_url.split("/")[2].replace("\\","")

    def get_real_url (facebook_url) :
        response = urllib.request.urlopen(facebook_url)
        full_url = BeautifulSoup(response.read(),"lxml").find('script')
        url = str(full_url).split("(\"")[1].split("\")")[0].replace("\\","")

        return url
