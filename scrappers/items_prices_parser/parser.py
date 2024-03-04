import requests
import json
import hydra
import datetime
import logging
import os
from omegaconf import DictConfig
from pathlib import Path
from dotenv import load_dotenv
from classes import DBClient
from utils import repo_path

def load_stickers_ids():
    with open(os.path.join(repo_path(), 'data', 'stickers_ids.json'), 'r') as f:
        return json.loads(f.read())

def load_stickers_content():
    with open(os.path.join(repo_path(), 'data', 'stickers_content.json'), 'r') as f:
        return json.loads(f.read())

def parse_response(result_mapping):
    sticker_contents = load_stickers_content()
    stickers_ids = load_stickers_ids()
    weaponts_to_insert, stickers_to_insert = [], []
    for key, item in result_mapping['items_list'].items():
        # logging.debug("Got item from API", key, item)
        if 'type' in item and 'gun_type' in item and 'price' in item:
            if item['type'] == 'Weapon' and 'Souvenir' not in item['name']:
                price = 0
                for qual in ['24_hours', '7_days', '30_days', 'all_time']:
                    if qual in item["price"]:
                        price = item["price"][qual]["average"]
                        break
                name = item["name"].replace("StatTrak™ ", "").replace(f' ({item["exterior"]})', "")
                weaponts_to_insert.append((
                    name, str(item["exterior"]), 'stattrak' in item, price,
                    item["price"]["7_days"]['lowest_price'] if "7_days" in item["price"] else 0,
                    item["price"]["7_days"]['highest_price'] if "7_days" in item["price"] else 0,
                    item["price"]["30_days"]['lowest_price'] if "30_days" in item["price"] else 0,
                    item["price"]["30_days"]['highest_price'] if "30_days" in item["price"] else 0,
                    item["price"]["all_time"]['lowest_price'] if "all_time" in item["price"] else 0,
                    item["price"]["all_time"]['highest_price'] if "all_time" in item["price"] else 0,
                    datetime.datetime.now(),
                    item["icon_url"]
                ))

        elif "sticker" in item and "price" in item:
            key_sticker = None
            name = item['name'].replace("Sticker | ", "")
            for key, value in sticker_contents.items():
                if 'name' in value and value['name'] == name:
                    key_sticker = key
                    break

            price = 0
            for qual in ['24_hours', '7_days', '30_days', 'all_time']:
                if qual in item["price"]:
                    price = item["price"][qual]["average"]
                    break

            stickers_to_insert.append((
                stickers_ids[item['name']] if item['name'] in stickers_ids else '',
                name,
                key_sticker,
                price,
                "", item["rarity"], "",
                item["icon_url"]
            ))

    return  weaponts_to_insert, stickers_to_insert

def invoke_api():
    return requests.get('http://csgobackpack.net/api/GetItemsList/v2/').json()

def split_array(array, k=1000):
    return [array[i * k:i * k + k] for i in range(len(array) // k + 1)]

@hydra.main(config_path=str((Path(repo_path()) / 'conf').resolve()), config_name='items_prices_parser')
def main(cfg: DictConfig):
    try:
        response_api = invoke_api()
        logging.info("Got results from API")

        weaponts_to_insert, stickers_to_insert = parse_response(response_api)
        logging.info("Response parsed")

        db_client = DBClient()
        for weapons in split_array(weaponts_to_insert):
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