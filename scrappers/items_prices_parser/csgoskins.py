import json
import logging
import datetime
import os
import requests
import time
from dotenv import load_dotenv
from classes import DBClient
from urllib.parse import urlparse, quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


qualitys = ['factory-new', 'minimal-wear', 'field-tested', 'well-worn', 'battle-scarred']
market_names = [
    "Skinport", "GamerPay", "Lis Skins", "CS.MONEY", "SkinBaron",
    "SkinSwap", "BUFF163", "BitSkins", "WAXPEER", "ShadowPay",
    "Market CSGO", "CSFloat", "HaloSkins", "CS.DEALS", "DMarket",
    "Tradeit.gg", "Mannco.store", "Steam", "BUFF Market", "SkinBid"
]
periods = ['7 Day', '30 Day', 'All Time']
statistics = ['Low', 'High']


def alt_xpath(alt):
    return f"//*[contains(@alt, '{alt}')]//..//..//..//.."


def active_offers_xpath(driver, alt):
    try:
        active_offers_xpath = "//*[contains(text(), 'active offers')]//..//..//*[2]"
        active_offers_text = driver.find_element(By.XPATH, f"{alt_xpath(alt)}{active_offers_xpath}").text
        active_offers_price = int(active_offers_text) if 'K' not in active_offers_text else int(float(active_offers_text.replace('K','')) * 1000)
        return active_offers_price or None
    except NoSuchElementException as e:
        return None


def price_offers_xpath(driver, alt):
    try:
        price_from = "//*[text() = 'from']//..//..//*[2]"
        price_text = driver.find_element(By.XPATH, f"{alt_xpath(alt)}{price_from}").text.replace('$','')
        price_float = float(price_text) if ',' not in price_text else float(price_text.replace(',',''))
        return price_float or None
    except NoSuchElementException as e:
        return None


def get_market_prices(driver, alts):
    for alt in alts:
        if alt_xpath(alt):
            return {'active_offers': active_offers_xpath(driver, alt), 'price': price_offers_xpath(driver, alt)}


def price_statistics_xpath(period):
    return f"//*[@class = 'order-[24]']//*[@class = 'flex px-4 py-2']//*[contains(text(), '{period}')]//../*[2]"


class Driver(webdriver.Chrome):
    def __init__(self, **kwargs):
        options = webdriver.ChromeOptions()

        # Отключает расширения браузера.
        options.add_argument('--disable-extensions')
        # Отключает использование GPU для ускорения отрисовки страницы. Может быть полезно в виртуальных средах.
        options.add_argument('--disable-gpu')
        # Запускает браузер в безопасном режиме, отключая некоторые функции безопасности.
        options.add_argument('--no-sandbox')

        super().__init__(options=options, **kwargs)


def create_driver():
    try:
        driver = Driver()
        driver.implicitly_wait(0.1)
        return driver
    except Exception as e:
        print(f"Failed to create WebDriver: {e}")
        return None


def find_items_for_parsing_without_quality(driver, url, page):
    time.sleep(1)
    driver.get(f'{url}&page={page}')
    links = driver.find_elements(By.XPATH, '//a[starts-with(@href, "https://csgoskins.gg/items/")]')

    correct_links = []
    for link in links:
        href = link.get_attribute('href')
        parsed_url = urlparse(href)
        path_segments = parsed_url.path.strip('/').split('/')
        if len(path_segments) == 2:
            correct_links.append(href)

    return set(correct_links)


def find_items_global_links(driver):
    items_links_without_quality = []
    file_path = "data/items_links_without_quality.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            items_links_without_quality = json.load(file)

    if items_links_without_quality:
        return items_links_without_quality

    pages = 212
    for page in range(1, pages + 1):
        links = find_items_for_parsing_without_quality(driver, 'https://csgoskins.gg/?order=lowest_price', page)

        for link in links:
            items_links_without_quality.append(link)

    with open(file_path, "w") as file:
        json.dump(items_links_without_quality, file, indent=4)

    return items_links_without_quality


