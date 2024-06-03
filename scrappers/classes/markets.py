import requests
import json
import time
import logging
from urllib.parse import quote, urlencode

class SkinbidHelper:
    DB_ENUM_NAME = 'skinbid'
    MAX_ITEMS_PER_PAGE = 120
    REQUEST_TIMEOUT = 3

    def parse_item(self, item):
        item_json = item["items"][0]["item"]
        key_price = item_json["fullName"]
        item_price = float(item["auction"]["startBid"])
        item_link = f'https://skinbid.com/market/{item["auction"]["auctionHash"]}'
        stickers_keys = [sticker["name"] for sticker in item_json["stickers"]]

        return key_price, item_price, item_link, stickers_keys

    def do_request(self, type, name, is_stattrak, max_price, page_number = 0):
        url = f"https://api.skinbid.com/api/search/auctions?take=120&sort=discount%23desc&goodDeals=false&popular=false&currency=USD&name={quote(name)}&type={type}&Category=Stickers%23true,Souvenir%23false,{'StatTrak%23false' if is_stattrak == False else 'StatTrak%23true'}&skip={self.MAX_ITEMS_PER_PAGE * page_number}"
        response = requests.request("GET", url, headers={}, data={})

        try:
            if json.loads(response.text) and len(json.loads(response.text)["items"]) >= 0:
                return json.loads(response.text)["items"]
            return None
        except:
            return None


class CSMoneyHelper:
    DB_ENUM_NAME = 'cs-money'
    MAX_ITEMS_PER_PAGE = 60
    REQUEST_TIMEOUT = 3

    def parse_item(self, item):
        item_json = item["asset"]
        key_price = item_json["names"]["full"]
        item_price = float(item["pricing"]["computed"])
        item_link = f'https://cs.money/market/buy&unique_id={item["id"]}'
        stickers_keys = [sticker["name"].replace("Sticker | ", "") for sticker in item["stickers"] if sticker] if "stickers" in item else []

        return key_price, item_price, item_link, stickers_keys

    def do_request(self, type, name, is_stattrak, max_price, page_number = 0):
        url = f"https://cs.money/1.0/market/sell-orders?isStatTrak={'true' if is_stattrak else 'false'}&order=asc&sort=price&isSouvenir=false&hasStickers=true&limit={self.MAX_ITEMS_PER_PAGE}&name={quote(type)}%20%7C%20{quote(name)}&offset={page_number * self.MAX_ITEMS_PER_PAGE}&maxPrice={max_price}"
        response = requests.request("GET", url, headers={}, data={})
        try:
            if json.loads(response.text) and len(json.loads(response.text)["items"]) >= 0:
                return json.loads(response.text)["items"]
            return None
        except:
            time.sleep(5)
            return None


class MarketCSGOHelper:
    DB_ENUM_NAME = 'market-csgo'
    MAX_ITEMS_PER_PAGE = 400
    REQUEST_TIMEOUT = 5

    def parse_item(self, item):
        key_price = item["market_hash_name"]
        market_csgo_item_price = float(item["price"])
        market_csgo_item_link = f'https://market.csgo.com/en/{quote(item["seo"]["category"])}/{item["seo"]["type"]}/{quote(key_price)}?id={item["id"]}'
        stickers_keys = [sticker["name"] for sticker in item["stickers"]]

        return key_price, market_csgo_item_price, market_csgo_item_link, stickers_keys

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
