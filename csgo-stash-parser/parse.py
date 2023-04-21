import json
import requests
import logging
import threading
import gc
import re
import time
import pg8000
from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


with open('skins.json', 'r') as j:
    contents = json.loads(j.read())


def run_action_id(id):
    global contents
    stickers = dict()
    conn = pg8000.connect(
            host="localhost",
            port=54320,
            database="postgres",
            user="postgres",
            password="my_password"
    )
    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")
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
                if value['name'] == f'{sticker_name} | {sticker_tournament}':
                    key_sticker = key
                    break
            cur.execute(query, (f'{sticker_name} | {sticker_tournament}', key_sticker, stickers[f'{sticker_name} | {sticker_tournament}'], "tournament", "", ""))
        else:
            if numeric_string != '':
                stickers[sticker_name] = float(numeric_string)
            else:
                stickers[sticker_name] = 2000.0
            for key, value in contents.items():
                if value['name'] == sticker_name:
                    key_sticker = key
                    break
            cur.execute(query, (sticker_name, key_sticker, stickers[sticker_name], "regular", "", ""))

        conn.commit()
    try:
        conn.close()
    except pg8000.Error as e:
        pass


for index in range(16):
    threads = []
    needed_exit = False
    for i in range(1 + index * 8, (index + 1) * 8):
        thread = threading.Thread(target=run_action_id, args=(i,))
        threads.append(thread)

    # Start the threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    gc.collect()
