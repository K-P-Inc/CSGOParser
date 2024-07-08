import json
import logging
import datetime
import os
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


qualitys = ['factory-new', 'minimal-wear', 'field-tested', 'well-worn', 'battle-scarred']

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
        # # Запускает браузер в безопасном режиме, отключая некоторые функции безопасности.
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
    time.sleep(2)
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
    markets_data = dict()
    time.sleep(1)
    parsed_items = ['sticker', 'ak-47', 'm4a1-s', 'm4a4', 'awp']
    сondition = [i for i in parsed_items if i in url and 'souvenir' not in url]
    if сondition:
        driver.get(url)
        driver.implicitly_wait(0.5)

        skin_name = driver.find_element(By.XPATH, '//h1[@class="text-2xl sm:text-3xl font-bold"]').text

        types_config, links = [], []

        try:
            for element in driver.find_elements(By.XPATH, f'//a[starts-with(@href, "{url}")]'):
                if 'key' not in element.get_attribute('href'):
                    links.append(element.get_attribute('href'))
        finally:
            if len(links) == 0:
                links.append(url)

        try:
            for link in links:
                if link != url:
                    driver.get(link)
                logging.info(f'Parse item: {link}')

                try:
                    type_name = driver.find_element(By.XPATH, "//*[contains(@class, 'hover:bg-gray-700 bg-gray-700')]//div[1]").text
                    if type_name:
                        name = type_name.replace("StatTrak ", "").replace("Souvenir ", "")
                        is_stattrak = type_name.startswith("StatTrak")
                        is_souvenir = type_name.startswith("Souvenir")
                except NoSuchElementException:
                    name, is_stattrak, is_souvenir = None, None, None

                price_values = {}

                for period in periods:
                    for stat in statistics:
                        value = float(driver.find_element(By.XPATH, price_statistics_xpath(f'{period} {stat}')).text.replace('$',''))
                        price_values[f'{period} {stat}'] = value

                markets_data = {
                    "Skinport": get_market_prices(driver, 'Skinport'),
                    # "GamerPay": get_market_prices(driver, 'GamerPay'),
                    # "Lis Skins": get_market_prices(driver, 'Lis Skins'),
                    "CS.MONEY": get_market_prices(driver, 'CS.MONEY'),
                    "SkinBaron": get_market_prices(driver, 'SkinBaron'),
                    # "SkinSwap": get_market_prices(driver, 'SkinSwap'),
                    # "BUFF163": get_market_prices(driver, 'BUFF163'),
                    "BitSkins": get_market_prices(driver, 'BitSkins'),
                    # "WAXPEER": get_market_prices(driver, 'WAXPEER'),
                    # "ShadowPay": get_market_prices(driver, 'ShadowPay'),
                    "Market CSGO": get_market_prices(driver, 'Market CSGO'),
                    "CSFloat": get_market_prices(driver, 'CSFloat'),
                    "HaloSkins": get_market_prices(driver, 'HaloSkins'),
                    # "CS.DEALS": get_market_prices(driver, 'CS.DEALS'),
                    "DMarket": get_market_prices(driver, 'DMarket'),
                    # "Tradeit.gg": get_market_prices(driver, 'Tradeit.gg'),
                    # "Mannco.store": get_market_prices(driver, 'Mannco.store'),
                    "Steam": get_market_prices(driver, 'Steam'),
                    # "BUFF Market": get_market_prices(driver, 'BUFF Market')
                }

                week_low_value = price_values.get('7 Day Low')
                week_high_value = price_values.get('7 Day High')
                month_low_value = price_values.get('30 Day Low')
                month_high_value = price_values.get('30 Day High')
                all_time_low = price_values.get('All Time Low')
                all_time_high = price_values.get('All Time High')

                types_config.append({
                    "link": driver.current_url,
                    "name": name,
                    "is_stattrak": is_stattrak,
                    "is_souvenir": is_souvenir,
                    "weeks_price": {
                        "high": week_high_value,
                        "low": week_low_value 
                    },
                    "monthly_price": {
                        "high": month_high_value,
                        "low": month_low_value
                    },
                    'all_time_price': {
                        "low": all_time_low,
                        "high": all_time_high
                    },
                    "markets_data": markets_data
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
            "summary": skin_summary,
            'icon': icon
        }

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
    
    markets_data = {
        "Skinport": get_market_prices(driver, 'Skinport'),
        "GamerPay": get_market_prices(driver, 'GamerPay'),
        "Lis Skins": get_market_prices(driver, 'Lis Skins'),
        "CS.MONEY": get_market_prices(driver, 'CS.MONEY'),
        "SkinBaron": get_market_prices(driver, 'SkinBaron'),
        "SkinSwap": get_market_prices(driver, 'SkinSwap'),
        "BUFF163": get_market_prices(driver, 'BUFF163'),
        "BitSkins": get_market_prices(driver, 'BitSkins'),
        "WAXPEER": get_market_prices(driver, 'WAXPEER'),
        "ShadowPay": get_market_prices(driver, 'ShadowPay'),
        "Market CSGO": get_market_prices(driver, 'Market CSGO'),
        "CSFloat": get_market_prices(driver, 'CSFloat'),
        "HaloSkins": get_market_prices(driver, 'HaloSkins'),
        "CS.DEALS": get_market_prices(driver, 'CS.DEALS'),
        "DMarket": get_market_prices(driver, 'DMarket'),
        "Tradeit.gg": get_market_prices(driver, 'Tradeit.gg'),
        "Mannco.store": get_market_prices(driver, 'Mannco.store'),
        "Steam": get_market_prices(driver, 'Steam'),
        "BUFF Market": get_market_prices(driver, 'BUFF Market'),
        'SkinBid': get_market_prices(driver, 'SkinBid')
    }
    
    return prices, markets_data

def update_item_with_prices(item, prices, markets_data):
    item['markets'] = markets_data
    item['week_low_value'] = prices['7 Day Low']
    item['week_high_value'] = prices['7 Day High']
    item['month_low_value'] = prices['30 Day Low']
    item['month_high_value'] = prices['30 Day High']
    item['all_time_low'] = prices['All Time Low']
    item['all_time_high'] = prices['All Time High']
    return item

def parse(driver):
    global_config = []
    parsed_items = ['sticker', 'ak-47', 'm4a1-s', 'm4a4', 'awp']
    file_to_read = "scrappers/data/global_weapon_configs.json"
    file_to_write = "scrappers/data/parse_items_with_price.json"

    with open(file_to_read, 'r') as file:
        items = json.load(file)

    # with open(file_to_write, 'r') as file:
        # global_config = json.load(file)

    try:
        for parsed_item in parsed_items:
            for item in items:
                if parsed_item in item['link']:
                    price_values = {}
                    print(item['link'])
                    if 'sticker' in item['link']:
                        prices, markets_data = fetch_market_data(driver, item['link'], price_values)
                        updated_item = update_item_with_prices(item, prices, markets_data)
                        global_config.append(updated_item)
                    else:
                        for item_type in item.get('types', []):
                            if 'souvenir' not in item_type['link']:
                                prices, markets_data = fetch_market_data(driver, item_type['link'], price_values)
                                updated_item_type = update_item_with_prices(item_type, prices, markets_data)
                                global_config.append(updated_item_type)
    finally:
        with open(file_to_write, "w") as file:
            json.dump(global_config, file, indent=4)



def find_items_description(driver, items_list):
    global_weapon_configs = []
    # file_path = "scrappers/data/global_weapon_configs.json"
    file_path = "scrappers/data/parse_items_with_price.json"
    try:
        # if os.path.exists(file_path):
        #     with open(file_path, "r") as file:
        #         global_weapon_configs = json.load(file)

        # if global_weapon_configs:
            # return global_weapon_configs

        for url in items_list:
            global_weapon_configs.append(parse_global_weapon_information(driver, url))

        with open(file_path, "w") as file:
            json.dump(global_weapon_configs, file, indent=4)
    except Exception as e:
        logging.error(f"Got exception: {e}")

    return global_weapon_configs


def main():
    pages_mock, parse_urls = [], []
    weapons_to_insert, stickers_to_insert = [], []

    try:
        driver = create_driver()
        logging.info(f"Creating driver")

        parse(driver)

        # # with open('scrappers/data/items_links_without_quality.json', 'r') as file:
        #     # items_links_without_quality = json.load(file)

        # items_links_without_quality = [
        #     "https://csgoskins.gg/items/ak-47-redline",
        #     "https://csgoskins.gg/items/sticker-kennys-krakow-2017"
        # ]

        # logging.info(f"Get items links")

        # # items_links_without_quality = find_items_global_links(driver)

        # weapon_configs = find_items_description(driver,  items_links_without_quality)

        # with open('scrappers/data/parse_items_with_price.json','r') as file:
        #     weapon_with_prices_file = json.load(file)
        # logging.info(f"Get items data")

        # for item in weapon_with_prices_file:
        #     for items_exterior in range(len(item['types'])):
        #         item_name = item['name']
        #         avarage_prive = (item['types'][items_exterior]['weeks_price']['high'] + item['types'][items_exterior]['weeks_price']['low']) / 2,
        #         week_price_low = item['types'][items_exterior]['weeks_price']['low'],
        #         week_price_high = item['types'][items_exterior]['weeks_price']['high'],
        #         monthly_price_low = item['types'][items_exterior]['monthly_price']['low'],
        #         monthly_price_high = item['types'][items_exterior]['monthly_price']['high'],
        #         all_time_price_low = item['types'][items_exterior]['all_time_price']['low'],
        #         all_time_price_high = item['types'][items_exterior]['all_time_price']['high'],
        #         date = datetime.datetime.now(),
        #         icon = item['icon']

        #         if 'Sticker |' in item['name']:
        #             stickers_to_insert.append((
        #                 item_name,
        #                 avarage_prive,
        #                 week_price_low,
        #                 week_price_high,
        #                 monthly_price_low,
        #                 monthly_price_high,
        #                 all_time_price_low,
        #                 all_time_price_high,
        #                 date,
        #                 icon
        #             ))
        #         else:
        #             weapons_to_insert.append((
        #                 item_name,
        #                 item['types'][items_exterior]['name'],
        #                 item['types'][items_exterior]['is_stattrak'],
        #                 # item['types'][items_exterior]['is_souvenir'],
        #                 avarage_prive,
        #                 # TODO: Add markets prices?
        #                 week_price_low,
        #                 week_price_high,
        #                 monthly_price_low,
        #                 monthly_price_high,
        #                 all_time_price_low,
        #                 all_time_price_high,
        #                 date,
        #                 icon
        #             )

        # print(weapons_to_insert, stickers_to_insert)

        # db_client = DBClient()
        # for weapons in split_array(weapons_to_insert):
        #     logging.info(f"Updating weapons prices for {len(weapons)} items")
        #     db_client.update_weapon_prices(weapons)

    except Exception as e:
        logging.error(f"Got exception: {e}")
    finally:
        if driver:
            driver.quit()


def split_array(array, k=1000):
    return [array[i * k:i * k + k] for i in range(len(array) // k + 1)]


if __name__ == '__main__':
    main()