def parse_global_weapon_information(driver, url):
    time.sleep(1)
    driver.get(url)
    driver.implicitly_wait(0.5)

    skin_name = driver.find_element(By.XPATH, '//h1[@class="text-2xl sm:text-3xl font-bold"]').text

    types_config = []
    try:
        for type_link in driver.find_elements(By.XPATH, f'//a[starts-with(@href, "{url}")]'):
            type_name = type_link.find_element(By.XPATH, './/div[@class="w-2/3 flex-none"]').text
            types_config.append({
                "link": type_link.get_attribute("href"),
                "name": type_name.replace("StatTrak ", "").replace("Souvenir ", ""),
                "is_stattrak": type_name.startswith("StatTrak"),
                "is_souvenir": type_name.startswith("Souvenir"),
            })
    except NoSuchElementException:
        types_config = []

    try:
        summary_element = driver.find_element(By.XPATH, '//h2[text()="Summary"]')
        summary_parent_element = summary_element.find_element(By.XPATH, './ancestor::div[@class="mt-12"]/following-sibling::div[@class="shadow-md bg-gray-800 rounded mt-4"]')
        summary_sub_elements = summary_parent_element.find_elements(By.XPATH, './div[@class="flex px-4 py-2"]')
        skin_summary = {}
        for child in summary_sub_elements:
            key, _, value = child.text.partition("\n")
            skin_summary[key] = value.replace("\"", "")
    except NoSuchElementException:
        skin_summary = {}

    try:
        item_class_element = driver.find_element(By.XPATH, '//h2[text()="Item Class"]')
        item_class_parent_element = item_class_element.find_element(By.XPATH, './ancestor::div[@class="mt-12"]/following-sibling::div[@class="flex mt-4"]')
        item_class_sub_elements = item_class_parent_element.find_elements(By.XPATH, './div[@class="w-1/2"]')
        item_class_names = [item_class.text for item_class in item_class_sub_elements]
    except NoSuchElementException:
        item_class_names = []

    try:
        collections_element = driver.find_element(By.XPATH, '//h2[text()="Collections"]')
        collections_parent_element = collections_element.find_element(By.XPATH, './ancestor::div[@class="mt-12 mb-6"]/following-sibling::div[@class="flex -mx-4 flex-wrap"]')
        collections_sub_elements = collections_parent_element.find_elements(By.XPATH, './div[@class="w-1/2 sm:w-1/3 md:w-1/4 lg:w-1/3 p-4"]')
        collections_names = [collection_element.text for collection_element in collections_sub_elements]
    except NoSuchElementException:
        collections_names = []

    try:
        containers_element = driver.find_element(By.XPATH, '//h2[text()="Containers"]')
        containers_parent_element = containers_element.find_element(By.XPATH, './ancestor::div[@class="mt-12 mb-6"]/following-sibling::div[@class="flex -mx-4 flex-wrap"]')
        containers_sub_elements = containers_parent_element.find_elements(By.XPATH, './div[@class="w-1/2 sm:w-1/3 md:w-1/4 lg:w-1/3 p-4"]')
        containers_names = [container_element.text for container_element in containers_sub_elements]
    except NoSuchElementException:
        containers_names = []

    try:
        colors_element = driver.find_element(By.XPATH, '//h2[text()="Colors"]')
        colors_parent_element = colors_element.find_element(By.XPATH, './ancestor::div[@class="mt-12 mb-6"]/following-sibling::div[@class="flex -mx-4 flex-wrap"]')
        colors_sub_elements = colors_parent_element.find_elements(By.XPATH, './div[@class="w-full flex p-4"]/a')
        colors_names = [color_element.get_attribute('aria-label') for color_element in colors_sub_elements]
    except NoSuchElementException:
        colors_names = []

    return {
        "name": skin_name,
        "link": url,
        "types": types_config,
        "item_classes": item_class_names,
        "collections": collections_names,
        "containers": containers_names,
        "colors": colors_names,
        "summary": skin_summary
    }


def find_items_description(driver, items_list):
    global_weapon_configs = []
    file_path = "data/global_weapon_configs.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            global_weapon_configs = json.load(file)

    if global_weapon_configs:
        return global_weapon_configs

    for url in items_list:
        global_weapon_configs.append(parse_global_weapon_information(driver, url))

    with open(file_path, "w") as file:
        json.dump(global_weapon_configs, file, indent=4)

    return global_weapon_configs


def get_item_icon(driver):
    icon = None
    try:
        icon = driver.find_element(By.XPATH, "//img[@id = 'main-image']").get_attribute('src')
    finally:
        return icon


def get_price_values(driver, price_values):
    try:
        for period in periods:
            for stat in statistics:
                value = float(driver.find_element(By.XPATH, price_statistics_xpath(f'{period} {stat}')).text.replace('$',''))
                price_values[f'{period} {stat}'] = value
    finally:
        return price_values


def fetch_market_data(driver, item_link, price_values):
    time.sleep(1)
    driver.get(item_link)
    prices = get_price_values(driver, price_values)
    markets_data = {market: get_market_prices(driver, market) for market in market_names}

    return prices, markets_data


