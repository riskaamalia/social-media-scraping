import os
import sys
import logging
import timeout_decorator

dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.insert(0, dir_path)
from sea_libr import sea_check


@timeout_decorator.timeout(30, use_signals=False,exception_message='reach timeout ....')
def send (url,keyword) :

     logging.info("Exist : "+str(sea_check.is_exist(url,'similarweb',keyword))+" url : "+url)
