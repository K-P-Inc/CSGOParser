import json
import logging
import os
import time
from urllib.parse import urlparse
from classes import DBClient, SeleniumDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from lxml import etree
from utils import repo_path

items = {
    'ak-47': ['inheritance', 'asiimov', 'ice-coaled', 'slate',
              'the-empress', 'nightwish', 'redline', 'legion-of-anubis',
              'head-shot', 'bloodsport', 'neon-revolution', 'aquamarine-revenge', 'frontside-misty',
            #   'phantom-disruptor', 'point-disarray', 'elite-build', 'vulcan', 'case-hardened', 'leet-museo',
            #   'fuel-injector', 'cartel', 'emerald-pinstripe', 'blue-laminate', 'safety-net', 'fire-serpent',
            #   'orbit-mk01', 'uncharted', 'wasteland-rebel', 'rat-rod', 'jaguar', 'steel-delta', 'green-laminate',
            #   'baroque-purple', 'x-ray', 'panthera-onca', 'red-laminate', 'black-laminate', 'safari-mesh', 'jet-set',
            #   'predator', 'jungle-spray', 'first-class', 'gold-arabesque', 'wild-lotus', 'hydroponic',
    ],
    # 'm4a4': ['temukau', #'neo-noir', 'the-emperor', 'desolate-space', 'tooth-fairy', 'in-living-color', 'dragon-king',
    #         #  'spider-lily', 'cyber-security', 'buzz-kill', 'asiimov', 'etch-lord', 'evil-daimyo', 'eye-of-horus', 'royal-paladin',
    #         #  'bullet-rain', 'magnesium', 'hellfire', 'the-coalition', 'converter', 'the-battlestar', 'griffin', 'desert-strike',
    #         #  'dark-blossom', 'x-ray', 'global-offensive', 'poly-mag', 'urban-ddpat', 'daybreak', 'tornado', 'zirka', 'radiation-hazard',
    #         #  'mainframe', 'desert-storm', 'red-ddpat', 'faded-zebra', 'jungle-tiger', 'modern-hunter', 'poseidon', 'howl'
    # ],
    # 'm4a1-s': ['black-lotus', 'printstream', 'player-two', 'decimator', 'nightmare', 'hyper-beast', 'cyrex', 'golden-coil', 'chanticos-fire',
    #         #    'leaded-glass', 'mecha-industries', 'night-terror', 'emphorosaur-s', 'atomic-alloy', 'basilisk', 'dark-water', 'control-panel',
    #         #    'blue-phosphor', 'bright-water', 'guardian', 'nitro', 'mud-spec', 'hot-rod', 'varicamo', 'moss-quartz', 'welcome-to-the-jungle',
    #         #    'flashback', 'blood-tiger', 'briefing', 'icarus-fell', 'fizzy-pop', 'master-piece', 'boreal-forest', 'imminent-danger', 'knight'
    # ],
    # 'awp': ['chrome-cannon', 'neo-noir', 'atheris', 'chromatic-aberration', 'asiimov', 'wildfire', 'duality', 'hyper-beast', 'fever-dream', 'redline',
    #         # 'mortis', 'containment-breach', 'graphite', 'sun-in-leo', 'exoskeleton', 'black-nile', 'elite-build', 'paw', 'worm-god', 'electric-hive',
    #         # 'man-o-war', 'boom', 'corticera', 'phobos', 'capillary', 'oni-taiji', 'acheron', 'pop-awp', 'pink-ddpat', 'silk-tiger', 'pit-viper',
    #         # 'snake-camo', 'safari-mesh', 'desert-hydra', 'fade', 'gungnir', 'the-prince', 'medusa', 'dragon-lore', 'lightning-strike'
    # ],
}

qualitys = ['factory-new', 'minimal-wear', 'field-tested', 'well-worn', 'battle-scarred']

class Driver(webdriver.Chrome):
    def __init__(self, **kwargs):
        options = webdriver.ChromeOptions()

        # Отключает расширения браузера.
        options.add_argument('--disable-extensions')
        # Отключает использование GPU для ускорения отрисовки страницы. Может быть полезно в виртуальных средах.
        options.add_argument('--disable-gpu')
        # Отключает информационные панели и уведомления.
        # options.add_argument('--disable-infobars')
        # Отключает уведомления браузера.
        # options.add_argument('--disable-notifications')
        # # Запускает браузер в безопасном режиме, отключая некоторые функции безопасности.
        options.add_argument('--no-sandbox')
        # Отключает блокировку всплывающих окон.
        # options.add_argument('--disable-popup-blocking')
        # # Отключает логирование браузера.
        # options.add_argument("--disable-logging")
        # # Запускает браузер с максимальным размером окна.
        # options.add_argument("--start-maximized")
        # # Устанавливает фактор масштабирования устройства, что может быть полезно для управления масштабом.
        # options.add_argument("--force-device-scale-factor=0.8")
        # # Разрешает выполнение небезопасного контента на страницах (например, HTTP на HTTPS).
        # options.add_argument("--allow-running-insecure-content")
        # # Отключает веб-безопасность, что может понадобиться для разработки и тестирования.
        # options.add_argument("--disable-web-security")
        # # Отключает изоляцию сайтов (site isolation) для испытательных целей.
        # options.add_argument("--disable-site-isolation-trials")
        # # Игнорирует ошибки сертификатов SSL, что может быть полезно для тестирования на локальных серверах.
        # options.add_argument("--ignore-certificate-errors")
        # # Игнорирует ошибки SSL, если такие ошибки возникают при обращении к сайту.
        # options.add_argument('--ignore-ssl-errors')
        # # Исключает опцию "enable-logging" при настройке экспериментальных параметров браузера.
        # options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # options.add_argument('--headless=new')
        super().__init__(options=options, **kwargs)


