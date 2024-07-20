import logging
import time
import json
from classes.db import DBClient
from classes.redis import RedisClient

def get_weapons_array_by_type(db_client, redis_client, weapon_config, parsed_items, with_quality=False):
    weapons = []
    weapons_prices = {}

    while len(weapons) == 0:
        logging.debug(f'Getting skins from database, already parsed {parsed_items}')
        redis_key = f"{weapon_config.type}_weapons_prices{'_with_quality' if with_quality else ''}"

        if redis_client.exists(redis_key):
            weapons_prices_str_json = redis_client.get(redis_key)
            weapons_prices = json.loads(weapons_prices_str_json)

        else:
            weapons_db_list = db_client.get_all_weapons(weapon_config.type, weapon_config.min_steam_item_price, weapon_config.max_steam_item_price)
            weapons_prices = {}
            for weapon in weapons_db_list:
                key = f'{"StatTrak™ " if weapon[3] == True else ""}{weapon[0]} ({weapon[2]})'
                weapons_prices[key] = {
                    "uuid": str(weapon[4]),
                    "price": weapon[1],
                    "is_stattrak": weapon[3],
                    "type": weapon_config.type,
                    "name": f"{weapon[0].split(' | ')[1]} ({weapon[2]})" if with_quality else weapon[0].split(' | ')[1]
                }
            if weapons_db_list:
                redis_client.set(redis_key, json.dumps(weapons_prices), ex=60)

        weapons = sorted(list(set([
            (weapon_config.type, value["name"], value["is_stattrak"])
            for _, value in weapons_prices.items()
        ])))

        if len(weapons) > parsed_items:
            weapons = weapons[parsed_items:]
        else:
            logging.debug(f'All items parsed, reseting parsed items counter')
            parsed_items = 0

        logging.debug(f'Fetched {len(weapons)} skins from database')
        time.sleep(1)

    return weapons, weapons_prices

def get_stickers_dict(db_client, redis_client):
    redis_key = "stickers_dict"

    stickers_dict = {}
    while len(stickers_dict) == 0:
        logging.debug('Getting stickers from database for keys')

        if redis_client.exists(redis_key):
            stickers_dict_str_json = redis_client.get(redis_key)
            stickers_dict = json.loads(stickers_dict_str_json)
        else:
            stickers = db_client.get_all_stickers()
            for sticker in stickers:
                key = sticker[1]
                stickers_dict[key] = {
                    "price": sticker[0],
                    "name": sticker[1],
                    "key": sticker[2],
                    "id": str(sticker[3])
                }
            if stickers_dict:
                redis_client.set(redis_key, json.dumps(stickers_dict), ex=60)

        logging.debug(f'Fetched {len(stickers_dict)} stickers')
        time.sleep(1)

    return stickers_dict
