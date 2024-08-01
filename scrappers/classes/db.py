import os
import psycopg2, psycopg2.extensions
import logging
import threading
import time
from functools import wraps

def retry(fn):
    @wraps(fn)
    def wrapper(*args, **kw):
        cls: DBClient = args[0]
        for x in range(cls._reconnectTries):
            try:
                return fn(*args, **kw)
            except (psycopg2.InterfaceError, psycopg2.OperationalError) as e:
                logging.info("\nDatabase Connection [InterfaceError or OperationalError]")
                logging.info("Idle for %s seconds" % (cls._reconnectIdle))
                time.sleep(cls._reconnectIdle)
                cls._connect()
    return wrapper


class DBClient:
    _reconnectTries = 50
    _reconnectIdle = 2  # wait seconds before retying
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if not cls._instance:
                cls._instance = super(DBClient, cls).__new__(cls)
                cls._instance.__init__()

        return cls._instance

    def __init__(self) -> None:
        self.database = os.environ.get("POSTGRES_DB")
        self.user = os.environ.get("POSTGRES_USER")
        self.password = os.environ.get("POSTGRES_PASSWORD")
        self.host = os.environ.get("POSTGRES_HOST")
        self.port = os.environ.get("POSTGRES_PORT")
        logging.debug(f"\nDatabase: {self.database}\nUser: {self.user}\nPassword: {self.password}\nHost: {self.host}\nPort: {self.port}\n")

        self._connect()

    def _connect(self) -> None:
        logging.debug("Connecting to database")
        self.db = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port
        )
        logging.debug("Connected to database")

    @retry
    def execute(self, query, params) -> None:
        with self.db.cursor() as cursor:
            try:
                cursor.execute(query, params)
                self.db.commit()
            except BaseException as e:
                logging.error(f'Failed to run query ({query=}, {params=}): {e}')
                if cursor is not None:
                    self.db.rollback()

    @retry
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
        logging.debug("Updated weapon prices in db")

    @retry
    def update_skins_profit_by_weapon(self, value):
        query = f'''
            WITH locked_skins AS (
                SELECT *, skins.id as item_id
                FROM skins
                JOIN weapons_prices wp ON skins.skin_id = wp.id
                WHERE skins.is_sold = False AND wp.name LIKE '{value}%'
                FOR UPDATE SKIP LOCKED
            )
            UPDATE skins
            SET profit = (skins.stickers_price * 0.1 + wp.price - skins.price) / (skins.stickers_price * 0.1 + wp.price) * 100.0
            FROM weapons_prices wp, locked_skins as ls
            WHERE skins.skin_id = wp.id AND ls.item_id = skins.id
        '''
        self.execute(query)

    @retry
    def update_skins_profit_by_stickers(self):
        query = f'''
            UPDATE skins
            SET
                stickers_price = ss.total_price,
                profit = (ss.total_price * 0.1 + ss.steam_price - skins.price) / (ss.total_price * 0.1 + ss.steam_price) * 100.0
            FROM (
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
                    FROM (SELECT * FROM skins FOR UPDATE SKIP LOCKED) as s
                    CROSS JOIN unnest(s.stickers) AS st(id)
                    WHERE s.is_sold = False
                    GROUP BY s.id, s.skin_id, st.id
                ) AS sc
                INNER JOIN stickers st ON st.id = sc.sticker_id
                INNER JOIN weapons_prices wp ON wp.id = sc.weapon_id
                GROUP BY sc.skin_id, wp.price
            ) AS ss
            WHERE skins.id = ss.skin_id;
        '''
        self.execute(query)

    @retry
    def insert_skins(self, values):
        placeholders = ','.join(["(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CAST(%s AS uuid[]),CAST(%s AS double precision[]),%s,%s,%s,%s,CAST(%s AS csgo_stickers_variant[]))" for _ in values])
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
                stickers = EXCLUDED.stickers,
                stickers_wears = EXCLUDED.stickers_wears,
                item_float = EXCLUDED.item_float,
                in_game_link = EXCLUDED.in_game_link,
                pattern_template = EXCLUDED.pattern_template,
                order_type = EXCLUDED.order_type,
                stickers_distinct_variants = EXCLUDED.stickers_distinct_variants
        '''
        flat_values = [val for row in values for val in row]
        self.execute(query, flat_values)

    @retry
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
        logging.debug("Updated sticker prices in db")

    @retry
    def get_all_stickers(self):
        with self.db.cursor() as cursor:
            cursor.execute('SELECT price, name, key, id FROM stickers')
            stickers = cursor.fetchall()
            return stickers

    @retry
    def get_all_weapons(self, type, min_price=0, max_price=1000000000):
        with self.db.cursor() as cursor:
            cursor.execute(f'''
                SELECT name, price, quality, is_stattrak, id
                FROM weapons_prices
                WHERE price >= %s and price <= %s and name LIKE %s
                ORDER BY name
            ''', (min_price, max_price, f'{type}%'))

            weapons = cursor.fetchall()
            return weapons

    @retry
    def delete_old_skins(self, market, weapon_uuids):
        with self.db.cursor() as cursor:
            cursor.execute(f'''
                DELETE FROM skins
                WHERE market = %s AND skin_id IN ({",".join(len(weapon_uuids) * ["%s"])})
            ''', [market, *weapon_uuids])

    @retry
    def update_skins_as_sold(self, market, parsed_urls, weapon_uuids):
        if len(parsed_urls) > 0:
            self.execute(f'''
                UPDATE skins SET is_sold = True
                WHERE link NOT IN ({",".join(len(parsed_urls) * ["%s"])}) AND market = %s AND skin_id IN ({",".join(len(weapon_uuids) * ["%s"])}) AND is_sold = False
            ''', [*parsed_urls, market, *weapon_uuids])
        else:
            self.execute(f'''
                UPDATE skins SET is_sold = True
                WHERE market = %s AND skin_id IN ({",".join(len(weapon_uuids) * ["%s"])}) AND is_sold = False
            ''', [market, *weapon_uuids])

    @retry
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
            logging.debug("Database connection closed")
            self.db = None