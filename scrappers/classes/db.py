import os
import pg8000
import logging

class DBClient:
    def __init__(self) -> None:
        database = os.environ.get("POSTGRES_DB")
        user = os.environ.get("POSTGRES_USER")
        password = os.environ.get("POSTGRES_PASSWORD")
        host = os.environ.get("POSTGRES_HOST")
        port = os.environ.get("POSTGRES_PORT")
        logging.info("Connecting to database")
        self.db = pg8000.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        logging.info("Connecting to database")

    def execute(self, query, params) -> None:
        with self.db.cursor() as cursor:
            cursor.execute(query, params)
            self.db.commit()

    def update_weapon_prices(self, values):
        placeholders = ','.join(["(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" for x in values])
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
        flat_values = [val for row in values for val in row]
        self.execute(query, flat_values)


    def update_stickers_prices(self, values):
        query = f'''
            INSERT INTO stickers(classid, name, key, price, type, rare, collection, icon_url)
            VALUES {','.join(["(%s,%s,%s,%s,%s,%s,%s,%s)"] * len(values))}
            ON CONFLICT (name) 
            DO UPDATE SET price = EXCLUDED.price, classid = EXCLUDED.classid
        '''
        flat_values = [val for row in values for val in row]
        self.execute(query, flat_values)

    def get_all_stickers(self):
        with self.db.cursor() as cursor:
            cursor.execute('SELECT price, name, key, id FROM stickers')
            stickers = cursor.fetchall()
            return stickers

    def get_all_weapons(self, min_price=0, max_price=1000000000):
        with self.db.cursor() as cursor:
            cursor.execute('''
                SELECT name, price, quality, is_stattrak, id
                FROM weapons_prices
                WHERE price >= %s and price <= %s
                ORDER BY name
            ''', (min_price, max_price,))

            weapons = cursor.fetchall()
            return weapons


    def parse_items_without_link(self):
        items_id, item_links, csgo_links = [], [], []

        with self.db.cursor() as cursor:
            try:
                query = "SELECT id, link, in_game_link FROM skins WHERE ((in_game_link IS NULL or in_game_link = '') AND is_sold = FALSE) or is_sold = FALSE"
                cursor.execute(query)
                data_set = cursor.fetchall()
                for data in data_set:
                    items_id.append(data[0])
                    item_links.append(data[1])
                    csgo_links.append(data[2])

            except Exception as e:
                logging.error(f'Error while parsing items without link: {e}')

        return item_links, items_id, csgo_links


    def __del__(self) -> None:
        if self.db:
            self.db.close()
            logging.info("Database connection closed")