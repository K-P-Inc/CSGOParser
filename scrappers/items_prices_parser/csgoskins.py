import json
import logging
import os
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


qualitys = ['factory-new', 'minimal-wear', 'field-tested', 'well-worn', 'battle-scarred']

periods = ['7 Day', '30 Day']
statistics = ['Low', 'High']

def alt_xpath(alt):
    return f"//*[contains(@alt, '{alt}')]//..//..//..//.."


def active_offers_xpath(driver, alt):
    try:
        active_offers_xpath = "//*[contains(text(), 'active offers')]//..//..//*[2]"
        return driver.find_element(By.XPATH, f"{alt_xpath(alt)}{active_offers_xpath}").text or None
    except NoSuchElementException as e:
        return None


def price_offers_xpath(driver, alt):
    try:
        price_from = "//*[text() = 'from']//..//..//*[2]"
        return  driver.find_element(By.XPATH, f"{alt_xpath(alt)}{price_from}").text or None
    except NoSuchElementException as e:
        return None


def get_market_prices(driver, alt):
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
            print(link)

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
                    value = driver.find_element(By.XPATH, price_statistics_xpath(f'{period} {stat}')).text
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
        "summary": skin_summary
    }


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

    try:
        driver = create_driver()
        logging.info(f"Creating driver")

        # with open('scrappers/data/items_links_without_quality.json', 'r') as file:
            # items_links_without_quality = json.load(file)

        items_links_without_quality = [
            "https://csgoskins.gg/items/five-seven-forest-night", # Пушка
            "https://csgoskins.gg/items/m9-bayonet-tiger-tooth", # Нож
            "https://csgoskins.gg/items/bloodhound-gloves-bronzed", # Перчатки
            'https://csgoskins.gg/items/dreams-nightmares-case', # Сундук
            "https://csgoskins.gg/items/csgo-case-key", # Ключ
            'https://csgoskins.gg/items/dreams-nightmares-case-key', # Ключ без предложений обмена на рынке
            'https://csgoskins.gg/items/sticker-koi-holo-copenhagen-2024', # Стикер
            "https://csgoskins.gg/items/paris-2023-mirage-souvenir-package", # Сувенирная коробка
            "https://csgoskins.gg/items/anubis-collection-package", # Коллекционная коробка
            "https://csgoskins.gg/items/copenhagen-2024-contenders-sticker-capsule", # Капсула с наклейками
            "https://csgoskins.gg/items/copenhagen-2024-legends-autograph-capsule", # Капсула с автографами
            "https://csgoskins.gg/items/stockholm-2021-legends-patch-pack", # Патч пакет
            "https://csgoskins.gg/items/community-graffiti-box-1", # Граффити коробка
            "https://csgoskins.gg/items/nightmode-music-kit-box", # Музыкальный набор
            "https://csgoskins.gg/items/collectible-pins-capsule-series-1", # Набор пинов
            "https://csgoskins.gg/items/audience-participation-parcel", # Подарки
            "https://csgoskins.gg/items/special-agent-ava-fbi", # Агент
            "https://csgoskins.gg/items/music-kit-knock2-dashstar", # Музыкальный набор
            "https://csgoskins.gg/items/operation-breakout-all-access-pass", # Пропуск на операцию
            "https://csgoskins.gg/items/howl-pin", # Пин
            "https://csgoskins.gg/items/name-tag", # Нейм тег
            "https://csgoskins.gg/items/stattrak-swap-tool", # Статтрек свап тул
            'https://csgoskins.gg/items/sealed-graffiti-recoil-awp', # Граффити
            'https://csgoskins.gg/items/patch-metal-silver-demon' # Патч
            ]

        # items_links_without_quality = find_items_global_links(driver)

        weapon_configs = find_items_description(driver,  items_links_without_quality)

    except Exception as e:
        logging.error(f"Got exception: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()
