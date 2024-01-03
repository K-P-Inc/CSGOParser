import requests
import json
import os
import datetime
import pg8000
from dotenv import load_dotenv


if __name__ == '__main__':
    try:
        print("Loading dotenv")
        load_dotenv()
        with open('skins.json', 'r') as f:
            contents = json.loads(f.read())

        print("Connection to database")
        conn = pg8000.connect(
            host="db",
            database="postgres",
            user="postgres",
            password="superbotparser"
        )

        request = requests.get('http://csgobackpack.net/api/GetItemsList/v2/')
        result_mapping = request.json()
        print("Got results from API")

        for key, item in result_mapping['items_list'].items():
            if 'type' in item and 'gun_type' in item and 'price' in item:
                if item['type'] == 'Weapon' and 'Souvenir' not in item['name']:
                    cur = conn.cursor()
                    query = '''
                        INSERT INTO weapons_prices(
                            name, quality, is_stattrak, price,
                            price_week_low, price_week_high,
                            price_month_low, price_month_high,
                            price_all_time_low, price_all_time_high, parsing_time, icon_url
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (name, quality, is_stattrak) DO UPDATE SET
                            price = EXCLUDED.price,
                            price_week_low = EXCLUDED.price_week_low,
                            price_week_high = EXCLUDED.price_week_high,
                            price_month_low = EXCLUDED.price_month_low,
                            price_month_high = EXCLUDED.price_month_high,
                            price_all_time_low = EXCLUDED.price_all_time_low,
                            price_all_time_high = EXCLUDED.price_all_time_high,
                            parsing_time = EXCLUDED.parsing_time
                            icon_url = EXCLUDED.icon_url
                    '''
                    price = 0
                    for qual in ['24_hours', '7_days', '30_days', 'all_time']:
                        if qual in item["price"]:
                            price = item["price"][qual]["average"]
                            break
                    name = item["name"].replace("StatTrak™ ", "").replace(f' ({item["exterior"]})', "")
                    cur.execute(query, (
                        name, item["exterior"], 'stattrak' in item, price,
                        item["price"]["7_days"]['lowest_price'] if "7_days" in item["price"] else 0,
                        item["price"]["7_days"]['highest_price'] if "7_days" in item["price"] else 0,
                        item["price"]["30_days"]['lowest_price'] if "30_days" in item["price"] else 0,
                        item["price"]["30_days"]['highest_price'] if "30_days" in item["price"] else 0,
                        item["price"]["all_time"]['lowest_price'] if "all_time" in item["price"] else 0,
                        item["price"]["all_time"]['highest_price'] if "all_time" in item["price"] else 0,
                        datetime.datetime.now(),
                        item["icon_url"]
                    ))
                    conn.commit()
            elif "sticker" in item and "price" in item:
                cur = conn.cursor()
                query = '''
                    INSERT INTO stickers(name, key, price, type, rare, collection)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (name) 
                    DO UPDATE SET price = EXCLUDED.price
                '''
                key_sticker = None
                name = item['name'].replace("Sticker | ", "")
                for key, value in contents.items():
                    if 'name' in value and value['name'] == name:
                        key_sticker = key
                        break

                if key_sticker is not None:
                    price = 0
                    for qual in ['24_hours', '7_days', '30_days', 'all_time']:
                        if qual in item["price"]:
                            price = item["price"][qual]["average"]
                            break

                    cur.execute(query, (
                        name,
                        key_sticker,
                        price,
                        "", item["rarity"], ""
                    ))

                    conn.commit()

        print("Items parsed")

        conn.close()
    except Exception as e:
        print(e)