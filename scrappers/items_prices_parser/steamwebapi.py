import time
import json
import logging
import requests
import datetime

from pathlib import Path

from classes import DBClient

# https://www.steamwebapi.com/api/doc/steam-market-api

class PriceParser:
    def __init__(self):
        self.body = 'https://www.steamwebapi.com/steam/api/items?key='
        self.key = 'KT8DIAE9C2Q29L9X'

        # To save or to use saved data
        self.file_path = Path('data/steamwebapi.json')


    def send_request(self):
        url = f'{self.body}{self.key}'
        response = requests.get(url)
        response.raise_for_status()  # Will raise an error for HTTP codes 4xx/5xx
        return response

    def save_data(self, data):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_data(self):
        response = self.send_request()
        text_data = response.text.encode('utf-8').decode('unicode_escape')
        data = json.loads(text_data)

        # self.save_data(data) # Uncomment this line to save data

        return data

    def parse_weapon_name(self, name, parsed_weapons):
        weapon_qualities = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']

        weapon_name = name

        parsed_weapons['is_souvenir'] = False
        parsed_weapons['is_stattrak'] = False

        # For now we are skipping Souvenir, this code for future
        # if 'Souvenir' in weapon_name:
        #     parsed_weapons['is_souvenir'] = True
        #     weapon_name = weapon_name.replace('Souvenir', '').strip()

        if 'StatTrak™' in weapon_name:
            parsed_weapons['is_stattrak'] = True
            weapon_name = weapon_name.replace('StatTrak™', '').strip()

        for quality in weapon_qualities:
            if quality in weapon_name:
                parsed_weapons['weapon_quality'] = quality
                weapon_name = weapon_name.replace(f"({quality})", '').strip()

        parsed_weapons['weapon_name'] = weapon_name

    def parse_sticker_name(self, name, parsed_stickers):
        sticker_qualities = ['Gold', 'Holo', 'Foil', 'Glitter']

        parsed_stickers['sticker_quality'] = ''

        sticker_name = name

        if 'Sticker |' in sticker_name:
            sticker_name = sticker_name.replace('Sticker |', '').strip()

        for quality in sticker_qualities:
            if quality in sticker_name:
                parsed_stickers['sticker_quality'] = quality
                # sticker_name = sticker_name.replace(f"({quality}) ", '').strip()

        parsed_stickers['sticker_name'] = sticker_name

    def parce_steam_price(self, item, parsed_item):
        price_fields = [
            'pricemedian7d',
            'pricemedian',
            'priceavg',
            'pricereal7d',
            'pricereal',
            'pricelatestsell'
        ]

        parsed_item['price'] = next((item.get(field) for field in price_fields if item.get(field) is not None), -1)

    def get_item_image_url(self, item, parsed_item):
        logging.info(f"{item['marketname']}: Getting image url for")
        steam_service_url = 'https://community.cloudflare.steamstatic.com/economy/image/'
        parsed_item['icon_url'] = item.get('itemimage', '').replace(steam_service_url, '').strip()

    def get_rarity(self, item, parsed_item):
        parsed_item['rarity'] = item.get('rarity', '')

    def read_saved_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

    def parser(self):
        insert_weapons = []
        insert_stickers = []

        weapon_items_groups = ['rifle', 'pistol', 'smg', 'shotgun', 'machinegun', "sniper rifle"]

        # data = self.get_data()
        data = self.read_saved_data()  # Uncomment this line to read from saved data

        for item in data:
            name = item.get('marketname', '')
            item_group = item.get('itemgroup')

            if item_group in weapon_items_groups:
                parsed_weapons = {}

                if 'Souvenir' in name:
                    logging.debug(f"Souvenir weapon skiped: {name}")
                    continue
                else:

                    self.parse_weapon_name(name, parsed_weapons)
                    self.parce_steam_price(item, parsed_weapons)
                    self.get_rarity(item, parsed_weapons)
                    self.get_item_image_url(item, parsed_weapons)

                    for field_name in ['weapon_name', 'weapon_quality', 'is_stattrak', 'price', 'icon_url', 'rarity']:
                        if parsed_weapons.get(field_name, None) is None:
                            logging.warning(f"Weapon parsing warning: {field_name} is None for item '{name}'")

                    weapon_tuple = (
                        parsed_weapons.get('weapon_name', None),
                        parsed_weapons.get('weapon_quality', None),
                        parsed_weapons.get('is_stattrak', None),
                        parsed_weapons.get('price', -1),
                        datetime.datetime.now(),
                        parsed_weapons.get('icon_url', None),
                        parsed_weapons.get('rarity', None)
                    )

                    insert_weapons.append(weapon_tuple)

            elif item_group == 'sticker':
                parsed_stickers = {}

                self.parse_sticker_name(name, parsed_stickers)
                self.parce_steam_price(item, parsed_stickers)
                self.get_rarity(item, parsed_stickers)
                self.get_item_image_url(item, parsed_stickers)

                for field_name in ['sticker_name', 'price', 'icon_url', 'rarity', 'sticker_quality']:
                    if parsed_stickers.get(field_name, None) is None:
                        logging.warning(f"Sticker parsing warning: {field_name} is None for item '{name}'")

                sticker_tuple = (
                    parsed_stickers.get('sticker_name', None),
                    parsed_stickers.get('price', -1),
                    parsed_stickers.get('icon_url', None),
                    datetime.datetime.now(),
                    parsed_stickers.get('rarity', None),
                    parsed_stickers.get('sticker_quality', None),
                )

                insert_stickers.append(sticker_tuple)

        if insert_stickers:
            DBClient().update_stickers_prices(insert_stickers)
        if insert_weapons:
            DBClient().update_weapon_prices(insert_weapons)

        # TODO: Do we need to save profit?
        # DBClient().update_skins_profit_by_weapon(weapons)


if __name__ == "__main__":
    # TODO: Add more logging
    # BUILD_TYPE=infrastructure ansible-playbook  prepare-build-config.yml
    # docker-compose up -d --build
    logging.info("Start parsing")
    parser = PriceParser()
    result = parser.parser()
    logging.info("Finish parsing")
    time.sleep(86400) # 24 hours
