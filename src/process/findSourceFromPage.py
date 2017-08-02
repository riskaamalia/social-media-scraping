# class _2pie _14i5 _1qkq _1qkx
import re
import time
import urllib.request
import urllib.parse

from bs4 import BeautifulSoup

from util import loggerConfig

logger = loggerConfig.setConfig()
pathFacebookPage = '/home/riskaamalia/Documents/fromGit/my-git/facebook-page-scraping/result-folder/berita-page.txt'
pathPotential = '/home/riskaamalia/Documents/fromGit/my-git/facebook-page-scraping/result-folder/potential-source.tsv'

def processor (driver) :
    logger.info("Process finding source from a page")
    getSource(driver)
    driver.quit()

def getSource (driver) :
    time.sleep(5)
    # go to a page , data from file
    open(pathFacebookPage).readline()

    for line in open(pathFacebookPage) :
        logger.info("From file : "+line)
        try :
            driver.get(line+"posts/")
            time.sleep(5)

            # find all related link to the page
            elems = driver.find_elements_by_xpath("//div[@class='_2pie _14i5 _1qkq _1qkx']//a[@href]")

            for elem in elems:
                url = elem.get_attribute("href")
                regex = r'(https://l.facebook.com/)(.*)$'
                if re.match(regex,url) :
                    logger.info("From facebook : "+url)
                    realUrl = getRealUrl(url)
                    logger.info("Article Source : "+realUrl)
                    url = getArticleSource(realUrl)
                    logger.info("Potential Source : "+url)
                    if isUrlExistInFile(pathPotential,realUrl) == 0 :
                        writeTofile(pathPotential,url+"\t"+line+"\t"+realUrl)

        except (Exception) :
            logger.info('Invalid URL ')

        time.sleep(2)

# write to file per line
def writeTofile (path,content) :
    fWrite = open(path, "a")
    with fWrite as myfile:
        myfile.write(content)
        fWrite.close()

def getArticleSource (articleUrl) :
    return articleUrl.split("/")[2]

def getRealUrl (facebookUrl) :
    response = urllib.request.urlopen(facebookUrl)
    full_url = BeautifulSoup(response.read(),"lxml").find('script')
    url = str(full_url).split("(\"")[1].split("\")")[0]

    return url

def isUrlExistInFile (path,content) :
    exist = 0
    for check in open(path) :
        if content in check :
            exist = 1
            break

    return exist

# regex = r'[^https]*$'
# url = 'https://www.facebook.com/kuku'
# if re.match(regex,url) :
#     print(url)

# article = getRealUrl('https://l.facebook.com/l.php?u=https%3A%2F%2Fberitagar.id%2Fartikel%2Finfografik%2Flhkpn-sebelas-mobil-tjahjo-kalah-mahal-dari-luhut&h=ATNXX5mCEegBmnFA0fkNtKGJXlzrvaU394zPVEoACmjC3TCqrwlBuqIxrw-0NYXVsQsZ2tL5Cs_f-pNstp-pRliLStwK1l2AVSO2Rf2hDRsxewxVnqTcWKIF1BG94eLcJshnKg&enc=AZNYJ-bPfaOH8OYFj0zutc-y0iiM9M_Wj-m6zc3SiquImjxT-nLqJddj6xW7zORY9-oG46T15gwiUNg8lMU3udF5u2EC8sAiObirfRbLxc40z82nBETQITTtIs3UZm4SilA-bWZn34aWV4wN0WDSnBHsuSZhhCDVeaJi7FuMRehaOhYP2DEzJLGvXenE7zecV75K_yS3fk-qB4LbHd1Wvaol&s=1')
# print(article)
# print(getArticleSource(article))
