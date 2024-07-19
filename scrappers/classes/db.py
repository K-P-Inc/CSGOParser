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

        # logging.info(f"\nDatabase: {database}\nUser: {user}\nPassword: {password}\nHost: {host}\nPort: {port}\n")

        logging.info("Connecting to database")
        self.db = pg8000.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        logging.info("Connected to database")

    def execute(self, query, params) -> None:
        with self.db.cursor() as cursor:
            cursor.execute(query, params)
            self.db.commit()

    def update_weapon_prices(self, values):
        placeholders = ','.join(["(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" for _ in values])
        query = f'''
            INSERT INTO weapons_prices(
                name, quality, is_stattrak, price, market_prices,
                price_week_low, price_week_high, price_month_low, price_month_high, price_all_time_low,
                price_all_time_high, parsing_time, icon_url, rare
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
                parsing_time = EXCLUDED.parsing_time
        '''
        flat_values = [val for row in values for val in row]
        self.execute(query, flat_values)
        logging.info("Updated weapon prices in db")

    def update_skins_profit_by_weapon(self, value):
        query = f'''
            WITH locked_skins AS (
                SELECT skins.skin_id
                FROM skins
                JOIN weapons_prices wp ON skins.skin_id = wp.id
                WHERE is_sold = False AND wp.name LIKE '{value}%%'
                FOR UPDATE
            )
            UPDATE skins
            SET profit = (skins.stickers_price * 0.1 + wp.price - skins.price) / (skins.stickers_price * 0.1 + wp.price) * 100.0
            FROM weapons_prices wp
            WHERE skins.skin_id = wp.id AND is_sold = False AND wp.name LIKE '{value}%%';
        '''
        self.execute(query, ())

    def update_skins_profit_by_stickers(self):
        query = f'''
            WITH stickers_subquery AS (
                SELECT
                    sc.skin_id,
                    wp.price as steam_price,
                    SUM(st.price * sc.count_stickers) as total_price  
                FROM (
                    SELECT
                        s.id as skin_id,
                        s.skin_id as weapon_id,
                        st.id as sticker_id,
                        COUNT(*) as count_stickers
                    FROM skins s
                    CROSS JOIN unnest(s.stickers) AS st(id)
                    WHERE s.is_sold = False
                    GROUP BY s.id, s.skin_id, st.id
                    FOR UPDATE
                ) AS sc
                INNER JOIN stickers st ON st.id = sc.sticker_id
                INNER JOIN weapons_prices wp ON wp.id = sc.weapon_id
                GROUP BY sc.skin_id, wp.price
            )
            UPDATE skins
            SET
                stickers_price = ss.total_price,
                profit = (ss.total_price * 0.1 + ss.steam_price - skins.price) / (ss.total_price * 0.1 + ss.steam_price) * 100.0
            FROM stickers_subquery ss
            WHERE skins.id = ss.skin_id;
        '''
        self.execute(query, ())

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
                is_sold = EXCLUDED.is_sold
        '''
        flat_values = [val for row in values for val in row]
        self.execute(query, flat_values)

    def update_stickers_prices(self, values, parser=None):
        if parser == 'csgoskins':
            query = f'''
                INSERT INTO stickers(name, price, icon_url, market_prices, price_week_low, price_week_high, price_month_low,
                price_month_high, price_all_time_low, price_all_time_high, parsing_time, rare, type, collection)
                VALUES {','.join(["(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"] * len(values))}
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
                type = EXCLUDED.type,
                collection = EXCLUDED.collection
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
                    DELETE FROM skins
                    WHERE link NOT IN ({",".join(len(parsed_urls) * ["%s"])}) AND market = %s AND skin_id IN ({",".join(len(weapon_uuids) * ["%s"])}) AND is_sold = False
                ''', [*parsed_urls, market, *weapon_uuids])
            else:
                cursor.execute(f'''
                    DELETE FROM skins
                    WHERE market = %s AND skin_id IN ({",".join(len(weapon_uuids) * ["%s"])}) AND is_sold = False
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
