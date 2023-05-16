import json
import threading
import gc
import os
import re
from tkinter import N
import traceback
import pg8000
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def run_action_id(indexes, contents):
    try:
        driver = None
        stickers = dict()
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

        options.add_argument("--start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--disable-blink-features=AutomationControlled')

        driver = uc.Chrome(options=options)

        for id in indexes:
            url = f"https://csgoskins.gg/categories/sticker?page={id}"
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            sticker_rows = soup.find_all("div", {"class": "w-full sm:w-1/2 md:w-1/2 lg:w-1/3 xl:w-1/3 2xl:w-1/4 p-4 flex-none"})
            print(f'{len(sticker_rows)} stickers parsed {id}')
            for row in sticker_rows:
                # Extract the sticker name
                numeric_string = re.sub(r"[^\d.]", "", row.find("div", {"class": "left-4 right-4 text-center text-lg absolute"}).text.strip())
                if "$" in numeric_string:  # Check if string contains "$"
                    numeric_string = numeric_string.replace("$", "")  # Remove "$"

                key_sticker = ""

                sticker_tournament = row.find("span", {"class": "block text-gray-400 text-sm truncate" }).text
                sticker_name = row.find("span", {"class": "block text-lg leading-7 truncate" }).text
                cur = conn.cursor()
                query = "INSERT INTO stickers(name, key, price, type, rare, collection) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (name) DO UPDATE SET price = EXCLUDED.price"

                if sticker_tournament != 'Sticker':
                    if numeric_string != '':
                        stickers[f'{sticker_name} | {sticker_tournament}'] = float(numeric_string)
                    else:
                        stickers[f'{sticker_name} | {sticker_tournament}'] = 2000.0
                    for key, value in contents.items():
                        if 'name' in value and value['name'] == f'{sticker_name} | {sticker_tournament}':
                            key_sticker = key
                            break
                    cur.execute(query, (f'{sticker_name} | {sticker_tournament}', key_sticker, stickers[f'{sticker_name} | {sticker_tournament}'], "tournament", "", ""))
                else:
                    if numeric_string != '':
                        stickers[sticker_name] = float(numeric_string)
                    else:
                        stickers[sticker_name] = 2000.0
                    for key, value in contents.items():
                        if 'name' in value and value['name'] == sticker_name:
                            key_sticker = key
                            break
                    cur.execute(query, (sticker_name, key_sticker, stickers[sticker_name], "regular", "", ""))

                conn.commit()

    except Exception as e:
        try:
            conn.close()
        except pg8000.Error as e:
            pass
        traceback.print_exc()
        driver.close()
        driver.quit()
        run_action_id(indexes, contents)
    finally:
        try:
            conn.close()
        except pg8000.Error as e:
            pass
        driver.close()
        driver.quit()

def parse_stickers_prices(contents):
    indexes = [range(1 + index * 16, (index + 1) * 16) for index in range(8)]
    threads = []
    for index in indexes:
        thread = threading.Thread(target=run_action_id, args=(index, contents,))
        threads.append(thread)

    # Start the threads
    for thread in threads:
        thread.start()
        time.sleep(1)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    gc.collect()

if __name__ == '__main__':
    load_dotenv()
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'stickers', 'skins.json'), 'r', encoding='utf-8') as f:
        parse_stickers_prices(json.loads(f.read()))
