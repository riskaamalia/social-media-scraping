# logging
import logging
from util.ConfigProcessor import ConfigProcessor

def setConfig () :
    config_proccessor = ConfigProcessor()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(config_proccessor.config_log_name())
    hdlr = logging.FileHandler(config_proccessor.config_log_location())
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    return logger
