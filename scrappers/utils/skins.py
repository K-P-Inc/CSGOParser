import logging
import time

def get_weapons_array_by_type(db_client, weapon_config, parsed_items):
    weapons = []
    weapons_prices = {}

    while len(weapons) == 0:
        logging.info(f'Getting skins from database, already parsed {parsed_items}')
        weapons = db_client.get_all_weapons(weapon_config.min_steam_item_price, weapon_config.max_steam_item_price)
        weapons_prices = {}
        for weapon in weapons:
            if weapon_config.type in weapon[0]:
                key = f'{"StatTrak™ " if weapon[3] == True else ""}{weapon[0]} ({weapon[2]})'
                weapons_prices[key] = {
                    "uuid": weapon[4],
                    "price": weapon[1]
                }

        weapons = sorted(list(set([
            (weapon[0].split(' | ')[0], weapon[0].split(' | ')[1], weapon[3])
            for weapon in weapons
            if weapon[0].split(' | ')[0] == weapon_config.type
        ])))

        if len(weapons) > parsed_items:
            weapons = weapons[parsed_items:]
        else:
            logging.info(f'All items parsed, reseting parsed items counter')
            parsed_items = 0

        logging.info(f'Fetched {len(weapons)} skins from database')
        time.sleep(1)

    return weapons, weapons_prices

def get_stickers_dict(db_client):
    stickers_dict = {}
    while len(stickers_dict) == 0:
        logging.info('Getting stickers from database for keys')
        stickers = db_client.get_all_stickers()
        for sticker in stickers:
            key = sticker[1]
            stickers_dict[key] = sticker
        logging.info(f'Fetched {len(stickers_dict)} stickers')
        time.sleep(1)

    return stickers_dict
