import undetected_chromedriver as uc
import re
import threading
import gc
import os
import time
import datetime
import pg8000
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

def run_action_id(skins):
    try:
        driver = None
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

        quality_mas = ['Well-Worn', 'Field-Tested', 'Battle-Scarred', 'Minimal Wear', 'Factory New']
        link = 'https://csgoskins.gg/weapons'

        options = uc.ChromeOptions()
        options.add_argument('--disable-extensions')
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = uc.Chrome(options=options)
        driver.get(f'{link}/{skins[0]}')

        for weapon in skins:
            print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] <Thread {skins}> :: Starting')
            main_window = driver.current_window_handle
            for skins_name in driver.find_elements(By.XPATH, "//*[@class = 'left-4 right-4 text-center absolute overflow-hidden'] //a[contains(@href, 'https://csgoskins.gg/items/')]"):
                skins_link = skins_name.get_attribute('href')
                skins_name_text = skins_name.text
                driver.switch_to.new_window('tab')
                driver.get(skins_link)
                is_avaliable_quality = [skin_got_quality.text.splitlines() for skin_got_quality in driver.find_elements(By.XPATH, "//*[@class = 'version-link'] //*[@class = 'w-2/3 flex-none']")]
                print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] <Thread {weapon}> :: Opened skin page')
                for is_startrack_link in ['', 'stattrak-']:
                    for quality in quality_mas:
                        if [quality] not in is_avaliable_quality and [f'StatTrak {quality}'] in is_avaliable_quality:
                            print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] <Thread {weapon}> :: {quality} skipped')
                            continue
                        quality_link = quality.replace(' ', '-').lower()
                        driver.switch_to.new_window('tab')
                        driver.get(f'{skins_link}/{is_startrack_link}{quality_link}')
                        print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] <Thread {weapon}> :: Started parsing {quality} for {weapon}')
                        markets = driver.find_elements(By.XPATH, "//*[@class = 'bg-gray-800 rounded shadow-md relative flex items-center flex-wrap my-4 '] //*[@class = 'w-1/2 sm:w-1/4 p-4 flex-none']")
                        for market in markets:
                            if 'Steam' in market.text:
                                parent = market.find_element(By.XPATH, '..')
                                steam_price = parent.find_elements(By.XPATH, ".//*[@class = 'w-1/2 sm:w-1/4 p-4 flex-none']")
                                for price in steam_price:
                                    if "$" in price.text:
                                        numeric_string = re.sub(r"[^\d.]", "", price.text)
                                        if "$" in numeric_string:  # Check if string contains "$"
                                            numeric_string = numeric_string.replace("$", "")  # Remove "$"
                                        stats = [each.replace("$", "").replace(',', '') for each in driver.find_elements(By.XPATH, "//*[@class = 'shadow-md bg-gray-800 rounded mt-4']")[-1].text.splitlines()]
                                        cur = conn.cursor()
                                        print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] <Thread {weapon}> :: Parsed {weapon.upper()} | {skins_name_text}, {quality}, {False if is_startrack_link == "" else True}, {float(numeric_string)}')
                                        query = '''
                                            INSERT INTO weapons_prices(
                                                name, quality, is_stattrak, price,
                                                price_week_low, price_week_high,
                                                price_month_low, price_month_high,
                                                price_year_low, price_year_high,
                                                price_all_time_low, price_all_time_high, parsing_time
                                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                            ON CONFLICT (name, quality, is_stattrak) DO UPDATE SET
                                                price = EXCLUDED.price,
                                                price_week_low = EXCLUDED.price_week_low,
                                                price_week_high = EXCLUDED.price_week_high,
                                                price_month_low = EXCLUDED.price_month_low,
                                                price_month_high = EXCLUDED.price_month_high,
                                                price_year_low = EXCLUDED.price_year_low,
                                                price_year_high = EXCLUDED.price_year_high,
                                                price_all_time_low = EXCLUDED.price_all_time_low,
                                                price_all_time_high = EXCLUDED.price_all_time_high,
                                                parsing_time = EXCLUDED.parsing_time
                                        '''
                                        print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] <Thread {weapon}> :: Parsed {weapon.upper()} | {skins_name_text}, {quality}, {False if is_startrack_link == "" else True}, {float(numeric_string)} inserted')
                                        cur.execute(query, (
                                            f'{weapon.upper()} | {skins_name_text}', quality, False if is_startrack_link == '' else True, float(numeric_string),
                                            float(stats[-15]), float(stats[-13]),
                                            float(stats[-11]), float(stats[-9]),
                                            float(stats[-7]), float(stats[-5]),
                                            float(stats[-3]), float(stats[-1]), datetime.datetime.now()
                                        ))
                                        conn.commit()
                        print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] <Thread {weapon}> :: Ended parsing {quality} for {weapon}')
                        driver.close()
                        driver.switch_to.window(driver.window_handles[1])
                driver.close()
                driver.switch_to.window(main_window)
            try:
                conn.close()
            except pg8000.Error as e:
                pass
    except Exception as e:
        print(e)
        if driver:
            driver.close()
        run_action_id(skins)
    finally:
        driver.close()


def parse_skins_prices():
    skins = [
        ['ak-47', 'famas', 'galil-ar', 'm4a1-s'],
        ['m4a4', 'sg-553', 'awp'],
        ['g3sg1', 'scar-20', 'ssg-08'],
        ['cz75-auto', 'desert-eagle', 'dual-berettas', 'five-seven'],
        ['glock-18', 'p2000', 'p250', 'r8-revolver', 'tec-9', 'usp-s'],
        ['mac-10', 'mp5-sd', 'mp7', 'mp9'],
        ['p90', 'pp-bizon', 'ump-45', 'aug'],
        ['mag-7', 'nova', 'sawed-off', 'xm1014', 'm249', 'negev']
    ]

    threads = []
    for items in skins:
        thread = threading.Thread(target=run_action_id, args=(items,))
        threads.append(thread)

    for thread in threads:
        thread.start()
        time.sleep(2)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    gc.collect()

if __name__ == '__main__':
    load_dotenv()
    parse_skins_prices()