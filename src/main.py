from util import driverConfig
from process import loginFacebook
from process import findPage
from process import findSourceFromPage
# set driver configuration
driver = driverConfig.defineDriver()

# log in facebook
loginFacebook.login(driver)

# find facebook page process
findPage.processor(driver)

# try to get another source
# findSourceFromPage.processor(driver)
