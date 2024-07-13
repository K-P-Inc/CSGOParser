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

        try:
            logging.info("Connecting to database")
            self.db = pg8000.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port
            )
            logging.info("Connected to database")
        except Exception as e:
            logging.error(f"Failed to connect to database: {e}")

    def execute(self, query, params) -> None:
        with self.db.cursor() as cursor:
            cursor.execute(query, params)
            self.db.commit()

    def update_weapon_prices(self, values):
        try:
            placeholders = ','.join(["(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" for _ in values])
            query = f'''
                INSERT INTO weapons_prices(
                    name, quality, is_stattrak, price, market_prices,
                    price_week_low, price_week_high,
                    price_month_low, price_month_high,
                    price_all_time_low, price_all_time_high, parsing_time, icon_url
                ) VALUES {placeholders}
                ON CONFLICT (name, quality, is_stattrak) DO UPDATE SET
                    price = EXCLUDED.price,
                    market_prices = EXCLUDED.market_prices,
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
            logging.info("Updated weapon prices in db")
        except Exception as e:
            logging.error(f"Failed to update weapon prices in db: {e}")

    def update_skins_profit_by_weapon(self, value):
        query = f'''
            WITH cte AS (
                SELECT skins.skin_id
                FROM skins
                JOIN weapons_prices ON skins.skin_id = weapons_prices.id
                WHERE weapons_prices.name = %s
                AND weapons_prices.quality = %s
                AND weapons_prices.is_stattrak = %s
                ORDER BY skins.skin_id
                LIMIT 1
            )
            UPDATE skins
            SET profit = 1 - (skins.price + 0.1 * skins.stickers_price) / %s
            WHERE skin_id IN (SELECT skin_id FROM cte);
        '''
        self.execute(query, value)

    def update_skins_profit_by_stickers(self, value):
        return
        query = f''''''
        self.execute(query, value)

    def insert_skins(self, values):
        placeholders = ','.join(["(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" for _ in values])
        query = f'''
            INSERT INTO skins(
                market, link, stickers_price, price, profit, skin_id,
                stickers_patern, amount_of_stickers_distinct, amount_of_stickers, is_sold, stickers,
                stickers_wears, item_float, in_game_link, pattern_template, order_type, stickers_distinct_variants
            ) VALUES {placeholders}
            ON CONFLICT (link) DO UPDATE SET
                stickers_price = EXCLUDED.stickers_price,
                price = EXCLUDED.price,
                profit = EXCLUDED.profit,
                skin_id = EXCLUDED.skin_id,
                stickers_patern = EXCLUDED.stickers_patern,
                amount_of_stickers_distinct = EXCLUDED.amount_of_stickers_distinct,
                amount_of_stickers = EXCLUDED.amount_of_stickers,
                is_sold = EXCLUDED.is_sold,
                stickers = EXCLUDED.stickers
        '''
        flat_values = [val for row in values for val in row]
        self.execute(query, flat_values)

    def update_stickers_prices(self, values, parser=None):
        try:
            if parser == 'csgoskins':
                query = f'''
                    INSERT INTO stickers(name, price, icon_url, market_prices, price_week_low, price_week_high, price_month_low,
                    price_month_high, price_all_time_low, price_all_time_high, parsing_time, rare, type)
                    VALUES {','.join(["(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"] * len(values))}
                    ON CONFLICT (name)
                    DO UPDATE SET price = EXCLUDED.price,
                    market_prices = EXCLUDED.market_prices,
                    price_week_low = EXCLUDED.price_week_low,
                    price_week_high = EXCLUDED.price_week_high,
                    price_month_low = EXCLUDED.price_month_low,
                    price_month_high = EXCLUDED.price_month_high,
                    price_all_time_low = EXCLUDED.price_all_time_low,
                    price_all_time_high = EXCLUDED.price_all_time_high,
                    parsing_time = EXCLUDED.parsing_time,
                    rare = EXCLUDED.rare,
                    type = EXCLUDED.type
                '''
            else:
                query = f'''
                    INSERT INTO stickers(classid, name, key, price, type, rare, collection, icon_url, market_prices)
                    VALUES {','.join(["(%s,%s,%s,%s,%s,%s,%s,%s,%s)"] * len(values))}
                    ON CONFLICT (name)
                    DO UPDATE SET price = EXCLUDED.price, classid = EXCLUDED.classid, market_prices = EXCLUDED.market_prices
                '''
            flat_values = [val for row in values for val in row]
            self.execute(query, flat_values)
            logging.info("Updated sticker prices in db")
        except Exception as e:
            logging.error(f"Failed to update weapon prices in db: {e}")

    def get_all_stickers(self):
        with self.db.cursor() as cursor:
            cursor.execute('SELECT price, name, key, id FROM stickers')
            stickers = cursor.fetchall()
            return stickers

    def get_all_weapons(self, type, min_price=0, max_price=1000000000):
        with self.db.cursor() as cursor:
            cursor.execute(f'''
                SELECT name, price, quality, is_stattrak, id
                FROM weapons_prices
                WHERE price >= %s and price <= %s and name LIKE '{type}%'
                ORDER BY name
            ''', (min_price, max_price))

            weapons = cursor.fetchall()
            return weapons

    def delete_old_skins(self, market, weapon_uuids):
        with self.db.cursor() as cursor:
            cursor.execute(f'''
                DELETE FROM skins
                WHERE market = %s AND skin_id IN ({",".join(len(weapon_uuids) * ["%s"])})
            ''', [market, *weapon_uuids])

    def update_skins_as_sold(self, market, parsed_urls, weapon_uuids):
        with self.db.cursor() as cursor:
            if len(parsed_urls) > 0:
                cursor.execute(f'''
                    UPDATE skins SET is_sold = True
                    WHERE link NOT IN ({",".join(len(parsed_urls) * ["%s"])}) AND market = %s AND skin_id IN ({",".join(len(weapon_uuids) * ["%s"])})
                ''', [*parsed_urls, market, *weapon_uuids])
            else:
                cursor.execute(f'''
                    UPDATE skins SET is_sold = True
                    WHERE market = %s AND skin_id IN ({",".join(len(weapon_uuids) * ["%s"])})
                ''', [market, *weapon_uuids])


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