def try_to_get_price_from_steam_api(market_hash_name):
    try:
        url = f"http://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name={quote(market_hash_name)}&currency=1"

        response = requests.request("GET", url)
        response_json = json.loads(response.text)

        price = response_json.get("median_price", -1)

        if price != -1:
            return float(price[1:])
        return -1
    except:
        return -1


def update_item_with_prices(item, prices, markets_data, name):
    price = -1
    for market_name, market_value in markets_data.items():
        if market_name == "Steam":
            price = market_value["price"]

    if price == -1:
        price = try_to_get_price_from_steam_api(name)

    if price == -1:
        if prices['7 Day Low'] <= 1200:
            price = prices['7 Day Low'] * 1.3
        else:
            price = prices['7 Day Low']

    item["price"] = price
    item['markets'] = markets_data
    item['week_low_value'] = prices['7 Day Low']
    item['week_high_value'] = prices['7 Day High']
    item['month_low_value'] = prices['30 Day Low']
    item['month_high_value'] = prices['30 Day High']
    item['all_time_low'] = prices['All Time Low']
    item['all_time_high'] = prices['All Time High']

    return item


def update_weapon_price_in_and_skins(updated_item, updated_item_type, markets_data):
    db_client = DBClient()
    db_client.update_weapon_prices([(
        updated_item["name"],
        updated_item_type["name"],
        updated_item_type["is_stattrak"],
        updated_item_type["price"],
        json.dumps(markets_data),
        updated_item_type['week_low_value'],
        updated_item_type['week_high_value'],
        updated_item_type['month_low_value'],
        updated_item_type['month_high_value'],
        updated_item_type['all_time_low'],
        updated_item_type['all_time_high'],
        datetime.datetime.now(),
        get_item_image_url(f'{updated_item["name"]} ({updated_item_type["name"]})')
    )])
    db_client.update_skins_profit_by_weapon((
        updated_item["name"],
        updated_item_type["name"],
        updated_item_type["is_stattrak"],
        updated_item_type['price']
    ))


def update_sticker_price(updated_item, markets_data):
    db_client = DBClient()
    db_client.update_stickers_prices([(
        updated_item['name'].replace('Sticker | ',''),
        updated_item["price"],
        get_item_image_url(updated_item['name']),
        json.dumps(markets_data),
        updated_item['week_low_value'],
        updated_item['week_high_value'],
        updated_item['month_low_value'],
        updated_item['month_high_value'],
        updated_item['all_time_low'],
        updated_item['all_time_high'],
        datetime.datetime.now(),
        updated_item['item_classes'][0], # rare
        updated_item['summary']['Category'], # type
    )], parser='csgoskins')


def get_item_image_url(item_name, image_url = None):
    file_path = 'data/csgo_skins_images.json'  if 'Sticker |' in item_name else 'data/cs2_skins_images.json'

    try:
        with open(file_path, 'r') as file:
            images_urls = json.load(file)

        image_url = images_urls[item_name] if 'Sticker |' in item_name else images_urls[item_name].get('image')

    except Exception as e:
        logging.error(f"Got exception: {e}")

    finally:
        return image_url


def parse_with_price_and_update_profits(items, driver):
    parsed_items = ['ak-47-', 'm4a1-s-', 'm4a4-', 'awp-', 'sticker-']
    try:
        for parsed_item in parsed_items:
            for item in items:
                if parsed_item in item['link']:
                    price_values = {}
                    print(item['link'])
                    if 'sticker-' in item['link']:
                        prices, markets_data = fetch_market_data(driver, item['link'], price_values)
                        updated_item = update_item_with_prices(item, prices, markets_data, item["name"])
                        update_sticker_price(updated_item, markets_data)
                    else:
                        for item_type in item.get('types', []):
                            if 'souvenir' not in item_type['link']:
                                prices, markets_data = fetch_market_data(driver, item_type['link'], price_values)
                                updated_item_type = update_item_with_prices(item_type, prices, markets_data, f'{item["name"]} ({item_type["name"]})')
                                update_weapon_price_in_and_skins(item, updated_item_type, markets_data)
    except Exception as e:
        logging.error(f"Got exception: {e}")


def split_array(array, k=1000):
    return [array[i * k:i * k + k] for i in range(len(array) // k + 1)]


def main():
    try:
        driver = create_driver()
        logging.info(f"Creating driver")

        items_links_without_quality = find_items_global_links(driver)
        weapon_configs = find_items_description(driver,  items_links_without_quality)

        parse_with_price_and_update_profits(weapon_configs, driver)

    except Exception as e:
        logging.error(f"Got exception: {e}")
    finally:
        if driver:
            driver.quit()


if __name__ == '__main__':
    load_dotenv()
    main()
