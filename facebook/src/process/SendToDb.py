import logging
import timeout_decorator
import os
import sys

parent1 = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
parent2 = os.path.abspath(os.path.join(parent1, os.pardir))
dir_path = os.path.abspath(os.path.join(parent2, os.pardir))
sys.path.insert(0, dir_path)
print dir_path

from sea_libr import sea_check

# @timeout_decorator.timeout(30, use_signals=False)
def send_video (page, dict) :

    logging.info("Exist : %r url : "+page,sea_check.is_exist_video(dict))

@timeout_decorator.timeout(30, use_signals=False,exception_message='reach timeout ....')
def send (url,keyword) :

    logging.info("Exist : "+str(sea_check.is_exist(url,'facebook',keyword))+" url : "+url)
