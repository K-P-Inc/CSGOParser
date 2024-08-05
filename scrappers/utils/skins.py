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


def calculate_weapon_real_price(item_price, weapon_key_price, matched_stickers, wears_stickers, stickers_dict, weapons_dict):
    stickers_pattern_coef = {
        1 : 0.001,
        2 : 0.01,
        3 : 0.05,
        4 : 0.1,
        5 : 0.1,
    }
    stickers_price_coef = {
        1 : 0.5,
        2 : 1,
        3 : 2,
        4 : 4,
        5 : 4
    }

    stickers_overprice = 0

    sticker_count = {}
    valid_sticker_count = {}
    for index, sticker in enumerate(matched_stickers):
        key = sticker["name"]

        if key in sticker_count:
            sticker_count[key] += 1
        else:
            sticker_count[key] = 1

        if wears_stickers[index] == 0 or not wears_stickers[index]:
            if key in valid_sticker_count:
                valid_sticker_count[key] += 1
            else:
                valid_sticker_count[key] = 1

    num_stickers = len(sticker_count)

    stickers_pattern = 'other'
    if num_stickers == 1 and max(sticker_count.values()) == 5:
        stickers_pattern = '5-equal'
    elif num_stickers in [1, 2] and max(sticker_count.values()) == 4:
        stickers_pattern = '4-equal'
    elif max(sticker_count.values()) == 3:
        stickers_pattern = '3-equal'
    elif sorted(sticker_count.values()) == [2, 2] or sorted(sticker_count.values()) == 2:
        stickers_pattern = '2-equal'
    elif max(sticker_count.values()) == 2:
        stickers_pattern = '2-equal'
    else:
        stickers_pattern = 'other'

    for key, amount in valid_sticker_count.items():
        integer_part = str(stickers_dict[key]["price"]).split('.')[0]

        # Find the number of digits in the integer part
        num_digits = min(len(integer_part), 5)

        stickers_overprice += stickers_dict[key]["price"] * stickers_pattern_coef[amount] * stickers_price_coef[num_digits]

    actually_price_steam = weapons_dict[weapon_key_price]["price"]
    future_profit_percentages_steam = (stickers_overprice + actually_price_steam - item_price) / (stickers_overprice + actually_price_steam) * 100

    actually_price_buff = weapons_dict[weapon_key_price]["price"] * 0.7 if weapons_dict[weapon_key_price]["price"] < 1500 else weapons_dict[weapon_key_price]["price"] 
    future_profit_percentages_buff = (stickers_overprice + actually_price_buff - item_price) / (stickers_overprice + actually_price_buff) * 100

    return stickers_pattern, round(stickers_overprice, 2), future_profit_percentages_steam, future_profit_percentages_buff