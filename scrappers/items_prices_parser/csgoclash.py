import requests
import json
import hydra
import datetime
import logging
import os
import html
from omegaconf import DictConfig
from pathlib import Path
from dotenv import load_dotenv
from classes import DBClient, SeleniumDriver
from utils import repo_path
from selenium.webdriver.common.by import By

def load_stickers_ids():
    with open(os.path.join(repo_path(), 'data', 'stickers_ids.json'), 'r') as f:
        return json.loads(f.read())

def load_stickers_content():
    with open(os.path.join(repo_path(), 'data', 'stickers_content.json'), 'r') as f:
        return json.loads(f.read())

def parse_response(result_mapping):
    exteriors = [
        'Factory New',
        'Minimal Wear',
        'Field-Tested',
        'Well-Worn',
        'Battle-Scarred'
    ]
    # Individual weapon type arrays

    # Pistols
    pistols = [
        "Glock-18",
        "P2000",
        "USP-S",
        "P250",
        "Five-SeveN",
        "Desert Eagle",
        "R8 Revolver",
        "CZ75-Auto",
        "Dual Berettas",
        "Tec-9"
    ]

    # Submachine Guns (SMGs)
    smgs = [
        "MAC-10",
        "MP5-SD",
        "MP7",
        "MP9",
        "PP-Bizon",
        "P90",
        "UMP-45"
    ]

    # Rifles
    rifles = [
        "AK-47",
        "M4A4",
        "M4A1-S",
        "AUG",
        "SG 553",
        "FAMAS",
        "Galil AR"
    ]

    # Sniper Rifles
    sniper_rifles = [
        "AWP",
        "SSG 08",
        "G3SG1",
        "SCAR-20"
    ]

    # Shotguns
    shotguns = [
        "Nova",
        "XM1014",
        "MAG-7",
        "Sawed-Off"
    ]

    # Machine Guns
    machine_guns = [
        "M249",
        "Negev"
    ]

    # Combine all arrays into one
    all_weapons = pistols + smgs + rifles + sniper_rifles + shotguns + machine_guns

    sticker_contents = load_stickers_content()
    stickers_ids = load_stickers_ids()
    weapons_to_insert, stickers_to_insert = [], []

    for key, item in result_mapping['items_list'].items():
        if any(item["name"].startswith(weapon) or item["name"].startswith("StatTrak™ " + weapon) for weapon in all_weapons) and "price" in item:
            price = 0
            for qual in ['7_days', '30_days', 'all_time']:
                if qual in item["price"]:
                    price = item["price"][qual]["average"]
                    break
            exterior = next(x for x in exteriors if x in item["name"])
            name = html.unescape(item["name"].replace("StatTrak™ ", "").replace(f' ({exterior})', ""))
            weapons_to_insert.append((
                name, exterior, 'StatTrak™' in item["name"], price,
                item["price"]["7_days"]['lowest_price'] if "7_days" in item["price"] else 0,
                item["price"]["7_days"]['highest_price'] if "7_days" in item["price"] else 0,
                item["price"]["30_days"]['lowest_price'] if "30_days" in item["price"] else 0,
                item["price"]["30_days"]['highest_price'] if "30_days" in item["price"] else 0,
                item["price"]["all_time"]['lowest_price'] if "all_time" in item["price"] else 0,
                item["price"]["all_time"]['highest_price'] if "all_time" in item["price"] else 0,
                datetime.datetime.now(),
                item["icon_url"]
            ))

        elif "Sticker | " in item["name"] and "price" in item:
            key_sticker = None
            name = html.unescape(item['name'].replace("Sticker | ", ""))
            for key, value in sticker_contents.items():
                if 'name' in value and value['name'] == name:
                    key_sticker = key
                    break

            price = 0
            for qual in ['7_days', '30_days', 'all_time']:
                if qual in item["price"]:
                    price = item["price"][qual]["average"]
                    break

            stickers_to_insert.append((
                stickers_ids[item['name']] if item['name'] in stickers_ids else '',
                name,
                key_sticker,
                price,
                "", "", "",
                item["icon_url"]
            ))

    return  weapons_to_insert, stickers_to_insert

def invoke_api():
    driver_class = SeleniumDriver()
    driver = driver_class.driver

    driver.get('https://inventory.clash.gg/api/GetItemsList/v2')
    content = driver.find_element(By.TAG_NAME, 'pre').text

    return json.loads(content)

def split_array(array, k=1000):
    return [array[i * k:i * k + k] for i in range(len(array) // k + 1)]

@hydra.main(config_path=str((Path(repo_path()) / 'conf').resolve()), config_name='items_prices_parser')
def main(cfg: DictConfig):
    try:
        response_api = invoke_api()
        logging.info(f"Got results from API")

        weapons_to_insert, stickers_to_insert = parse_response(response_api)
        logging.info("Response parsed")

        db_client = DBClient()
        for weapons in split_array(weapons_to_insert):
            logging.info(f"Updating weapons prices for {len(weapons)} items")
            db_client.update_weapon_prices(weapons)

        for stickers in split_array(stickers_to_insert):
            logging.info(f"Updating stickers prices for {len(stickers)} items")
            db_client.update_stickers_prices(stickers)

        logging.info("All items were parsed successfully")
    except Exception as e:
        logging.error(f"Got exception: {e}")

if __name__ == '__main__':
    load_dotenv()
    main()