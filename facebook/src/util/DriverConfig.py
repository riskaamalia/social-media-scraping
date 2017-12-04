from selenium import webdriver
from util.ConfigProcessor import ConfigProcessor
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options

def defineDriver (proxy, country) :
    # connect to driver
    display = Display(visible=0, size=(1920/2,1080))
    display.start()
    driver_location = ConfigProcessor().config_driver_browser()
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    if country != 'id' and proxy is not None :
        chrome_options.add_argument('--proxy-server=%s' % proxy)
    driver = webdriver.Chrome(executable_path=driver_location,chrome_options=chrome_options)
    driver.set_window_size(1920/2, 1080)
    return driver
