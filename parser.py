from re import A
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import time
import datetime
import threading
import traceback
import pg8000


def run_action(quality, type_con):
    options = webdriver.ChromeOptions()

    options.add_argument('--disable-extensions')
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol
        '''
    })

    print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] <Thread {quality}> :: Getting connection to database')
    conn = pg8000.connect(
        host="localhost",
        port=54320,
        database="postgres",
        user="postgres",
        password="my_password"
    )
    for_replace_front, for_replace_back  = 'background-image: url("https://steamcdn-a.akamaihd.net/apps/730/icons/econ/stickers/', '.png");'
    cur = conn.cursor()
    cur.execute('''
        SELECT name, price, uuid
        FROM weapon_prices
        WHERE is_stattrak = %s and quality = %s
        ORDER BY name
    ''', (type_con != 'Normal', quality,))
    weapons = cur.fetchall()
    weapon_types = ['AWP', 'AK-47', 'GALIL-AR', 'M4A4', 'M4A1-S', 'FAMAS', 'SSG-08', 'SG-553']
    weapons = [(weapon[0].split(' | ')[0], weapon[0].split(' | ')[1], weapon[1], weapon[2]) for weapon in weapons if weapon[0].split(' | ')[0] in weapon_types]
    try:
        for weapon_type, weapon_name, actually_price, weapon_uuid in weapons:
            link = f'https://market.csgo.com/ru/?sort=price&order=asc&search={weapon_type}%20%7C%20{weapon_name}%20&quality={quality}&priceMax=1000000&categories=any_stickers&categories={type_con}'
            driver.get(link)
            actions = ActionChains(driver)
            driver.implicitly_wait(20)
            skins_data = []
            while True:
                try:
                    driver.implicitly_wait(3)
                    driver.find_element(By.XPATH, "//*[text() = 'Ничего не найдено']")
                    break
                except NoSuchElementException:
                    pass
                driver.implicitly_wait(3)
                item_url = driver.find_elements(By.XPATH, "//a[contains(@href, '/ru/Rifle')]")
                for i in item_url:
                    sticker_data = i.find_elements(By.XPATH, './/*[starts-with(@class, "stickers")]//*[starts-with(@class, "sticker ")]')
                    sticker_selenium = [b.find_element(By.XPATH, './/*[starts-with(@class, "sticker-img")]').get_attribute('style') for b in sticker_data[0:(len(sticker_data)//2)]]
                    stickers_keys = [sticker.replace(for_replace_front, '').replace(for_replace_back, '').split('.')[0] for sticker in sticker_selenium]
                    stickers_dict = {}
                    cur = conn.cursor()
                    placeholders = ', '.join(['%s'] * len(stickers_keys))

                    if len(stickers_keys) == 0:
                        continue

                    cur.execute(f"SELECT price, name, key FROM stickers WHERE key IN ({placeholders})", tuple(stickers_keys))
                    stickers = cur.fetchall()
                    if len(stickers) == 0:
                        continue

                    for sticker in stickers:
                        key = sticker[2]
                        stickers_dict[key] = sticker

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
                        sticker_overprice = stickers[0][0] * 0.5
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

                    if ((((sticker_overprice + actually_price) - (float(i.text.split()[1]))) *100)/(float(i.text.split()[1]))) > 0:
                        if i.get_attribute('href') not in skins_data and sticker_sum > 10:
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
                            print(f"\n{i.get_attribute('href')}\n{' '.join(i.text.split()[4:])}: {float(i.text.split()[1]):.2f} $")
                            print(f"{stickers_names_string}")
                            print(f"Sum of stickers: {sticker_sum:.2f} $ ")
                            print(f"Процент потенциальной выручки - {((((sticker_overprice + actually_price) - (float(i.text.split()[1]))) *100)/(float(i.text.split()[1]))):.2f} %")

                if len(item_url) == 0:
                    break

                element = item_url[-1]
                actions.move_to_element(element).perform()
                if driver.find_elements(By.XPATH, "//a[contains(@href, '/ru/Rifle')]")[-1] == element:
                    break
        try:
            conn.close()
        except pg8000.Error as e:
            pass
            time.sleep(15)
    except Exception as ex:
        traceback.print_exc()
        print(f'Error - {ex}')
    finally:
        driver.close()
        driver.quit()

rarity = ['Well-Worn', 'Field-Tested', 'Battle-Scarred', 'Minimal Wear', 'Factory New']
threads = []
for i in rarity:
    for quality in ['Normal', 'StatTrak™']:
        thread = threading.Thread(target=run_action, args=(i,quality,))
        threads.append(thread)

# Start the threads
for thread in threads:
    thread.start()
    time.sleep(4)

# Wait for all threads to finish
for thread in threads:
    thread.join()