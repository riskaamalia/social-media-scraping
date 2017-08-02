import re
import time

from util import loggerConfig


logger = loggerConfig.setConfig()
path = '/home/riskaamalia/Documents/fromGit/my-git/facebook-page-scraping/result-folder/facebook-page.txt'

def processor (driver) :
    logger.info("Process finding source from a page")
    # fromRecommendationPage(driver)
    # fromRelatedPage(driver)
    fromSearchPage(driver,"berita")
    driver.quit()

def fromRecommendationPage (driver) :
    listUrl = []

    driver.get("http://www.facebook.com/pages")
    time.sleep(5)

    # find all related link
    elems = driver.find_elements_by_xpath("//div[@id='u_0_2']//a[@href]")
    for elem in elems:
        regex = r'https://www.facebook.com/(.*)/'
        url = elem.get_attribute("href")
        if re.match(regex,url) and url not in listUrl :
                listUrl.append(url)

    if listUrl.__len__() != 0 :
        logger.info("Get url page from recommendation")
        loop = 0
        for list in listUrl :
            if isUrlExistInFile(path,list) == 0 :
                if loop == 0 :
                    writeTofile(path,list)
                else :
                    writeTofile(path,"\n"+list)
            loop= loop+1
            logger.info("Write "+list+" to file from recommendation page, total write : "+str(loop))


def fromSearchPage (driver,keyword) :
    listUrl = []

    if not keyword :
        keyword = "berita"

    driver.get("https://www.facebook.com/search/str/"+keyword+"/keywords_pages")
    time.sleep(5)

    # find all related link
    elems = driver.find_elements_by_xpath("//div[@id='BrowseResultsContainer']//a[@href]")
    for elem in elems:
        regex = r'(https://www.facebook.com/)([^/]*)([/?ref=br_rs]*)$'
        url = elem.get_attribute("href")
        if re.match(regex,url) and url not in listUrl :
                listUrl.append(url)

    # scroll until end


    if listUrl.__len__() != 0 :
        logger.info("Get url page from recommendation")
        loop = 0
        for list in listUrl :
            if isUrlExistInFile(path,list) == 0 :
                if loop == 0 :
                    writeTofile(path,list)
                    print("hehe")
                else :
                    writeTofile(path,"\n"+list)
            loop= loop+1
            logger.info("Write "+list+" to file from recommendation page, total write : "+str(loop))


def fromRelatedPage (driver) :
    time.sleep(5)
    # go to a page , data from file
    open(path).readline()

    for line in open(path) :
        logger.info("From file : "+line)
        try :
            driver.get(line)
            time.sleep(5)

            # find all related link to the page
            elems = driver.find_elements_by_xpath("//div[@class='_5ay5']//a[@href]")
            loop = 0
            for elem in elems:
                regex = r'(https://www.facebook.com/)([^/]*)(/)$'
                regex2 = r'(https://www.facebook.com/)([^/]*)([/?ref=py_c]*)$'
                url = elem.get_attribute("href")
                if re.match(regex,url) or re.match(regex2,url) :
                    # check the url exist or not in file

                    if isUrlExistInFile(path,url) == 0 :
                        #     write to file
                        writeTofile(path,"\n"+url)

                        loop = loop + 1
                        logger.info("Write "+url+" to file, total write : "+str(loop))

        except (Exception) :
            logger.info('Invalid URL ')

        time.sleep(2)

# write to file per line
def writeTofile (path,content) :
    fWrite = open(path, "a")
    with fWrite as myfile:
        myfile.write(content)
        fWrite.close()

def isUrlExistInFile (path,content) :
    exist = 0
    for check in open(path) :
        if content in check :
            exist = 1
            break

    return exist

