# logging
import logging

def setConfig () :
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("facebook-page-scraping")
    hdlr = logging.FileHandler('/home/riskaamalia/Documents/fromGit/my-git/facebook-page-scraping/LOG/myapp.log')
    logger.addHandler(hdlr)

    return logger
