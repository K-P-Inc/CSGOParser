import requests
import json
import time
import logging
from urllib.parse import quote, urlencode
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from .redis import RedisClient
from .driver import SeleniumDriver


# stickers_wears = 0 (not scratched)
# stickers_wears = 0.68 (100% - 68% = 32% sticker health)
# stickers_wears = 1 (fully scratched)

# is_buy_type_fixed = 'fixed' (not auctions)
# is_buy_type_fixed = False (auctions)


class BaseHelper:
    PARSE_WITH_QUALITY = False

    def _get_fullname(self, type, name, is_stattrak):
        return f"{'StatTrak™ ' if is_stattrak else ''}{type} | {name}"

class SkinbidHelper(BaseHelper):
    DB_ENUM_NAME = 'skinbid'
    MAX_ITEMS_PER_PAGE = 120
    REQUEST_TIMEOUT = 3

    def parse_item(self, item):
        item_json = item["items"][0]["item"]
        key_price = item_json["fullName"]
        # TODO: Here we got EUR price, do we change it to USD?
        item_price = float(item["auction"]["startBid"] if item['auction']['sellType'] == 'FIXED_PRICE' and item["currentHighestBid"] != 0.0 else item["currentHighestBid"])
        item_link = f'https://skinbid.com/market/{item["auction"]["auctionHash"]}'
        stickers_keys = [sticker["name"] for sticker in item_json.get("stickers", [])]
        stickers_wears = [(round(float(sticker["wear"]), 2) if "wear" in sticker else None) for sticker in item_json.get("stickers", [])]
        item_float = item_json.get('float')

        item_in_game_link = item_json.get('inspectLink')
        pattern_template = item_json.get('paintSeed')

        is_buy_type_fixed = 'fixed' if item['auction']['sellType'] == 'FIXED_PRICE' else 'auction'

        return key_price, item_price, item_link, stickers_keys, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed

    def do_request(self, type, name, is_stattrak, max_price, page_number = 0):
        url = f"https://api.skinbid.com/api/search/auctions?take=120&sort=discount%23desc&goodDeals=false&popular=false&currency=USD&name={quote(name)}&type={type}&Category=Stickers%23true,Souvenir%23false,{'StatTrak%23false' if is_stattrak == False else 'StatTrak%23true'}&skip={self.MAX_ITEMS_PER_PAGE * page_number}"
        response = requests.request("GET", url, headers={}, data={})

        try:
            if json.loads(response.text) and len(json.loads(response.text)["items"]) >= 0:
                return json.loads(response.text)["items"]
            return None
        except:
            return None


class CSMoneyHelper(BaseHelper):
    DB_ENUM_NAME = 'cs-money'
    MAX_ITEMS_PER_PAGE = 60
    REQUEST_TIMEOUT = 3

    def parse_item(self, item):
        item_json = item["asset"]
        key_price = item_json["names"]["full"]
        item_price = float(item["pricing"]["computed"])

        if round(item_json["float"], 8) - item_json["float"] > 0:
            start_float = round(round(item_json["float"], 8) - 10 ** -8, 8)
            end_float = round(item_json["float"], 8)
        else:
            start_float = round(item_json["float"], 8)
            end_float = round(round(item_json["float"], 8) + 10 ** -8, 8)

        item_link = f'https://cs.money/market/buy/?search={quote(key_price)}&sort=price&order=asc&minFloat={start_float:.8f}&maxFloat={end_float:.8f}&unique_id={item["id"]}'
        stickers_keys = [sticker["name"].replace("Sticker | ", "") for sticker in item["stickers"] if sticker] if "stickers" in item else []

        stickers_wears = [
            (round(float(sticker["wear"] / 100), 2) if "wear" in sticker else None) 
            for sticker in item["stickers"] if sticker
        ] if "stickers" in item else []

        item_float = item_json["float"]

        # steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S[Put_your_steam_id_here]A[Put_Item_ID_here]D[Last_step_D_thing_here_pls]
        item_in_game_link = f"steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S{item['seller']['steamId64']}A{item_json['id']}D{item_json['inspect']}" if ("seller" in item and "steamId64" in item["seller"]) and ("inspect" in item_json) and ("id" in item_json) else ""
        pattern_template = item_json['pattern']

        is_buy_type_fixed = 'fixed'

        return key_price, item_price, item_link, stickers_keys, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed

    def do_request(self, type, name, is_stattrak, max_price, page_number = 0):
        url = f"https://cs.money/1.0/market/sell-orders?isStatTrak={'true' if is_stattrak else 'false'}&order=asc&sort=price&isSouvenir=false&hasStickers=true&limit={self.MAX_ITEMS_PER_PAGE}&name={quote(type)}%20%7C%20{quote(name)}&offset={page_number * self.MAX_ITEMS_PER_PAGE}&maxPrice={max_price}"
        response = requests.request("GET", url, headers={}, data={})

        json_response = json.loads(response.text)
        if json_response and "items" in json_response and len(json_response["items"]) >= 0:
            return json_response["items"]
        if json_response and "error" in json_response and len(json_response["errors"]) >= 0:
            return []
        else:
            raise Exception(f"Couldn't parse response for skin {type} {name}")

