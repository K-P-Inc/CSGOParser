import time
import brotli
import json

from seleniumwire import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

def main(item_link):
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--enable-javascript")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(60)

    driver.get(item_link)

    # Open 'View in game page'
    xpath_route = "//button[@class = 'mat-focus-indicator spinner mat-button mat-button-base']"
    element = driver.find_element(By.XPATH, xpath_route)
    element.click()

    time.sleep(5) # Need this break to get logs update

    with open('./market_csgo_parser/item_in_game_link.json', 'w') as item_logs:
        for request in driver.requests:
            if request.response:
                if request.url == 'https://market.csgo.com/api/graphql': # This is market.csgo request to db
                    try:
                        decompressed_data = brotli.decompress(request.response.body)
                        decoded_json = json.loads(decompressed_data.decode('utf-8'))

                        if 'steam://rungame/' in decoded_json['data']['getInGameLink']['gameLink']:
                            item_info = {
                                "item": item_link,
                                "link": decoded_json['data']['getInGameLink']['gameLink']
                            }

                            item_logs.write(json.dumps(item_info, indent=2))
                            item_logs.write('\n')

                    except:
                        pass

    driver.quit()

if __name__ == "__main__":
    item_link = 'https://market.csgo.com/ru/Rifle/AK-47/AK-47%20%7C%20Nightwish%20%28Battle-Scarred%29'
    main(item_link=item_link)
