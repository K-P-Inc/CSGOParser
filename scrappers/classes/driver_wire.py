import logging
import os
from seleniumwire import webdriver

class SeleniumWireDriver:
    def __init__(self):
        self.driver = None

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-extensions')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--proxy-server=market_csgo_link_parser:8097')
        seleniumwire_options={
            'auto_config': False,
            'port': 8097,
            'addr': '0.0.0.0'
        }
        capabilities = {
            "browserName": "chrome",
            "selenoid:options": {
                "enableVNC": True
            }
        }

        weapon_parser_type = os.getenv("WEAPON_TYPE")
        if weapon_parser_type:
            capabilities['ps:weaponType'] = weapon_parser_type

        capabilities.update(options.to_capabilities())
        command_executor = os.getenv("CUSTOM_ALONE_NODE") if os.getenv("CUSTOM_ALONE_NODE") else "seleniarm-hub"

        logging.info('Connecting to selenium wire remote driver')
        self.driver = webdriver.Remote(
            command_executor=f"http://{command_executor}:4444/wd/hub",
            desired_capabilities=capabilities,
            seleniumwire_options=seleniumwire_options
        )


    def __del__(self):
        if self.driver:
            self.driver.quit()
            logging.info(f'Сlosed undetected chromedriver')