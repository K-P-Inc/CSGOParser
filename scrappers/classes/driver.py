import logging
import os
from selenium.webdriver import ChromeOptions, Remote, DesiredCapabilities

class SeleniumDriver:
    def __init__(self):
        self.driver = None

        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--enable-javascript")
        options.add_argument("--incognito")

        capabilities = {
            "browserName": "chrome",
            "selenoid:options": {
                "enableVNC": True
            }
        }
        capabilities.update(options.to_capabilities())

        weapon_parser_type = os.getenv("WEAPON_TYPE")
        if weapon_parser_type:
            capabilities['ps:weaponType'] = weapon_parser_type

        logging.info(f'Starting undetected chromedriver')
        self.driver = Remote(command_executor="http://seleniarm-hub:4444/wd/hub", desired_capabilities=capabilities)
        logging.info(f'Undetected chromedriver started')

    def __del__(self):
        if self.driver:
            self.driver.quit()
            logging.info(f'Сlosed undetected chromedriver')