class MarketCSGOHelper(BaseHelper):
    DB_ENUM_NAME = 'market-csgo'
    MAX_ITEMS_PER_PAGE = 400
    REQUEST_TIMEOUT = 8

    def parse_item(self, item):
        key_price = item["market_hash_name"]
        market_csgo_item_price = float(item["price"])
        market_csgo_item_link = f'https://market.csgo.com/en/{quote(item["seo"]["category"])}/{item["seo"]["type"]}/{quote(key_price)}?id={item["id"]}'
        stickers_keys = [sticker["name"] for sticker in item["stickers"]]
        stickers_wears = [None for _ in item["stickers"]]
        item_float = None

        item_in_game_link = None
        pattern_template = None

        is_buy_type_fixed = 'fixed'

        return key_price, market_csgo_item_price, market_csgo_item_link, stickers_keys, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed

    def generate_market_link(self, type, name, is_stattrak):
        return f'https://market.csgo.com/en/?sort=price&order=asc&search={quote(type)}%20%7C%20{quote(name)}%20&priceMax=1000000&categories=any_stickers{"&search=StatTrak" if is_stattrak == True else ""}'

    def do_request(self, type, name, is_stattrak, max_price, page_number = 0):
        url = "https://market.csgo.com/api/graphql"
        search_name = [{ "id": "StatTrak" }, { "id":  f'{type} | {name}' }] if is_stattrak == True else [{ "id":  f'{type} | {name}' }]

        payload = json.dumps({
            "operationName": "items",
            "variables": {
                "filters": [
                    {
                        "id": "search",
                        "items": search_name
                    },
                    {
                        "id": "price",
                        "max": "1000000"
                    },
                    {
                        "id": "categories",
                        "items": [{ "id": "any_stickers" }] if is_stattrak == True else [{ "id": "any_stickers" }, { "id": "Normal" }]
                    }
                ],
                "order": {
                    "id": "price",
                    "direction": "asc"
                },
                "page": page_number,
                "count": self.MAX_ITEMS_PER_PAGE
            },
            "query": "query items($count: Int, $filters: [FilterInputType], $page: Int, $order: OrderInputType!) {\n  items(count: $count, filters: $filters, page: $page, order: $order) {\n    paginatorInfo {\n      count\n      currentPage\n      hasMorePages\n      lastPage\n      perPage\n      total\n      __typename\n    }\n    filters {\n      id\n      items {\n        color\n        enabled\n        id\n        name\n        value\n        image\n        __typename\n      }\n      max\n      min\n      name\n      order\n      type\n      value\n      __typename\n    }\n    meta {\n      title\n      description\n      __typename\n    }\n    data {\n      color\n      id\n      currency\n      stattrak\n      slot\n      popularity\n      features\n      rarity\n      my_item\n      rarity_ext {\n        id\n        name\n        __typename\n      }\n      ctp\n      quality\n      phase\n      descriptions {\n        type\n        value\n        __typename\n      }\n      type\n      tags {\n        category\n        category_name\n        localized_category_name\n        localized_tag_name\n        internal_name\n        name\n        value {\n          name\n          link\n          __typename\n        }\n        __typename\n      }\n      image_512\n      image_100\n      image_150\n      image_300\n      seo {\n        category\n        type\n        __typename\n      }\n      market_hash_name\n      market_name\n      price\n      stickers {\n        image\n        name\n        __typename\n      }\n      __typename\n    }\n    paginatorInfo {\n      count\n      currentPage\n      hasMorePages\n      lastPage\n      perPage\n      total\n      __typename\n    }\n    __typename\n  }\n}"
        })

        headers = {
            'Referer': self.generate_market_link(type, name, is_stattrak),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        try:
            if json.loads(response.text) and len(json.loads(response.text)["data"]["items"]["data"]) >= 0:
                return json.loads(response.text)["data"]["items"]["data"]
            return None
        except:
            time.sleep(5)
            return None

class SkinportHelper(BaseHelper):
    DB_ENUM_NAME = 'skinport'
    MAX_ITEMS_PER_PAGE = 50
    MAX_PAGE_NUMBER = 10
    REQUEST_TIMEOUT = 6
    PARSE_WITH_QUALITY = True # Vulcan (Field-Tested)

    def __init__(self) -> None:
        response = requests.request("GET", "https://skinport.com/api/data")
        json_data = json.loads(response.text)

        self.rates = json_data["rates"]
        self.redis_client = RedisClient()
        self.force_update = True

    def parse_item(self, item):
        key_price = item["marketHashName"]
        item_price = float(item["salePrice"]) / 100.0 * self.rates["USD"]
        item_link = f'https://skinport.com/item/{item["url"]}/{item["saleId"]}'
        stickers_keys = [sticker["name"] for sticker in item["stickers"]]

        stickers_wears = [sticker["wear"] if sticker["wear"] is not None else 0 for sticker in item["stickers"]]
        item_float = item.get('wear')

        item_in_game_link = item.get('link')
        pattern_template = item.get('pattern')

        is_buy_type_fixed = 'fixed'

        return key_price, item_price, item_link, stickers_keys, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed

    def get_cookies(self, type):
        redis_key = f"{type}_skinport_cookies"
        if self.redis_client.exists(redis_key) and not self.force_update:
            logging.info(f"Found cookies in redis for {type}")
            cookies_json = self.redis_client.get(redis_key)
            return json.loads(cookies_json)
        else:
            cookies_json = {
                'i18n': 'eu'
            }
            driver_class = SeleniumDriver()
            driver = driver_class.driver
            driver.delete_all_cookies()
            driver.get("https://skinport.com/")

            time.sleep(5)

            # Get all cookies
            logging.info("Getting cookies from skinport")
            cookies = driver.get_cookies()

            # Print the cookies
            for cookie in cookies:
                if cookie["name"] not in cookies_json:
                    cookies_json[cookie["name"]] = cookie["value"]

            logging.info("Cookies from skinport: {}".format(cookies_json))
            self.redis_client.set(redis_key, json.dumps(cookies_json), ex=3600)
            self.force_update = False

            return cookies_json


    def do_request(self, type, name, is_stattrak, max_price, page_number = 0):
        if page_number > self.MAX_PAGE_NUMBER:
            return []
 
        url = f"https://skinport.com/api/browse/730?search={quote(type)}%20%7C%20{quote(name)}&stattrak={int(is_stattrak)}&souvenir=0&stickers=1&sort=price&order=asc&pricelt={max_price * 100.0 / self.rates['USD']}&skip={page_number}"
        ua = UserAgent()
        user_agent = ua.random

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': f"https://skinport.com/ru/market?search={quote(type)}%20%7C%20{quote(name)}&stattrak={int(is_stattrak)}&souvenir=0&stickers=1&sort=price&order=asc&pricelt={max_price * 100.0 / self.rates['USD']}",
            'User-Agent': user_agent
        }

        try:
            response = requests.request("GET", url, headers=headers, cookies=self.get_cookies(type))
            json_response = json.loads(response.text)
            if json_response and "items" in json_response and len(json_response["items"]) >= 0:
                return json_response["items"]
            elif json_response and "message" in json_response and json_response["message"] == "RATE_LIMIT_REACHED":
                logging.info("Forcing to update cookies")
                self.force_update = True
                return self.do_request(type, name, is_stattrak, max_price, page_number)
            return None
        except:
            self.force_update = False
            return None

