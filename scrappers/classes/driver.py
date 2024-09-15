import logging
import os
from selenium.webdriver import ChromeOptions, Remote, DesiredCapabilities, Chrome
from selenium.webdriver.common.proxy import Proxy, ProxyType

class SeleniumDriver:
    def __init__(self):
        self.driver = None

        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--enable-javascript")

        if os.getenv("PROXY_URL"):
            options.proxy = Proxy({ 'proxyType': ProxyType.MANUAL, 'httpProxy': os.getenv("PROXY_URL").replace("http://", "") })

        if not os.getenv("DOCKER_RUN"):
            self.driver = Chrome(options=options)
        else:
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

            command_executor = os.getenv("CUSTOM_ALONE_NODE") if os.getenv("CUSTOM_ALONE_NODE") else "seleniarm-hub"

            logging.info(f'Starting undetected chromedriver {command_executor}')
            self.driver = Remote(command_executor=f"http://{command_executor}:4444/wd/hub", desired_capabilities=capabilities)
            logging.info(f'Undetected chromedriver started')

    def __del__(self):
        if self.driver:
            self.driver.quit()
            logging.info(f'Сlosed undetected chromedriver')