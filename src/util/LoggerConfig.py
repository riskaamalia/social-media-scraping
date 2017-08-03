# logging
import logging

def setConfig () :
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("facebook-scraping")
    hdlr = logging.FileHandler('/home/riskaamalia/Documents/fromGit/my-git/facebook-page-scraping/LOG/fb-scraping.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    return logger