class CSFloatHelper(BaseHelper):
    DB_ENUM_NAME = 'csfloat'
    MAX_ITEMS_PER_PAGE = 50
    REQUEST_TIMEOUT = 5
    PARSE_WITH_QUALITY = True # Vulcan (Field-Tested)

    def parse_item(self, item):
        item_json = item["item"]
        key_price = item_json["market_hash_name"]
        item_price = float(item["price"]) / 100.0
        item_link = f'https://csfloat.com/item/{item["id"]}'
        stickers_keys = [sticker["name"].replace("Sticker | ", "") for sticker in item_json["stickers"]] if "stickers" in item_json else []
        stickers_wears = [None for _ in item_json["stickers"]] if "stickers" in item_json else []
        item_float = item_json.get('float_value')

        item_in_game_link = item_json.get('inspect_link')
        pattern_template = item_json.get('paint_seed')

        is_buy_type_fixed = 'fixed' if item['type'] == 'buy_now' else 'auction'

        return key_price, item_price, item_link, stickers_keys, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed

    def do_request(self, type, name, is_stattrak, max_price, page_number = 0):
        fullname = self._get_fullname(type, name, is_stattrak)
        url = f"https://csfloat.com/api/v1/listings?limit=50&sort_by=lowest_price&market_hash_name={quote(fullname)}&max_price={max_price * 100}&page={page_number}"
        response = requests.request("GET", url)

        try:
            if json.loads(response.text) and len(json.loads(response.text)) >= 0:
                return json.loads(response.text)
            return None
        except:
            return None

