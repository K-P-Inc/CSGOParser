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

        with open('ids.json', 'r') as f:
            ids = json.loads(f.read())

        print("Connection to database")
        database = os.environ.get("POSTGRES_DB")
        user = os.environ.get("POSTGRES_USER")
        password = os.environ.get("POSTGRES_PASSWORD")
        host = os.environ.get("POSTGRES_HOST")
        port = os.environ.get("POSTGRES_PORT")
        conn = pg8000.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        request = requests.get('http://csgobackpack.net/api/GetItemsList/v2/')
        result_mapping = request.json()
        print("Got results from API")

        with conn.cursor() as cur:
            weaponts_to_insert = []
            stickers_to_insert = []
            for key, item in result_mapping['items_list'].items():
                print("Got item from API", key, item)
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

                        if len(weaponts_to_insert) > 1000:
                            placeholders = ','.join(["(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" for x in weaponts_to_insert])
                            query = f'''
                                INSERT INTO weapons_prices(
                                    name, quality, is_stattrak, price,
                                    price_week_low, price_week_high,
                                    price_month_low, price_month_high,
                                    price_all_time_low, price_all_time_high, parsing_time, icon_url
                                ) VALUES {placeholders}
                                ON CONFLICT (name, quality, is_stattrak) DO UPDATE SET
                                    price = EXCLUDED.price,
                                    price_week_low = EXCLUDED.price_week_low,
                                    price_week_high = EXCLUDED.price_week_high,
                                    price_month_low = EXCLUDED.price_month_low,
                                    price_month_high = EXCLUDED.price_month_high,
                                    price_all_time_low = EXCLUDED.price_all_time_low,
                                    price_all_time_high = EXCLUDED.price_all_time_high,
                                    parsing_time = EXCLUDED.parsing_time,
                                    icon_url = EXCLUDED.icon_url
                            '''

                            flat_values = [val for row in weaponts_to_insert for val in row]
                            cur.execute(query, flat_values)
                            weaponts_to_insert.clear()
                elif "sticker" in item and "price" in item:
                    query = '''
                        INSERT INTO stickers(classid, name, key, price, type, rare, collection, icon_url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (name) 
                        DO UPDATE SET price = EXCLUDED.price, classid = EXCLUDED.classid
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

                    stickers_to_insert.append((
                        ids[item['name']] if item['name'] in ids else '',
                        name,
                        key_sticker,
                        price,
                        "", item["rarity"], "",
                        item["icon_url"]
                    ))
                    if len(stickers_to_insert) > 1000:
                        placeholders = ','.join(["(%s,%s,%s,%s,%s,%s,%s,%s)"] * len(stickers_to_insert))
                        query = f'''
                            INSERT INTO stickers(classid, name, key, price, type, rare, collection, icon_url)
                            VALUES {placeholders}
                            ON CONFLICT (name) 
                            DO UPDATE SET price = EXCLUDED.price, classid = EXCLUDED.classid
                        '''

                        flat_values = [val for row in stickers_to_insert for val in row]
                        cur.execute(query, flat_values)
                        stickers_to_insert.clear()

        conn.commit()
        print("Items parsed")

        conn.close()
    except Exception as e:
        print(e)