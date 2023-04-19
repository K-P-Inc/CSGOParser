from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import time
import json

options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=C:\\Users\\coolm\\AppData\\Local\\Google\\Chrome\\User Data\\Default')

options.add_argument("--start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

s = Service(executable_path='./User/chromedriver.exe')

driver = webdriver.Chrome(service=s, chrome_options=options)

driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol
    '''
})

def config():
    with open('json_data.json', 'r', encoding="utf-8") as config:
        skins_config = json.load(config)
        return skins_config

def best_idea(config):
    def steam_price_checker(link_for_steam):
        try:
            main_window = driver.current_window_handle
            steam_link = r'https://steamcommunity.com/market/listings/730/'
            currect_link = steam_link + link_for_steam
            driver.switch_to.new_window('tab')
            driver.get(currect_link)
            price = driver.find_element(By.XPATH, '//*[@class = "market_listing_price market_listing_price_with_fee"]').text
            driver.close()
            driver.switch_to.window(main_window)                
        finally:
            return int(price[:price.find(',')])


    for_replace_front, for_replace_back  = 'background-image: url("https://steamcdn-a.akamaihd.net/apps/730/icons/econ/stickers/', '.png");'
    rarity = ['Well-Worn', 'Field-Tested', 'Battle-Scarred', 'Minimal Wear', 'Factory New']
    try:
        for quality in rarity:
            url = [f'https://market.csgo.com/ru/?sort=price&order=asc&search=AK-47%20%7C%20Slate%20({quality})&priceMax=1000000&categories=any_stickers']
            for link in url:
                driver.get(link)
                if r'AK-47%20%7C%20Slate%20(Well-Worn)' in link:
                    steam_price = int(steam_price_checker(r'AK-47%20%7C%20Slate%20%28Well-Worn%29') / 80 )
                elif r'AK-47%20%7C%20Slate%20(Field-Tested)' in link:
                    steam_price = int(steam_price_checker(r'AK-47%20%7C%20Slate%20%28Field-Tested%29') / 80)
                elif r'AK-47%20%7C%20Slate%20(Battle-Scarred)' in link:
                    steam_price = int(steam_price_checker(r'AK-47%20%7C%20Slate%20%28Battle-Scarred%29') / 80)
                elif r'AK-47%20%7C%20Slate%20(Minimal Wear)' in link:
                    steam_price = int(steam_price_checker(r'AK-47%20%7C%20Slate%20%28Minimal%20Wear%29') / 80)
                elif r'AK-47%20%7C%20Slate%20(Factory New)' in link:
                    steam_price = int(steam_price_checker(r'AK-47%20%7C%20Slate%20%28Factory%20New%29') / 80)
                print(f'Steam price - {steam_price} $')
                actions = ActionChains(driver)
                driver.implicitly_wait(20)
                skins_data = []
                while True:
                    item_url = driver.find_elements(By.XPATH, "//a[contains(@href, '/ru/Rifle')]")
                    for i in item_url:
                        sticker_data = i.find_elements(By.XPATH, './/*[starts-with(@class, "stickers")]//*[starts-with(@class, "sticker ")]')
                        sum = 0
                        stickers = []
                        for b in sticker_data[0:(len(sticker_data)//2)]:
                            sticker = b.find_element(By.XPATH, './/*[starts-with(@class, "sticker-img")]').get_attribute('style')
                            sticker_for_config = sticker.replace(for_replace_front, '').replace(for_replace_back, '').split('.')[0]
                            if sticker_for_config in config and 'price' in config[sticker_for_config]:
                                sum = config[sticker_for_config]['price'] + sum
                                stickers.append(config[sticker_for_config]['name'])
                            if len(stickers) == 4 and stickers[0] == stickers[1] and stickers[1] == stickers[2] and stickers[2] == stickers[3] and sum > steam_price:
                                if (((((config[sticker_for_config]['price'] *0.5) + steam_price) - (float(i.text.split()[1]))) *100)/(float(i.text.split()[1]))) >= 30:
                                    if i.get_attribute('href') not in skins_data:
                                        skins_data.append(i.get_attribute('href'))
                                        print(f"\n{i.get_attribute('href')}\n{' '.join(i.text.split()[4:])}: {float(i.text.split()[1]):.2f} $")
                                        print(f"{config[sticker_for_config]['name']} - {config[sticker_for_config]['price']:.2f} $")
                                        print(f"Sum of stickers: {sum:.2f} $ ")
                                        print(f"Процент потенциальной выручки - {(((((config[sticker_for_config]['price'] * 0.5) + steam_price) - (float(i.text.split()[1]))) *100)/(float(i.text.split()[1]))):.2f} %")

                    element = item_url[-1]
                    actions.move_to_element(element).perform()
                    if driver.find_elements(By.XPATH, "//a[contains(@href, '/ru/Rifle')]")[-1] == element:
                        break

        time.sleep(15)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

best_idea(config())