class BitskinsHelper(BaseHelper):
    DB_ENUM_NAME = 'bitskins'
    MAX_ITEMS_PER_PAGE = 501
    REQUEST_TIMEOUT = 3
    PARSE_WITH_QUALITY = True # Vulcan (Field-Tested)

    def parse_item(self, item):
        key_price = item["name"]
        item_price = float(item["price"]) / 1000.0
        item_link = f'https://bitskins.com/item/cs2/{item["id"]}'
        stickers_keys = [sticker["name"].replace("Sticker | ", "") for sticker in item["stickers"]] if "stickers" in item else []

        stickers_wears = [round(float(sticker["wear"]), 2) for sticker in item["stickers"]] if "stickers" in item else []
        item_float = item.get('float_value')

        # steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S[Put_your_steam_id_here]A[Put_Item_ID_here]D[Last_step_D_thing_here_pls]
        item_in_game_link = f"steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S{item['bot_steam_id']}A{item['asset_id']}D{item['float_id']}"
        pattern_template = item.get('paint_seed')

        is_buy_type_fixed = 'fixed'

        return key_price, item_price, item_link, stickers_keys, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed

    def do_request(self, type, name, is_stattrak, max_price, _):
        try:
            url = f"https://api.bitskins.com/market/search/730"
            payload = json.dumps({
                "order": [{"field": "price", "order": "ASC"}],
                "where": {"skin_name": f"%{type}%{name}%", "category_id": [3 if is_stattrak else 1], "sticker_counter_from": 1, "price_to": max_price * 1000},
                "limit": 500
            })
            response = requests.request("POST", url, data=payload)

            return json.loads(response.text)["list"]

        except:
            return None