def create_driver():
    try:
        driver = Driver()
        driver.implicitly_wait(10)
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
    time.sleep(1)
    driver.get(url)
    driver.implicitly_wait(1)

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


def get_parse_urls(parse_urls):
    for category, names in items.items():
        for name in names:
            for quality in qualitys:
                url = f"https://csgoskins.gg/items/{category}-{name}/{quality}"
                parse_urls.append(url)


def mock_pages(driver, url, pages_mock):
    try:
        driver.get(url)
        pages_mock.append(driver.page_source)
        time.sleep(0.5)
    except Exception as e:
        print(f"Failed to parse: {e}")


def write_data(parsed_items):
    with open(os.path.join(repo_path(), 'data', 'csgoskins-mock.json'), 'w') as mock_file:
        json.dump(parsed_items, mock_file, indent=4)


def price_statistics_xpath(period):
    return f"//*[@class = 'order-[24]']//*[@class = 'flex px-4 py-2']//*[contains(text(), '{period}')]//../*[2]"


def parse_mock_pages(pages_mock):
    parsed_items = []
    for page_html in pages_mock:
        soup = BeautifulSoup(page_html, 'html.parser')
        dom = etree.HTML(str(soup))

        spans = soup.select('.w-full > .font-bold.text-xl')

        item = soup.find('meta', {'property': 'og:url'}).get('content').replace('https://csgoskins.gg/items/', '').split('/')

        periods = ['7 Day', '30 Day']
        statistics = ['Low', 'High']

        price_values = {}

        for period in periods:
            for stat in statistics:
                elements = dom.xpath(price_statistics_xpath(f'{period} {stat}'))
                value = elements[0].text.strip() if elements else None
                price_values[f'{period} {stat}'] = value

        week_low_value = price_values.get('7 Day Low')
        week_high_value = price_values.get('7 Day High')
        month_low_value = price_values.get('30 Day Low')
        month_high_value = price_values.get('30 Day High')

        weapon_type = item[0].split('-')[0] if len(item[0].split('-')) == 2 else "-".join(item[0].split('-')[:2])
        name = item[0].replace(f'{weapon_type}-', '')
        quality = item[1].replace('stattrak-', '') if 'stattrak' in item else item[1]

        for span in spans:
            price = span.get_text()
            if "$" in price:
                prev_img = span.find_previous('img', class_='inline-block h-5 w-5 mr-2')
                active_offers = span.find_previous('div', class_='w-1/4 p-4 flex-none hidden sm:block').find('span', class_='').get_text().strip()
                if prev_img and 'alt' in prev_img.attrs:
                    alt = prev_img['alt']
                    if 'stattrak' in item[1]:
                        quality = item[1].replace('stattrak-', '')
                        stattrak = True
                    else:
                        stattrak = False

                    parsed_item = {
                        "type": weapon_type,
                        "name": name,
                        'stattrak': stattrak,
                        "quality": quality,
                        "market": alt,
                        "price": price,
                        "active_offers": active_offers,
                        # Значения по периоду, это за все магазины, а не за конкретный. Подумать бы как их лучше выводить
                        'week_low': week_low_value,
                        "week_high": week_high_value,
                        "month_low": month_low_value,
                        "month_high": month_high_value,
                    }
                    parsed_items.append(parsed_item)

    return parsed_items


# @hydra.main(config_path=str((Path(repo_path()) / 'conf').resolve()), config_name='items_prices_parser')
# def main(cfg: DictConfig):
def main():
    pages_mock, parse_urls = [], []
    try:
        driver = create_driver()
        logging.info(f"Creating driver")

        items_links_without_quality = find_items_global_links(driver)
        weapon_configs = find_items_description(driver,  items_links_without_quality)

        print(json.dumps(weapon_configs, indent=4))

        return

        logging.info("Get items url")

        for url in parse_urls:
            if driver:
                logging.info(f"Mocking in progress: {url}")
                mock_pages(driver, url, pages_mock)
                url = url.replace(url.split('/')[-1], f"stattrak-{url.split('/')[-1]}")
                mock_pages(driver, url, pages_mock)
        logging.info(f"Mocking finished")

        parsed_items = parse_mock_pages(pages_mock)

        write_data(parsed_items)

        # db_client = DBClient()

    except Exception as e:
        logging.error(f"Got exception: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()
