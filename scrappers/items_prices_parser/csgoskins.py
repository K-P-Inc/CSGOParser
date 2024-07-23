import json
import logging
import datetime
from fake_useragent import UserAgent
import hydra
import requests
import time
from lxml import html
from omegaconf import DictConfig
from dotenv import load_dotenv
from pathlib import Path
from utils import repo_path
from utils.data import load_data_json
from classes import DBClient, SeleniumDriver, RedisClient
from urllib.parse import urlparse, quote
from selenium.webdriver.common.by import By


class CookieManager(RedisClient):
    def __init__(self):
        super().__init__()
        self.redis_key = "csgo_skins_gg_cookies"
        self.redis_cookies_json = None

    def get_cookies(self):
        if self.redis_cookies_json:
            return self.redis_cookies_json

        if self.exists(self.redis_key):
            logging.info(f"Found cookies in redis for {type}")
            cookies_json = self.get(self.redis_key)
            self.redis_cookies_json = json.loads(cookies_json)
            return self.redis_cookies_json
        else:
            cookies_json = {
                'i18n': 'eu'
            }
            driver_class = SeleniumDriver()
            driver = driver_class.driver
            driver.delete_all_cookies()
            driver.get("https://csgoskins.gg/")

            time.sleep(10)

            # Get all cookies
            logging.info("Getting cookies from csgoskins.gg")
            cookies = driver.get_cookies()

            for cookie in cookies:
                if cookie["name"] not in cookies_json:
                    cookies_json[cookie["name"]] = cookie["value"]

            logging.info("Cookies from csgoskins.gg: {}".format(cookies_json))
            self.set(self.redis_key, json.dumps(cookies_json), ex=3600)

            self.redis_cookies_json = cookies_json
            return self.redis_cookies_json

    def clear_cookies(self):
        self.delete(self.redis_key)
        self.redis_cookies_json = None

qualitys = ['factory-new', 'minimal-wear', 'field-tested', 'well-worn', 'battle-scarred']
market_names = [
    "Skinport", "GamerPay", "Lis Skins", "CS.MONEY", "SkinBaron",
    "SkinSwap", "BUFF163", "BitSkins", "WAXPEER", "ShadowPay",
    "Market CSGO", "CSFloat", "HaloSkins", "CS.DEALS", "DMarket",
    "Tradeit.gg", "Mannco.store", "Steam", "BUFF Market", "SkinBid"
]
periods = ['7 Day', '30 Day', 'All Time']
statistics = ['Low', 'High']
cookies_manager = CookieManager()