class HaloskinsHelper(BaseHelper):
    DB_ENUM_NAME = 'haloskins'
    MAX_ITEMS_PER_PAGE = 500
    REQUEST_TIMEOUT = 3
    PARSE_WITH_QUALITY = True # Vulcan (Field-Tested)

    def __init__(self) -> None:
        self.redis_client = RedisClient()
        self.items_ids_json = {
            'strange': {},
            'normal': {}
        }

    def _check_if_dict_id_exists(self, type, is_stattrak, max_price):
        id = 'strange' if is_stattrak else 'normal'

        if self.items_ids_json[id]:
            return

        redis_key = f"{type}_haloskins_cookies_{id}"
        if self.redis_client.exists(redis_key):
            logging.info(f"Found cookies in redis for {redis_key}")
            cookies_json = self.redis_client.get(redis_key)
            self.items_ids_json[id] = json.loads(cookies_json)
        else:
            url = "https://api.haloskins.com/steam-trade-center/search/product/list?appId=730"
            payload = json.dumps({
                "appId": 730,
                "limit": 500,
                "page": 1,
                "maxPrice": max_price,
                "keyword": type,
                "sort": 0,
                "quality": "strange" if is_stattrak else "normal"
            })
            response = requests.request("POST", url, headers={ 'Content-Type': 'application/json' }, data=payload)
            logging.info(response.text)
            mapping = {}

            for value in json.loads(response.text)["data"]["list"]:
                mapping[value["itemName"]] = value["itemId"]

            logging.info("Updaing haloskins mapping: {}".format(mapping))
            self.redis_client.set(redis_key, json.dumps(mapping), ex=3600)
            self.items_ids_json[id] = mapping

    def _get_item_id(self, name):
        id = 'strange' if 'StatTrak™' in name else 'normal'
        return self.items_ids_json[id][name] if name in self.items_ids_json[id] else None

    def parse_item(self, item):
        key_price = item["itemName"]
        item_id = self._get_item_id(key_price)
        item_price = float(item["price"])
        item_link = f'https://www.haloskins.com/market/{item_id}?id={item["id"]}'
        asset_info = item.get("assetInfo", {})

        stickers_keys = [sticker["enName"] for sticker in asset_info.get("stickers", [])]
        stickers_wears = [sticker.get("wear") for sticker in asset_info.get("stickers", [])]
        item_float = asset_info.get("wear")

        item_in_game_link = None  # Default to None if key is missing
        pattern_template = asset_info.get("paintSeed")

        is_buy_type_fixed = 'fixed'

        return key_price, item_price, item_link, stickers_keys, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed

    def do_request(self, type, name, is_stattrak, max_price, page_number = 0):
        try:
            self._check_if_dict_id_exists(type, is_stattrak, max_price)
            fullname = self._get_fullname(type, name, is_stattrak)

            item_id = self._get_item_id(fullname)
            if not item_id:
                return []

            # https://api.haloskins.com/steam-trade-center/search/sell/list?itemId=22499&appId=730&limit=10&page=1&sort=2&containSticker=1
            url = f"https://api.haloskins.com/steam-trade-center/search/sell/list?itemId={item_id}&appId=730&limit=500&page={page_number + 1}&sort=0&containSticker=1"
            payload = json.dumps({
                "appId": 730,
                "itemId": item_id,
                "limit": 500,
                "page": page_number + 1,
                "sort": 0,
                "containSticker": 1
            })
            response = requests.request("POST", url, headers={ 'Content-Type': 'application/json' }, data=payload)

            return json.loads(response.text)["data"]["list"]

        except:
            return None

class DmarketHelper(BaseHelper):
    DB_ENUM_NAME = 'dmarket'
    MAX_ITEMS_PER_PAGE = 100
    REQUEST_TIMEOUT = 3

    def __init__(self) -> None:
        self.cursor = None

    def parse_item(self, item):
        key_price = item["title"]
        item_price = float(item["price"]["USD"]) / 100.0
        item_link = f'https://dmarket.com/ingame-items/item-list/csgo-skins?userOfferId={item["extra"]["linkId"]}'
        extra = item.get("extra", {})
        stickers_keys = [sticker["name"] for sticker in extra.get("stickers", [])]
        stickers_wears = [None for _ in extra.get("stickers", [])]
        item_float = extra.get("floatValue")
        item_in_game_link = extra.get("inspectInGame")
        pattern_template = extra.get("paintSeed")


        is_buy_type_fixed = 'fixed'

        return key_price, item_price, item_link, stickers_keys, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed

    def do_request(self, type, name, is_stattrak, max_price, page_number = 0):
        fullname = self._get_fullname(type, name, is_stattrak)
        url = f"https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=personal&orderDir=desc&title={quote(fullname)}&priceFrom=0&priceTo={max_price * 100}&treeFilters=cheapestBySteamAnalyst%5B%5D=true,StickersCombo_CountFrom%5B%5D=1,category_0%5B%5D={'stattrak_tm' if is_stattrak else 'not_stattrak_tm'}&gameId=a8db&types=dmarket&limit=100&currency=USD&platform=browser&isLoggedIn=false{f'&cursor={self.cursor}' if self.cursor else ''}"
        response = requests.request("GET", url)

        try:
            response_json = json.loads(response.text)
            if response_json and len(response_json["objects"]) >= 0:
                self.cursor = response_json["cursor"] if "cursor" in response_json else None 
                return response_json["objects"]

            self.cursor = None
            return None
        except:
            self.cursor = None
            return None

