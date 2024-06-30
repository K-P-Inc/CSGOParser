import time
# from classes import DBClient, SeleniumWireDriver
from selenium import webdriver
from bs4 import BeautifulSoup

items = {
    'ak-47': ['inheritance', 'asiimov', 'ice-coaled', 'slate',
            #   'the-empress', 'nightwish', 'redline', 'legion-of-anubis',
            #   'head-shot', 'bloodsport', 'neon-revolution', 'aquamarine-revenge', 'frontside-misty',
            #   'phantom-disruptor', 'point-disarray', 'elite-build', 'vulcan', 'case-hardened', 'leet-museo',
            #   'fuel-injector', 'cartel', 'emerald-pinstripe', 'blue-laminate', 'safety-net', 'fire-serpent',
            #   'orbit-mk01', 'uncharted', 'wasteland-rebel', 'rat-rod', 'jaguar', 'steel-delta', 'green-laminate',
            #   'baroque-purple', 'x-ray', 'panthera-onca', 'red-laminate', 'black-laminate', 'safari-mesh', 'jet-set',
            #   'predator', 'jungle-spray', 'first-class', 'gold-arabesque', 'wild-lotus', 'hydroponic',
    ],
    'm4a4': ['temukau', 'neo-noir', 'the-emperor', 'desolate-space', 'tooth-fairy', 'in-living-color', 'dragon-king',
            #  'spider-lily', 'cyber-security', 'buzz-kill', 'asiimov', 'etch-lord', 'evil-daimyo', 'eye-of-horus', 'royal-paladin',
            #  'bullet-rain', 'magnesium', 'hellfire', 'the-coalition', 'converter', 'the-battlestar', 'griffin', 'desert-strike',
            #  'dark-blossom', 'x-ray', 'global-offensive', 'poly-mag', 'urban-ddpat', 'daybreak', 'tornado', 'zirka', 'radiation-hazard',
            #  'mainframe', 'desert-storm', 'red-ddpat', 'faded-zebra', 'jungle-tiger', 'modern-hunter', 'poseidon', 'howl'
    ],
    'm4a1-s': ['black-lotus', 'printstream', 'player-two', 'decimator', 'nightmare', 'hyper-beast', 'cyrex', 'golden-coil', 'chanticos-fire',
            #    'leaded-glass', 'mecha-industries', 'night-terror', 'emphorosaur-s', 'atomic-alloy', 'basilisk', 'dark-water', 'control-panel',
            #    'blue-phosphor', 'bright-water', 'guardian', 'nitro', 'mud-spec', 'hot-rod', 'varicamo', 'moss-quartz', 'welcome-to-the-jungle',
            #    'flashback', 'blood-tiger', 'briefing', 'icarus-fell', 'fizzy-pop', 'master-piece', 'boreal-forest', 'imminent-danger', 'knight'
    ],
    'awp': ['chrome-cannon', 'neo-noir', 'atheris', 'chromatic-aberration', 'asiimov', 'wildfire', 'duality', 'hyper-beast', 'fever-dream', 'redline',
            # 'mortis', 'containment-breach', 'graphite', 'sun-in-leo', 'exoskeleton', 'black-nile', 'elite-build', 'paw', 'worm-god', 'electric-hive',
            # 'man-o-war', 'boom', 'corticera', 'phobos', 'capillary', 'oni-taiji', 'acheron', 'pop-awp', 'pink-ddpat', 'silk-tiger', 'pit-viper',
            # 'snake-camo', 'safari-mesh', 'desert-hydra', 'fade', 'gungnir', 'the-prince', 'medusa', 'dragon-lore', 'lightning-strike'
    ],
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
        time.sleep(1)
    except Exception as e:
        print(f"Failed to parse: {e}")

def parse_mock_pages(pages_mock):
    alt_price_pairs = []
    for page_html in pages_mock:
        soup = BeautifulSoup(page_html, 'html.parser')

        spans = soup.select('.w-full > .font-bold.text-xl')

        item = soup.find('meta', {'property': 'og:url'}).get('content').replace('https://csgoskins.gg/items/', '').split('/')

        for span in spans:
            price = span.get_text()
            if "$" in price:
                prev_img = span.find_previous('img', class_='inline-block h-5 w-5 mr-2')
                if prev_img and 'alt' in prev_img.attrs:
                    alt = prev_img['alt']
                    alt_price_pairs.append((alt, price))

        for alt, price in alt_price_pairs:
            print(f"item: {item[0]}, quality: {item[1]} market: {alt}, min_price: {price}")


if __name__ == '__main__':
    pages_mock = []
    parse_urls = []

    driver = create_driver()
    get_parse_urls(parse_urls)

    try:
        for url in parse_urls:
            if driver:
                # Мокаем обычные
                mock_pages(driver, url, pages_mock)
                url = url.replace(url.split('/')[-1], f"stattrak-{url.split('/')[-1]}")
                # Мокаем статрэки
                mock_pages(driver, url, pages_mock)
    except Exception as e:
        print(f"Failed to parse: {e}")    
    finally:
        driver.quit()

    parse_mock_pages(pages_mock)