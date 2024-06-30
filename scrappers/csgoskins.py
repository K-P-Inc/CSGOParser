import json
import logging
import time
from classes import DBClient
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree

items = {
    'ak-47': ['inheritance', #'asiimov', 'ice-coaled', 'slate',
            #   'the-empress', 'nightwish', 'redline', 'legion-of-anubis',
            #   'head-shot', 'bloodsport', 'neon-revolution', 'aquamarine-revenge', 'frontside-misty',
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

qualitys = ['factory-new', 'minimal-wear', ]#'field-tested', 'well-worn', 'battle-scarred']

class Driver(webdriver.Chrome):
    def __init__(self, **kwargs):
        options = webdriver.ChromeOptions()

        # Отключает расширения браузера.
        options.add_argument('--disable-extensions')
        # Отключает использование GPU для ускорения отрисовки страницы. Может быть полезно в виртуальных средах.
        options.add_argument('--disable-gpu')
        # Отключает информационные панели и уведомления.
        options.add_argument('--disable-infobars')
        # Отключает уведомления браузера.
        options.add_argument('--disable-notifications')
        # Запускает браузер в безопасном режиме, отключая некоторые функции безопасности.
        options.add_argument('--no-sandbox')
        # Отключает блокировку всплывающих окон.
        options.add_argument('--disable-popup-blocking')
        # Отключает логирование браузера.
        options.add_argument("--disable-logging")
        # Запускает браузер с максимальным размером окна.
        options.add_argument("--start-maximized")
        # Устанавливает фактор масштабирования устройства, что может быть полезно для управления масштабом.
        options.add_argument("--force-device-scale-factor=0.8")
        # Разрешает выполнение небезопасного контента на страницах (например, HTTP на HTTPS).
        options.add_argument("--allow-running-insecure-content")
        # Отключает веб-безопасность, что может понадобиться для разработки и тестирования.
        options.add_argument("--disable-web-security")
        # Отключает изоляцию сайтов (site isolation) для испытательных целей.
        options.add_argument("--disable-site-isolation-trials")
        # Игнорирует ошибки сертификатов SSL, что может быть полезно для тестирования на локальных серверах.
        options.add_argument("--ignore-certificate-errors")
        # Игнорирует ошибки SSL, если такие ошибки возникают при обращении к сайту.
        options.add_argument('--ignore-ssl-errors')
        # Исключает опцию "enable-logging" при настройке экспериментальных параметров браузера.
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
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

        get_parse_urls(parse_urls)
        logging.info("Get items url")

        for url in parse_urls:
            if driver:
                logging.info(f"Mocking in progress: {url}")
                mock_pages(driver, url, pages_mock)
                url = url.replace(url.split('/')[-1], f"stattrak-{url.split('/')[-1]}")
                mock_pages(driver, url, pages_mock)
        logging.info(f"Mocking finished")

        parsed_items = parse_mock_pages(pages_mock)

        with open('./scrappers/data/csgoskins-mock.json', 'w') as mock_file:
             json.dump(parsed_items, mock_file, indent=4)

        # db_client = DBClient()

    except Exception as e:
        logging.error(f"Got exception: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()
    