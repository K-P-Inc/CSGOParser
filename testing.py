from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import time
import json

options = webdriver.ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('user-data-dir=.')
options.add_argument('--profile-directory=Profile 1')

options.add_argument("--start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)


s = Service(executable_path='chromedriver.exe')

driver = webdriver.Chrome(service=s, options=options)

driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol
    '''
})


steam_link = r'https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20%28Minimal%20Wear%29'

driver.get(steam_link)

main_window = driver.current_window_handle

driver.switch_to.new_window('tab')
new_link = r'https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20%28Field-Tested%29'

driver.get(new_link)

# driver.switch_to.window(main_window)
