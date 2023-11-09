import time
import os
import threading
import pg8000
import logging
import hydra
from omegaconf import DictConfig
from re import A
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions, Remote

threadLocal = threading.local()

class Driver:
    def __init__(self):
        self.driver = None

        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--enable-javascript")

        # Set Chrome to automatically download files to the specified directory and disable the pdfjs viewer
        options.add_experimental_option(
            "prefs",
                {
                    "download.default_directory": "/home/seluser/Downloads",  # Set download directory.
                    "download.prompt_for_download": False,  # Automatically download files without prompting.
                    "download.directory_upgrade": True,  # Use the specified download directory.
                    "plugins.always_open_pdf_externally": True,  # Automatically open PDFs.
                    "pdfjs.disabled": True  # Disable the internal PDF viewer.
                },
        )

        logging.info(f'Starting undetected chromedriver')
        self.driver = Remote(options=options, command_executor="http://seleniarm-hub:4444/wd/hub")


    def __del__(self):
        if self.driver:
            self.driver.quit()
            logging.info(f'Сlosed undetected chromedriver')


def repo_path():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def run_action(weapon_config, parsed_items=0):
    try:
        logging.info(f'Getting connection to database')
        database = os.environ.get("POSTGRES_DB")
        user = os.environ.get("POSTGRES_USER")
        password = os.environ.get("POSTGRES_PASSWORD")
        conn = pg8000.connect(
            host="db",
            database=database,
            user=user,
            password=password
        )
        logging.info(f'Connected to database')

        driver_class = Driver()
        driver = driver_class.driver
        actions = ActionChains(driver)

        logging.info(f'Undetected chromedriver started')

        for_replace_front, for_replace_back = 'background-image: url("https://steamcdn-a.akamaihd.net/apps/730/icons/econ/stickers/', '.png");'

        cur = conn.cursor()

        stickers_dict = {}
        while len(stickers_dict) == 0:
            logging.info('Getting stickers from database for keys')
            cur.execute('SELECT price, name, key FROM stickers')
            stickers = cur.fetchall()
            for sticker in stickers:
                key = sticker[2]
                stickers_dict[key] = sticker
            logging.info(f'Fetched {len(stickers_dict)} stickers')
            time.sleep(1)

        weapons = []
        while len(weapons) == 0:
            logging.info('Getting skins from database')
            cur.execute('''
                SELECT name, price, quality, is_stattrak, id
                FROM weapons_prices
                WHERE price >= %s and price <= %s
                ORDER BY name
            ''', (weapon_config.min_steam_item_price, weapon_config.max_steam_item_price,))

            weapons = cur.fetchall()
            weapons_prices = {}
            for weapon in weapons:
                if weapon_config.type in weapon[0]:
                    key = f'{"StatTrak™ " if weapon[3] == True else ""}{weapon[0]} ({weapon[2]})'
                    weapons_prices[key] = weapon[1]

            weapons = sorted(list(set([
                (weapon[0].split(' | ')[0], weapon[0].split(' | ')[1], weapon[3], weapon[2], weapon[4])
                for weapon in weapons
                if weapon[0].split(' | ')[0] == weapon_config.type
            ])))

            if len(weapons) != parsed_items:
                weapon = weapon[parsed_items:]
            else:
                logging.info(f'All items parsed, reseting parsed items counter')
                parsed_items = 0

            logging.info(f'Fetched {len(weapons)} skins from database')
            time.sleep(1)

        for weapon_type, weapon_name, weapon_is_stattrak, weapon_quality, weapon_uuid in weapons:
            link = f'https://market.csgo.com/en/?sort=price&order=asc&search={weapon_type}%2r0%7C%20{weapon_name}%20&priceMax=1000000&categories=any_stickers{"&categories=StatTrak™" if weapon_is_stattrak == True else "&categories=Normal"}&quality={weapon_quality}'
            display_name = f'{"StatTrak™ " if weapon_is_stattrak == True else ""}{weapon_type} | {weapon_name} ({weapon_quality})'
            driver.get(link)
            driver.implicitly_wait(20)
            elements_index = None
            skins_data = []
            try:
                driver.implicitly_wait(3)
                driver.find_element(By.XPATH, "//*[text() = 'Nothing found']")
                break
            except NoSuchElementException:
                pass
            item_url = driver.find_elements(By.XPATH, "//a[contains(@href, '/en/')]")[2:]

            if len(item_url) == 0:
                logging.info(f'No weapons found {display_name}')
                continue

            logging.info(f'Parsing weapon {display_name}')
            while len(item_url) != 0 and elements_index != item_url[-1]:
                logging.info(f'Found {len(item_url)} weapons {display_name}')
                elements_index = item_url[-1]
                for index, i in enumerate(item_url):
                    try:
                        if i.is_displayed() and len(i.text.splitlines()) <= 2:
                            continue
                    except WebDriverException:
                        try:
                            i = driver.find_element(By.XPATH, f"//a[contains(@href, '/en/')][{2 + index}]")
                            if index == len(item_url) - 1:
                                elements_index = i
                        except NoSuchElementException:
                            continue

                    key_price = max(i.text.splitlines(), key=len)

                    if key_price not in weapons_prices:
                        continue

                    actually_price = weapons_prices[key_price]
                    sticker_data = i.find_elements(By.XPATH, './/*[starts-with(@class, "stickers")]//*[starts-with(@class, "sticker ")]')
                    sticker_selenium = [b.find_element(By.XPATH, './/*[starts-with(@class, "sticker-img")]').get_attribute('style') for b in sticker_data[0:(len(sticker_data)//2)]]
                    stickers_keys = [sticker.replace(for_replace_front, '').replace(for_replace_back, '').split('.')[0] for sticker in sticker_selenium]

                    if len(stickers_keys) == 0:
                        continue

                    matched_stickers = [stickers_dict[key] for key in stickers_keys if key in stickers_dict]

                    if len(matched_stickers) == 0:
                        continue

                    sticker_count = {}
                    for sticker in matched_stickers:
                        key = sticker[2]
                        if key in sticker_count:
                            sticker_count[key] += 1
                        else:
                            sticker_count[key] = 1

                    num_stickers = len(sticker_count)
                    sticker_patern = 'other'

                    if num_stickers == 1 and max(sticker_count.values()) == 4:
                        sticker_patern = 'full-set'
                        sticker_overprice = matched_stickers[0][0] * 0.5
                    elif num_stickers == 2 and max(sticker_count.values()) == 3:
                        sticker_patern = '3-equal'
                        equal_sticker_key = max(sticker_count, key=sticker_count.get)
                        equal_sticker_price = [sticker[0] for sticker in matched_stickers if sticker[2] == equal_sticker_key][0]
                        unequal_sticker_price = [sticker[0] for sticker in matched_stickers if sticker[2] != equal_sticker_key][0] if min(sticker_count.values()) == 1 else 0
                        sticker_overprice = equal_sticker_price * 0.25 + unequal_sticker_price * 0.1
                    elif num_stickers == 2 and (sorted(sticker_count.values()) == [2, 2] or sorted(sticker_count.values()) == 2):
                        sticker_patern = '2-equal'
                        equal_sticker_keys = [key for key, count in sticker_count.items() if count == 2]
                        equal_sticker_prices = [sticker[0] for sticker in matched_stickers if sticker[2] in equal_sticker_keys[0]][0]
                        unequal_sticker_prices = [sticker[0] for sticker in matched_stickers if sticker[2] not in equal_sticker_keys[0]] if min(sticker_count.values()) == 2 else [0]
                        sticker_overprice = equal_sticker_prices * 0.15 + sum(unequal_sticker_prices) * 0.15
                    elif num_stickers == 3 and max(sticker_count.values()) == 2:
                        sticker_patern = '2-equal'
                        equal_sticker_keys = [key for key, count in sticker_count.items() if count == 2]
                        equal_sticker_prices = [sticker[0] for sticker in matched_stickers if sticker[2] in equal_sticker_keys[0]][0]
                        unequal_sticker_prices = [sticker[0] for sticker in matched_stickers if sticker[2] not in equal_sticker_keys[0]] if min(sticker_count.values()) == 2 else [0]
                        sticker_overprice = equal_sticker_prices * 0.15 + sum(unequal_sticker_prices) * 0.1
                    else:
                        sticker_patern = 'other'
                        sticker_overprice = sum([sticker[0] for sticker in matched_stickers]) * 0.1

                    sticker_sum = sum([sticker[0] for sticker in matched_stickers])
                    stickers_names_string = ', '.join([sticker[1] for sticker in matched_stickers])
                    market_csgo_item_price = float(i.text.split()[1][1:])
                    market_csgo_item_link = i.get_attribute('href')
                    future_profit_percentages = (sticker_overprice + actually_price - market_csgo_item_price) / market_csgo_item_price * 100

                    if future_profit_percentages > 10:
                        if market_csgo_item_link not in skins_data and sticker_sum > weapon_config.profit_threshold:
                            cur = conn.cursor()
                            query = '''
                                INSERT INTO skins(
                                    link, stickers_price, price, profit, skin_id, stickers_patern, amount_of_stickers_distinct, amount_of_stickers
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (link) DO UPDATE SET
                                stickers_price = EXCLUDED.stickers_price,
                                price = EXCLUDED.price,
                                profit = EXCLUDED.profit,
                                skin_id = EXCLUDED.skin_id,
                                stickers_patern = EXCLUDED.stickers_patern,
                                amount_of_stickers_distinct = EXCLUDED.amount_of_stickers_distinct,
                                amount_of_stickers = EXCLUDED.amount_of_stickers
                            '''
                            cur.execute(query, (
                                market_csgo_item_link,
                                sticker_sum, market_csgo_item_price,
                                future_profit_percentages,
                                weapon_uuid, sticker_patern, num_stickers, len(matched_stickers)
                            ))
                            conn.commit()
                            cur.close()
                            skins_data.append(market_csgo_item_link)
                            logging.info(
                                f'Found new item:\n\n'
                                f'Link: {market_csgo_item_link}\n'
                                f'Name - price: {key_price} - {market_csgo_item_price:.2f} $\n'
                                f'Steam item price: {actually_price} $\n'
                                f'Found stickers: {stickers_names_string}\n'
                                f'Total stickers price: {sticker_sum:.2f} $, parsed stickers: {len(matched_stickers)}/{len(stickers_keys)}, stickers pattern: {sticker_patern}\n'
                                f'Stickers overprice: {sticker_overprice} $\n'
                                f'Profit: {future_profit_percentages:.2f} %\n\n'
                            )

                try:
                    actions.move_to_element(driver.find_element(By.XPATH, "//a[contains(@href, '/en/')][last()]")).perform()
                    time.sleep(2)
                    item_url = driver.find_elements(By.XPATH, "//a[contains(@href, '/en/')]")[len(item_url) + 2:]
                except:
                    continue

            logging.info(f'Parsed weapon {display_name}')
            parsed_items += 1
        try:
            conn.close()
        except pg8000.Error:
            pass
    except KeyboardInterrupt:
        logging.info('Closing parsing process (KeyboardInterrupt)')
        return
    except pg8000.Error or WebDriverException as e:
        logging.error(e)
        run_action(weapon_config, parsed_items)
    finally:
        logging.info('End parsing process')

@hydra.main(config_path=f'/app/conf', config_name='market_csgo_parser')
def main(cfg: DictConfig):
    while True:
        weapon_type = os.environ.get("WEAPON_TYPE")
        weapon = next((w for w in cfg.weapons if w.type == weapon_type), None)

        if weapon is not None:
            run_action(weapon)
        else:
            print("Weapon not found.")

        time.sleep(1)



if __name__ == "__main__":
    load_dotenv()
    main()