class WhiteMarketHelper(BaseHelper):
    DB_ENUM_NAME = 'white-market'
    MAX_ITEMS_PER_PAGE = 100
    REQUEST_TIMEOUT = 5

    def __init__(self) -> None:
        self.redis_client = RedisClient()
        self.force_update = True
        self.cursor_point = None
        self.cursor = None

    def parse_item(self, item):
        node_json = item["node"]
        key_price = node_json["item"]["description"]["nameHash"]
        market_csgo_item_price = float(node_json["price"]["value"])
        market_csgo_item_link = f'https://white.market/item/{node_json["slug"]}'
        stickers_keys = [sticker.replace("Sticker | ", "") for sticker in node_json["item"]["stickerTitles"]]
        stickers_wears = [None for _ in node_json["item"]["stickerTitles"]]
        item_float = node_json.get('float')
        item_in_game_link = node_json.get('link')
        pattern_template = node_json['item'].get('paintSeed')

        is_buy_type_fixed = 'fixed'

        return key_price, market_csgo_item_price, market_csgo_item_link, stickers_keys, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed

    def get_cursor(self, type, name, is_stattrak):
        if self.cursor_point and self.cursor_point == (type, name, is_stattrak):
            return self.cursor
        else:
            return None

    def save_cursor(self, type, name, is_stattrak, value):
        self.cursor_point = (type, name, is_stattrak)
        self.cursor = value

    def get_cookies(self, type):
        redis_key = f"{type}_white_market_cookies"
        if self.redis_client.exists(redis_key) and not self.force_update:
            logging.info(f"Found cookies in redis for {type}")
            cookies_json = self.redis_client.get(redis_key)
            return json.loads(cookies_json)
        else:
            cookies_json = {
                'i18n': 'eu'
            }
            driver_class = SeleniumDriver()
            driver = driver_class.driver
            driver.delete_all_cookies()
            driver.get("https://white.market")

            try:
                time.sleep(3)  # adjust sleep time if needed
                driver.implicitly_wait(10)
                driver.find_element(By.XPATH, "//button[text()='Accept all']").click()
                logging.info("Button 'accept cookies' clicked successfully.")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            time.sleep(5)

            # Get all cookies
            logging.info("Getting cookies from white.market")
            cookies = driver.get_cookies()

            # Print the cookies
            for cookie in cookies:
                if cookie["name"] not in cookies_json:
                    cookies_json[cookie["name"]] = cookie["value"]

            logging.info("Cookies from white.market: {}".format(cookies_json))
            self.redis_client.set(redis_key, json.dumps(cookies_json), ex=3600)
            self.force_update = False

            return cookies_json


    def do_request(self, type, name, is_stattrak, max_price, page_number = 0):
        url = "https://api.white.market/graphql/api"

        payload = json.dumps({
            "query": "\n  query MarketList($search: MarketProductSearchInput, $forwardPagination: ForwardPaginationInput) {\n    market_list(search: $search, forwardPagination: $forwardPagination) {\n      totalCount\n      pageInfo {\n        hasNextPage\n        endCursor\n      }\n      edges {\n        node {\n          id\n          price {\n            value\n            currency\n          }\n          slug\n          similarQty\n          storeSimilarQty\n          store {\n            slug\n            storeName\n            avatar\n            isStoreNamePublic\n            isTopSeller\n            steamAvatar\n            customAvatar\n          }\n          item {\n            ... on CSGOInventoryItem {\n              link\n              paintSeed\n              paintIndex\n              phase\n              float\n              stickerTitles\n            }\n            isAdditionalDataMissed\n            appId\n            id\n            description {\n              steamPrice {\n                value\n                currency\n              }\n              description\n              icon(width: 90, height: 90)\n              iconLarge(width: 400, height: 300)\n              name\n              nameHash\n              isTradeable\n              ... on CSGOSteamItem {\n                isStatTrak\n                isSouvenir\n                stickerImages\n                short\n                skin\n                collection {\n                  key\n                  value\n                }\n                categoryEnum\n                categoryTitle\n                subcategoryEnum\n                subcategoryTitle\n                rarity {\n                  value\n                  key\n                }\n                exterior {\n                  value\n                  key\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n",
            "variables": {
                "search": {
                    "name": f"{type} | {name}",
                    "sort": {
                        "field": "PRICE",
                        "type": "ASC"
                    },
                    "csgoStatTrak": is_stattrak,
                    "csgoSouvenir": False,
                    "csgoRarityEnum": [],
                    "csgoExteriorEnum": [],
                    "priceFrom": {
                        "value": "0",
                        "currency": "USD"
                    },
                    "priceTo": {
                        "value": f"{max_price}",
                        "currency": "USD"
                    },
                    "csgoStickerNames": [],
                    "csgoStickerNamesOperand": "OR",
                    "csgoItemSkin": None,
                    "distinctValues": False,
                    "csgoStickerTeam": None,
                    "csgoStickerPlayer": None,
                    "csgoStickerTournament": None,
                    "csgoStickerFilm": None,
                    "csgoStickers": True,
                    "nameStrict": False,
                    "csgoFloatFrom": None,
                "csgoFloatTo": None
                },
                "forwardPagination": {
                    "after": self.get_cursor(type, name, is_stattrak),
                    "first": 100
                }
            },
            "operationName": "MarketList"
        })

        headers = {
            'Content-Type': 'application/json',
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            respone_json = json.loads(response.text)
            if respone_json and len(respone_json["data"]["market_list"]["edges"]) >= 0:
                logging.info(f'Current cursor {self.get_cursor(type, name, is_stattrak)}, new {respone_json["data"]["market_list"]["pageInfo"]["endCursor"]}')
                self.save_cursor(type, name, is_stattrak, respone_json["data"]["market_list"]["pageInfo"]["endCursor"])
                return respone_json["data"]["market_list"]["edges"]
            return None
        except Exception as e:
            logging.error(e)
            return None


class SkinbaronHelper(BaseHelper):
    DB_ENUM_NAME = 'skinbaron'
    MAX_ITEMS_PER_PAGE = 61
    REQUEST_TIMEOUT = 5

    def parse_item(self, item):
        key_price = f'{"StatTrak™ " if "statTrakString" in item["singleOffer"] else ""}{item["singleOffer"]["localizedName"]} ({item["singleOffer"]["localizedExteriorName"]})'
        market_csgo_item_price = float(item["singleOffer"]["formattedItemPriceOtherCurrency"][1:])
        market_csgo_item_link = f'https://skinbaron.de{item["offerLink"]}'
        stickers_keys = [sticker["localizedName"].strip() for sticker in item["singleOffer"]["stickers"]] if "stickers" in item["singleOffer"] else []
        stickers_wears = [None for _ in item["singleOffer"]["stickers"]] if "stickers" in item["singleOffer"] else []
        item_float = item.get('singleOffer', {}).get('wearPercent')
        item_in_game_link = item.get('singleOffer', {}).get('inspectLink')
        pattern_template = None

        is_buy_type_fixed = 'fixed'

        return key_price, market_csgo_item_price, market_csgo_item_link, stickers_keys, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed

    def get_item_variant_id(self, type, name):
        try:
            name = f'{type} | {name}'
            url = f"https://skinbaron.de/api/v2/Browsing/QuickSearch?variantName={quote(name)}&appId=730&language=en"
            response = requests.request("GET", url)

            return json.loads(response.text)["variants"][0]["id"]
        except:
            return None

    def do_request(self, type, name, is_stattrak, max_price, page_number = 0):
        variant_id = self.get_item_variant_id(type, name)

        if not variant_id:
            logging.info(f"Failed to get variant_id for {type=} with {name=} {is_stattrak=}")
            return None

        url = f"https://skinbaron.de/api/v2/Browsing/FilterOffers?appId=730&variantId={variant_id}&sort=CF&wf=0&wf=1&wf=2&wf=3&wf=4&language=en&otherCurrency=USD&itemsPerPage=60&page={page_number + 1}&pub={max_price}{'&statTrak=true' if is_stattrak else ''}"

        response = requests.request("GET", url)

        try:
            respone_json = json.loads(response.text)
            if respone_json and len(respone_json["aggregatedMetaOffers"]) >= 0:
                for offer in respone_json["aggregatedMetaOffers"]:
                        if ("statTrakString" in offer["singleOffer"] and not is_stattrak) or \
                            ("statTrakString" not in offer["singleOffer"] and is_stattrak) or "souvenirString" in offer["singleOffer"]:
                            offer["singleOffer"]["stickers"] = []

                return respone_json["aggregatedMetaOffers"]
            return None
        except:
            return None