def split_array(array, k=1000):
    return [array[i * k:i * k + k] for i in range(len(array) // k + 1)]


def xpath_one(tree, path):
    return tree.xpath(path)[0]


def element_to_text(element):
    return ' '.join([n.strip() for n in element.itertext()]).strip()


def do_request_and_prepare_lxml(url):
    global cookies_manager
    ua = UserAgent()
    user_agent = ua.random

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'User-Agent': user_agent
    }

    page = requests.get(url, headers=headers, cookies=cookies_manager.get_cookies())

    if page.status_code != 200:
        cookies_manager.clear_cookies()

    tree = html.fromstring(page.content)

    return tree


def alt_xpath(alt):
    return f"//*[contains(@alt, '{alt}')]//..//..//..//.."


def active_offers_xpath(tree, alt):
    try:
        active_offers_xpath = "//*[contains(text(), 'active offers')]//..//..//*[2]"
        active_offers_text = element_to_text(xpath_one(tree, f"{alt_xpath(alt)}{active_offers_xpath}"))
        active_offers_price = int(active_offers_text) if 'K' not in active_offers_text else int(float(active_offers_text.replace('K','')) * 1000)
        return active_offers_price or None
    except Exception as e:
        return None


def price_offers_xpath(tree, alt):
    try:
        price_from = "//*[text() = 'from']//..//..//*[2]"
        price_text = element_to_text(xpath_one(tree, f"{alt_xpath(alt)}{price_from}")).replace('$','')
        price_float = float(price_text) if ',' not in price_text else float(price_text.replace(',',''))
        return price_float or None
    except Exception as e:
        return None


def get_market_prices(tree, alt):
    if alt_xpath(alt):
        return {'active_offers': active_offers_xpath(tree, alt), 'price': price_offers_xpath(tree, alt)}


def price_statistics_xpath(period):
    return f"//*[@class = 'order-[24]']//*[@class = 'flex px-4 py-2']//*[contains(text(), '{period}')]//../*[2]"


def find_items_for_parsing_without_quality(url, page):
    logging.info(f"Parsing page: {page}")
    time.sleep(1)
    tree = do_request_and_prepare_lxml(url)
    links = tree.xpath('//a[starts-with(@href, "https://csgoskins.gg/items/")]')

    correct_links = []
    for link in links:
        href = link.get('href')
        parsed_url = urlparse(href)
        path_segments = parsed_url.path.strip('/').split('/')
        if len(path_segments) == 2:
            correct_links.append(href)

    return set(correct_links)


def find_items_global_links():
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
        links = find_items_for_parsing_without_quality('https://csgoskins.gg/?order=lowest_price', page)
        logging.info(links)
        for link in links:
            items_links_without_quality.append(link)

    with open(f"{repo_path()}/{file_path}", "w") as file:
        json.dump(items_links_without_quality, file, indent=4)

    logging.info('Return parsed items_links_without_quality links')
    return items_links_without_quality


def parse_global_weapon_information(url):
    logging.info(f"Parse item {url}")
    time.sleep(1)
    tree = do_request_and_prepare_lxml(url)

    logging.info('Geting skin name')
    skin_name = xpath_one(tree, '//h1[@class="text-2xl sm:text-3xl font-bold"]').text

    logging.info(skin_name)
    types_config = []
    logging.info(f'Geting skin type')
    try:
        for type_link in tree.xpath(f'//a[starts-with(@href, "{url}")]'):
            type_name = element_to_text(xpath_one(type_link, './/div[@class="w-2/3 flex-none"]'))
            types_config.append({
                "link": type_link.get("href"),
                "name": type_name.replace("StatTrak  ", "").replace("Souvenir  ", ""),
                "is_stattrak": type_name.startswith("StatTrak"),
                "is_souvenir": type_name.startswith("Souvenir"),
            })
    except Exception:
        types_config = []

    logging.info('Geting skin summary')
    try:
        summary_element = xpath_one(tree, '//h2[text()="Summary"]')
        summary_parent_element = xpath_one(summary_element, './ancestor::div[@class="mt-12"]/following-sibling::div[@class="shadow-md bg-gray-800 rounded mt-4"]')
        summary_sub_elements = summary_parent_element.xpath('./div[@class="flex px-4 py-2"]')
        skin_summary = {}
        for child in summary_sub_elements:
            key, _, value = element_to_text(child).partition("   ")

            if value == "":
                key, _, value = element_to_text(child).partition("  ")

            skin_summary[key] = value.replace("\"", "")
    except Exception:
        skin_summary = {}

    logging.info('Geting skin class/rarity')
    try:
        item_class_element = xpath_one(tree, '//h2[text()="Item Class"]')
        item_class_parent_element = xpath_one(item_class_element, './ancestor::div[@class="mt-12"]/following-sibling::div[@class="flex mt-4"]')
        item_class_sub_elements = item_class_parent_element.xpath('./div[@class="w-1/2"]')
        item_class_names = [element_to_text(item_class) for item_class in item_class_sub_elements]
    except Exception:
        item_class_names = []

    logging.info('Geting skin collections')
    try:
        collections_element = xpath_one(tree, '//h2[text()="Collections"]')
        collections_parent_element = xpath_one(collections_element, './ancestor::div[@class="mt-12 mb-6"]/following-sibling::div[@class="flex -mx-4 flex-wrap"]')
        collections_sub_elements = collections_parent_element.xpath('./div[@class="w-1/2 sm:w-1/3 md:w-1/4 lg:w-1/3 p-4"]')
        collections_names = [element_to_text(collection_element) for collection_element in collections_sub_elements]
    except Exception:
        collections_names = []

    logging.info('Geting skin containers')
    try:
        containers_element = xpath_one(tree, '//h2[text()="Containers"]')
        containers_parent_element = xpath_one(containers_element, './ancestor::div[@class="mt-12 mb-6"]/following-sibling::div[@class="flex -mx-4 flex-wrap"]')
        containers_sub_elements = containers_parent_element.xpath('./div[@class="w-1/2 sm:w-1/3 md:w-1/4 lg:w-1/3 p-4"]')
        containers_names = [element_to_text(container_element) for container_element in containers_sub_elements]
    except Exception:
        containers_names = []

    logging.info('Geting skin colors')
    try:
        colors_element = xpath_one(tree, '//h2[text()="Colors"]')
        colors_parent_element = xpath_one(colors_element, './ancestor::div[@class="mt-12 mb-6"]/following-sibling::div[@class="flex -mx-4 flex-wrap"]')
        colors_sub_elements = colors_parent_element.xpath('./div[@class="w-full flex p-4"]/a')
        colors_names = [color_element.get('aria-label') for color_element in colors_sub_elements]
    except Exception:
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


def find_items_description(items_list):
    logging.info('Parse items descriptions')
    global_weapon_configs = []
    file_path = "data/global_weapon_configs.json"

    logging.info('Getting global_weapon_configs')
    global_weapon_configs = load_data_json('global_weapon_configs.json')

    if global_weapon_configs:
        return global_weapon_configs

    for url in items_list:
        global_weapon_configs.append(parse_global_weapon_information(url))

    with open(f"{repo_path()}/{file_path}", "w") as file:
        json.dump(global_weapon_configs, file, indent=4)

    return global_weapon_configs


def get_price_values(tree, price_values):
    logging.info("Get price values")
    try:
        for period in periods:
            for stat in statistics:
                value = element_to_text(xpath_one(tree, price_statistics_xpath(f'{period} {stat}'))).replace('$','')
                price_values[f'{period} {stat}'] = float(value) if ',' not in value else float(value.replace(',',''))
    finally:
        return price_values


def fetch_market_data(item_link, price_values):
    logging.info("Getting market active prices and offers")
    time.sleep(1)
    tree = do_request_and_prepare_lxml(item_link)
    prices = get_price_values(tree, price_values)
    markets_data = {market: get_market_prices(tree, market) for market in market_names}

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
    except Exception as e:
        logging.error(e)
        return -1


def update_item_with_prices(item, prices, markets_data):
    logging.info("Get stable price for item")
    price = -1

    for market_name, market_value in markets_data.items():
        if market_name == "Steam" and market_value["price"] != None and market_value["price"] < 100.0:
            price = market_value["price"]
            logging.info(f"Steam price found: {price}")
            break

    if price == -1 and '7 Day low' in prices:
        if prices['7 Day Low'] <= 1300:
            price = prices['7 Day Low'] / 0.7
        else:
            price = prices['7 Day Low']

    if price == -1 and '30 Day Low' in prices:
        if prices['30 Day Low'] <= 1300:
            price = prices['30 Day Low'] / 0.7
        else:
            price = prices['30 Day Low']

    item["price"] = price
    item['markets'] = markets_data
    item['week_low_value'] = prices.get('7 Day Low')
    item['week_high_value'] = prices.get('7 Day High')
    item['month_low_value'] = prices.get('30 Day Low')
    item['month_high_value'] = prices.get('30 Day High')
    item['all_time_low'] = prices.get('All Time Low')
    item['all_time_high'] = prices.get('All Time High')

    return item


def get_item_image_url(item_name, image_url = None):
    logging.info(f"{item_name}: Getting image url for")
    file = load_data_json('csgo_skins_images.json') if 'Sticker |' in item_name else load_data_json('cs2_skins_images.json')

    return file.get(item_name, None) if 'Sticker |' in item_name else file[item_name].get('image', None)


def parse_with_price_and_update_profits(items):
    global cookies_manager
    parsed_items = [
        ('/ak-47-', 'AK-47'),
        ('/m4a1-s-', 'M4A1-S'),
        ('/m4a4-', 'M4A4'),
        ('/awp-', 'AWP'),
        ('/sticker-', 'Sticker')
    ]
    try:
        for parsed_item, name in parsed_items:
            amount_of_parsed_items = 0
            filtered_items = [item for item in items if parsed_item in item['link']]
            items_for_insert = []

            while len(filtered_items) > amount_of_parsed_items:
                try:
                    cookies_manager = CookieManager()
                    for item in filtered_items:
                        if parsed_item in item['link']:
                            price_values = {}
                            logging.info(f"Parse item: {item['link']}")
                            if 'sticker-' in item['link'] and item['name'].startswith('Sticker | '):
                                prices, markets_data = fetch_market_data(item['link'], price_values)
                                updated_item = update_item_with_prices(item, prices, markets_data)
                                image_url = get_item_image_url(updated_item['name']),
                                if updated_item["price"] != -1 and image_url:
                                    items_for_insert.append((
                                        updated_item['name'].replace('Sticker | ',''),
                                        updated_item["price"],
                                        image_url,
                                        json.dumps(markets_data),
                                        updated_item['week_low_value'],
                                        updated_item['week_high_value'],
                                        updated_item['month_low_value'],
                                        updated_item['month_high_value'],
                                        updated_item['all_time_low'],
                                        updated_item['all_time_high'],
                                        datetime.datetime.now(),
                                        updated_item['item_classes'][0],
                                        updated_item['summary']['Film'],
                                        updated_item['summary']['Update']
                                    ))
                                amount_of_parsed_items += 1
                            else:
                                for item_type in item.get('types', []):
                                    if 'souvenir' not in item_type['link']:
                                        prices, markets_data = fetch_market_data(item_type['link'], price_values)
                                        updated_item_type = update_item_with_prices(item_type, prices, markets_data)
                                        image_url = get_item_image_url(f'{item["name"]} ({updated_item_type["name"]})')
                                        if updated_item_type["price"] != -1 and image_url:
                                            items_for_insert.append((
                                                item["name"],
                                                updated_item_type["name"],
                                                updated_item_type["is_stattrak"],
                                                updated_item_type["price"],
                                                image_url,
                                                json.dumps(markets_data),
                                                updated_item_type['week_low_value'],
                                                updated_item_type['week_high_value'],
                                                updated_item_type['month_low_value'],
                                                updated_item_type['month_high_value'],
                                                updated_item_type['all_time_low'],
                                                updated_item_type['all_time_high'],
                                                datetime.datetime.now(),
                                                image_url,
                                                item['item_classes'][0] # rare
                                            ))

                                    amount_of_parsed_items += 1

                except Exception as e:
                    logging.error(f"Failed to parse item {item['link']}: {e}")

            if name == 'Sticker':
                for stickers in split_array(items_for_insert, k=200):
                    logging.info(f"Updating stickers prices for {len(list(set(stickers)))} items")
                    DBClient().update_stickers_prices(list(set(stickers)), parser='csgoskins')

                DBClient().update_skins_profit_by_stickers()
                logging.info(f"Updated stickers profits")
            else:
                for weapons in split_array(items_for_insert, k=200):
                    logging.info(f"Updating weapon prices for {len(list(set(weapons)))} items")
                    DBClient().update_weapon_prices(list(set(weapons)))
                DBClient().update_skins_profit_by_weapon(name)

            items_for_insert.clear()
    except Exception as e:
        logging.error(f"Got exception: {e}")


def split_array(array, k=1000):
    return [array[i * k:i * k + k] for i in range(len(array) // k + 1)]


@hydra.main(config_path=str((Path(repo_path()) / 'conf').resolve()), config_name='items_prices_parser')
def main(cfg: DictConfig):
    try:
        logging.info(f"Creating driver")

        items_links_without_quality = find_items_global_links()
        weapon_configs = find_items_description(items_links_without_quality)

        parse_with_price_and_update_profits(weapon_configs)

    except Exception as e:
        logging.error(f"Got exception: {e}")


if __name__ == '__main__':
    load_dotenv()
    main()
