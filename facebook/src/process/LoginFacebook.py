from selenium.webdriver.common.keys import Keys
from util import LoggerConfig
logger = LoggerConfig.setConfig()


def login (driver, username, password) :

    # log in to facebook first
    driver.get("http://www.facebook.com")

    # element for log in
    assert "Facebook" in driver.title
    elem = driver.find_element_by_id("email")
    elem.send_keys(username)
    elem = driver.find_element_by_id("pass")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)

    # try to log in
    try:
        elem = driver.find_element_by_css_selector(".input.textInput")
        elem.send_keys("Posted using Python's Selenium WebDriver bindings!")
        elem = driver.find_element_by_css_selector("input[value=\"Publicar\"]")
        elem.click()
    except (Exception) :
        logger.info('Exception, I do not know')

    # click pop up
    try :
        driver.find_element_by_xpath("//*[text()='Lain Kali']").click()
    except(Exception) :
        logger.info("Pop up does not come")
