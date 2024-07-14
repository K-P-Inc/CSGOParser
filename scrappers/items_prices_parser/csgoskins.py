import json
import logging
import datetime
import hydra
import requests
import time
from omegaconf import DictConfig
from dotenv import load_dotenv
from pathlib import Path
from utils import repo_path
from utils.data import load_data_json
from classes import DBClient, SeleniumDriver
from urllib.parse import urlparse, quote
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


def find_items_for_parsing_without_quality(driver, url, page):
    logging.info(f"Parsing page: {page}")
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

    logging.info('Getting items_links_without_quality')
    items_links_without_quality = load_data_json('items_links_without_quality.json')

    if items_links_without_quality:
        logging.info('Return items_links_without_quality links from config')
        return items_links_without_quality

    pages = 212
    for page in range(1, pages + 1):
        logging.info('Parse all items links to config')
        links = find_items_for_parsing_without_quality(driver, 'https://csgoskins.gg/?order=lowest_price', page)

        for link in links:
            items_links_without_quality.append(link)

    with open(file_path, "w") as file:
        json.dump(items_links_without_quality, file, indent=4)

    logging.info('Return parsed items_links_without_quality links')
    return items_links_without_quality


def parse_global_weapon_information(driver, url):
    logging.info(f"Parse item {url}")
    time.sleep(1)
    driver.get(url)
    driver.implicitly_wait(0.1)

    logging.info('Geting skin name')
    skin_name = driver.find_element(By.XPATH, '//h1[@class="text-2xl sm:text-3xl font-bold"]').text

    types_config = []
    logging.info('Geting skin types')
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

    logging.info('Geting skin summary')
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

    logging.info('Geting skin class/rarity')
    try:
        item_class_element = driver.find_element(By.XPATH, '//h2[text()="Item Class"]')
        item_class_parent_element = item_class_element.find_element(By.XPATH, './ancestor::div[@class="mt-12"]/following-sibling::div[@class="flex mt-4"]')
        item_class_sub_elements = item_class_parent_element.find_elements(By.XPATH, './div[@class="w-1/2"]')
        item_class_names = [item_class.text for item_class in item_class_sub_elements]
    except NoSuchElementException:
        item_class_names = []

    logging.info('Geting skin collections')
    try:
        collections_element = driver.find_element(By.XPATH, '//h2[text()="Collections"]')
        collections_parent_element = collections_element.find_element(By.XPATH, './ancestor::div[@class="mt-12 mb-6"]/following-sibling::div[@class="flex -mx-4 flex-wrap"]')
        collections_sub_elements = collections_parent_element.find_elements(By.XPATH, './div[@class="w-1/2 sm:w-1/3 md:w-1/4 lg:w-1/3 p-4"]')
        collections_names = [collection_element.text for collection_element in collections_sub_elements]
    except NoSuchElementException:
        collections_names = []

    logging.info('Geting skin containers')
    try:
        containers_element = driver.find_element(By.XPATH, '//h2[text()="Containers"]')
        containers_parent_element = containers_element.find_element(By.XPATH, './ancestor::div[@class="mt-12 mb-6"]/following-sibling::div[@class="flex -mx-4 flex-wrap"]')
        containers_sub_elements = containers_parent_element.find_elements(By.XPATH, './div[@class="w-1/2 sm:w-1/3 md:w-1/4 lg:w-1/3 p-4"]')
        containers_names = [container_element.text for container_element in containers_sub_elements]
    except NoSuchElementException:
        containers_names = []

    logging.info('Geting skin colors')
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
    logging.info('Parse items descriptions')
    global_weapon_configs = []
    file_path = "data/global_weapon_configs.json"

    logging.info('Getting global_weapon_configs')
    global_weapon_configs = load_data_json('global_weapon_configs.json')

    if global_weapon_configs:
        return global_weapon_configs

    for url in items_list:
        global_weapon_configs.append(parse_global_weapon_information(driver, url))

    with open(file_path, "w") as file:
        json.dump(global_weapon_configs, file, indent=4)

    return global_weapon_configs


def get_price_values(driver, price_values):
    logging.info("Get price values")
    try:
        for period in periods:
            for stat in statistics:
                value = driver.find_element(By.XPATH, price_statistics_xpath(f'{period} {stat}')).text.replace('$','')
                price_values[f'{period} {stat}'] = float(value) if ',' not in value else float(value.replace(',',''))
    except Exception as e:
        logging.error(f"Got exception: {e}")
    finally:
        return price_values


def fetch_market_data(driver, item_link, price_values):
    logging.info("Getting market active prices and offers")
    time.sleep(1)
    driver.get(item_link)
    prices = get_price_values(driver, price_values)
    markets_data = {market: get_market_prices(driver, market) for market in market_names}

    return prices, markets_data


def try_to_get_price_from_steam_api(market_hash_name):
    logging.info(f"Trying to get price for {market_hash_name} from Steam API")
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
    logging.info("Get stable price for item")
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
    logging.info(f'{updated_item["name"]}: Update weapon price in db')
    DBClient().update_weapon_prices([(
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
        get_item_image_url(f'{updated_item["name"]} ({updated_item_type["name"]})'),
        updated_item['item_classes'][0] # rare
    )])
    # DBClient().update_skins_profit_by_weapon((
    #     updated_item["name"],
    #     updated_item_type["name"],
    #     updated_item_type["is_stattrak"],
    #     updated_item_type['price']
    # ))


def update_sticker_price(updated_item, markets_data):
    logging.info("Update sticker price in db")
    DBClient().update_stickers_prices([(
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
        updated_item['summary']['Film'], # type
        updated_item['summary']['Update'] # collection
    )], parser='csgoskins')
    # DBClient().update_skins_profit_by_stickers((
    #     updated_item["name"],
    #     updated_item['price']
    # ))


def get_item_image_url(item_name, image_url = None):
    logging.info(f"{item_name}: Getting image url for")
    file = load_data_json('csgo_skins_images.json') if 'Sticker |' in item_name else load_data_json('cs2_skins_images.json')

    return file[item_name] if 'Sticker |' in item_name else file[item_name].get('image')


def parse_with_price_and_update_profits(items, driver):
    parsed_items = ['ak-47-', 'm4a1-s-', 'm4a4-', 'awp-', 'sticker-']
    try:
        for parsed_item in parsed_items:
            for item in items:
                if parsed_item in item['link']:
                    price_values = {}
                    logging.info(f"Parse item: {item['link']}")
                    if 'sticker-' in item['link']:
                        prices, markets_data = fetch_market_data(driver, item['link'], price_values)
                        updated_item = update_item_with_prices(item, prices, markets_data, item["name"])
                        logging.info(f'{updated_item}')
                        update_sticker_price(updated_item, markets_data)
                    else:
                        for item_type in item.get('types', []):
                            if 'souvenir' not in item_type['link']:
                                prices, markets_data = fetch_market_data(driver, item_type['link'], price_values)
                                updated_item_type = update_item_with_prices(item_type, prices, markets_data, f'{item["name"]} ({item_type["name"]})')
                                logging.info(f'{item}')
                                update_weapon_price_in_and_skins(item, updated_item_type, markets_data)
    except Exception as e:
        logging.error(f"Got exception: {e}")


def split_array(array, k=1000):
    return [array[i * k:i * k + k] for i in range(len(array) // k + 1)]


@hydra.main(config_path=str((Path(repo_path()) / 'conf').resolve()), config_name='items_prices_parser')
def main(cfg: DictConfig):
    try:
        driver_class = SeleniumDriver()
        driver = driver_class.driver
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
