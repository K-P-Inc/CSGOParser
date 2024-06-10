import logging
from selenium.webdriver import ChromeOptions, Remote

class SeleniumDriver:
    def __init__(self):
        self.driver = None

        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--enable-javascript")
        options.add_argument("--incognito")

        logging.info(f'Starting undetected chromedriver')
        self.driver = Remote(options=options, command_executor="http://seleniarm-hub:4444/wd/hub")
        logging.info(f'Undetected chromedriver started')

    def __del__(self):
        if self.driver:
            self.driver.quit()
            logging.info(f'Сlosed undetected chromedriver')