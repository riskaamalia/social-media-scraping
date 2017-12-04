from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
import logging
import time
import os
from logging.handlers import TimedRotatingFileHandler

# path_driver = '/usr/local/bin/chromedriver'
path_driver = '/usr/bin/chromedriver'

def defineDriver () :
    # connect to driver
    display = Display(visible=0, size=(1920/2,1080))
    display.start()
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(executable_path=path_driver,chrome_options=chrome_options)
    driver.set_window_size(1920/2, 1080)
    return driver

parent1 = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
path = os.path.abspath(os.path.join(parent1, os.pardir))

def get_keywords () :
        location = path + "/config/keyword.log"
        f = open(location,'r')
        value = f.read().splitlines()

        return value

def config_api () :
    developer_key = ''
    cx = ''
    row = [developer_key,cx]

    return row