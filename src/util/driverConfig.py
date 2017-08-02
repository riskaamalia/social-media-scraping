from selenium import webdriver


def defineDriver () :
    # connect to driver
    driver = webdriver.Chrome('/usr/local/share/chromedriver')
    driver.set_window_size(1920/2, 1080)
    return driver
