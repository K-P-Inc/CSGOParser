import websocket
import json
import time

from ws import WSClient

# https://github.com/DrewStewart7/CSGO-Market-Tracker/blob/main/main.py

parser_items = ['AK-47', 'M4A4', 'AWP', 'M4A1-S']
price_rate = 100.0
item_listed_marker = '"saleFeed",{"eventType":"listed"'
item_sold_marker = '"saleFeed",{"eventType":"sold"'


def on_message(ws, main_message):
    if item_listed_marker in main_message or item_sold_marker in main_message:
        message = main_message.replace("42", "", 1)
        message = json.loads(message)
        sales = message[1]["sales"]

        for item in sales:
            key_price = item['marketHashName']
            for i in parser_items:
                if i in key_price:
                    item_price = float(item["salePrice"]) / price_rate
                    item_link = f'https://skinport.com/item/{item["url"]}/{item["saleId"]}'
                    stickers_keys = [sticker["name"] for sticker in item["stickers"]]
                    stickers_wears = [sticker["wear"] if sticker["wear"] is not None else 0 for sticker in item["stickers"]]
                    item_float = item.get('wear')
                    item_in_game_link = item.get('link')
                    pattern_template = item.get('pattern')
                    is_buy_type_fixed = 'fixed'
                    is_stattrack = False

                    if 'StatTrak™ ' in key_price:
                        key_price.replace('StatTrak™ ', '')
                        is_stattrack = True

                    if item_listed_marker in main_message:
                        print(f"Listed: {key_price}, {item_price}, {item_link}, {stickers_keys}, {stickers_wears}, {item_float}, {item_in_game_link}, {pattern_template}, {is_buy_type_fixed}")

                    elif item_sold_marker in main_message:
                        print(f"Sold: {key_price}, {item_price}, {item_link}, {stickers_keys}, {stickers_wears}, {item_float}, {item_in_game_link}, {pattern_template}, {is_buy_type_fixed}")

if __name__ == "__main__":
    while True:
        client = WSClient(on_message)
        client.run()
        time.sleep(1)  # Небольшая задержка перед повторным подключением
