from selenium import webdriver
from util.ConfigProcessor import ConfigProcessor

def defineDriver () :
    # connect to driver
    driver_location = ConfigProcessor().config_driver_browser()
    driver = webdriver.Chrome(driver_location)
    driver.set_window_size(1920/2, 1080)
    return driver
