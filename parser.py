import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import time
import datetime
import os
import threading
import traceback
import pg8000
import logging
import sys
from re import A
from dotenv import load_dotenv

def run_action(weapon_type_id):
    try:
        database = os.environ.get("POSTGRES_DB")
        user = os.environ.get("POSTGRES_USER")
        password = os.environ.get("POSTGRES_PASSWORD")
        conn = pg8000.connect(
            host="localhost",
            port=8080,
            database=database,
            user=user,
            password=password
        )

        options = uc.ChromeOptions()
        options.add_argument('--disable-extensions')
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument('--headless')
        options.add_argument("--enable-javascript")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')

        driver = uc.Chrome(use_subprocess=True, options=options)

        logging.info(f'Getting connection to database')

        for_replace_front, for_replace_back = 'background-image: url("https://steamcdn-a.akamaihd.net/apps/730/icons/econ/stickers/', '.png");'
        cur = conn.cursor()
        cur.execute('''
            SELECT name, price, quality, is_stattrak, id
            FROM weapons_prices
            WHERE price <= 30 and price >= 3
            ORDER BY name
        ''')
        weapons = cur.fetchall()

        cur.execute(f"SELECT price, name, key FROM stickers")
        stickers = cur.fetchall()
        stickers_dict = {}
        for sticker in stickers:
            key = sticker[2]
            stickers_dict[key] = sticker

        weapons_prices = {}
        for weapon in weapons:
            if weapon_type_id in weapon[0]:
                key = f'{"StatTrak™ " if weapon[3] == True else ""}{weapon[0]} ({weapon[2]})'
                weapons_prices[key] = weapon[1]

        weapons = set([(weapon[0].split(' | ')[0], weapon[0].split(' | ')[1], weapon[2], weapon[4]) for weapon in weapons if weapon[0].split(' | ')[0] == weapon_type_id])
        for weapon_type, weapon_name, weapon_quality, weapon_uuid in weapons:
            link = f'https://market.csgo.com/en/?sort=price&order=asc&search={weapon_type}%20%7C%20{weapon_name}%20&priceMax=1000000&categories=any_stickers&quality={weapon_quality}'
            logging.info(f'Working on {weapon_type} | {weapon_name} ({weapon_quality})')
            driver.get(link)
            actions = ActionChains(driver)
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

            logging.info(f'Parsing on {weapon_type} | {weapon_name} ({weapon_quality}) - {len(item_url)}')
            while len(item_url) != 0 and elements_index != item_url[-1]:
                elements_index = item_url[-1]
                logging.info(f'Found more items {weapon_type} | {weapon_name} ({weapon_quality}) - {len(item_url)}')

                for i in item_url:
                    if len(i.text.splitlines()) <= 2:
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

                    all_stickers = [stickers_dict[key] for key in stickers_keys if key in stickers_dict]

                    if len(all_stickers) == 0:
                        continue

                    sticker_count = {}
                    for sticker in all_stickers:
                        key = sticker[2]
                        if key in sticker_count:
                            sticker_count[key] += 1
                        else:
                            sticker_count[key] = 1

                    num_stickers = len(sticker_count)
                    sticker_patern = 'other'

                    if num_stickers == 1 and max(sticker_count.values()) == 4:
                        sticker_patern = 'full-set'
                        sticker_overprice = all_stickers[0][0] * 0.5
                    elif num_stickers == 2 and max(sticker_count.values()) == 3:
                        sticker_patern = '3-equal'
                        equal_sticker_key = max(sticker_count, key=sticker_count.get)
                        equal_sticker_price = [sticker[0] for sticker in all_stickers if sticker[2] == equal_sticker_key][0]
                        unequal_sticker_price = [sticker[0] for sticker in all_stickers if sticker[2] != equal_sticker_key][0] if min(sticker_count.values()) == 1 else 0
                        sticker_overprice = equal_sticker_price * 0.25 + unequal_sticker_price * 0.1
                    elif num_stickers == 2 and (sorted(sticker_count.values()) == [2, 2] or sorted(sticker_count.values()) == 2):
                        sticker_patern = '2-equal'
                        equal_sticker_keys = [key for key, count in sticker_count.items() if count == 2]
                        equal_sticker_prices = [sticker[0] for sticker in all_stickers if sticker[2] in equal_sticker_keys[0]][0]
                        unequal_sticker_prices = [sticker[0] for sticker in all_stickers if sticker[2] not in equal_sticker_keys[0]] if min(sticker_count.values()) == 2 else [0]
                        sticker_overprice = equal_sticker_prices * 0.15 + sum(unequal_sticker_prices) * 0.15
                    elif num_stickers == 3 and max(sticker_count.values()) == 2:
                        sticker_patern = '2-equal'
                        equal_sticker_keys = [key for key, count in sticker_count.items() if count == 2]
                        equal_sticker_prices = [sticker[0] for sticker in all_stickers if sticker[2] in equal_sticker_keys[0]][0]
                        unequal_sticker_prices = [sticker[0] for sticker in all_stickers if sticker[2] not in equal_sticker_keys[0]] if min(sticker_count.values()) == 2 else [0]
                        sticker_overprice = equal_sticker_prices * 0.15 + sum(unequal_sticker_prices) * 0.1
                    else:
                        sticker_patern = 'other'
                        sticker_overprice = sum([sticker[0] for sticker in all_stickers]) * 0.1

                    sticker_sum = sum([sticker[0] for sticker in all_stickers])
                    stickers_names_string = ', '.join([sticker[1] for sticker in all_stickers])

                    if ((((sticker_overprice + actually_price) - (float(i.text.split()[1]))) *100)/(float(i.text.split()[1]))) > 10:
                        if i.get_attribute('href') not in skins_data and sticker_sum > 10:
                            before = time.perf_counter()
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
                                i.get_attribute('href'),
                                sticker_sum, float(i.text.split()[1]),
                                ((((sticker_overprice + actually_price) - (float(i.text.split()[1]))) *100)/(float(i.text.split()[1]))),
                                weapon_uuid, sticker_patern, num_stickers, len(all_stickers)
                            ))
                            conn.commit()
                            skins_data.append(i.get_attribute('href'))
                            logging.info(
                                f"{i.get_attribute('href')}\n{key_price}: {float(i.text.split()[1]):.2f} $\n"
                                f'Steam item price: {actually_price}\n'
                                f'Stickers overprice: {sticker_overprice}\n'
                                f'{stickers_names_string}\n'
                                f'Sum of stickers: {sticker_sum:.2f} $\n'
                                f"Процент потенциальной выручки - {((((sticker_overprice + actually_price) - (float(i.text.split()[1]))) *100)/(float(i.text.split()[1]))):.2f} %"
                            )

                actions.move_to_element(item_url[-1]).perform()
                time.sleep(2)
                item_url = driver.find_elements(By.XPATH, "//a[contains(@href, '/en/')]")[2:]

            logging.info(f'Parsed {weapon_type} | {weapon_name} ({weapon_quality})')
        try:
            conn.close()
        except pg8000.Error as e:
            pass
    except Exception as ex:
        traceback.print_exc()
        run_action(weapon_type_id)
    finally:
        try:
            conn.close()
        except pg8000.Error as e:
            pass
        driver.close()
        driver.quit()


handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)-7s] %(threadName)-22s :: %(message)s'))
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

weapon_types = ['AWP', 'M4A4', 'M4A1-S', 'AK-47', 'DESERT-EAGLES', 'USP-S', 'GLOCK-18', 'P250']
load_dotenv()
threads = []
for i in weapon_types:
    thread = threading.Thread(target=run_action, name=f'<Thread {i}>', args=(i,))
    threads.append(thread)

for thread in threads:
    thread.start()
    time.sleep(1)

for thread in threads:
    thread.join()
