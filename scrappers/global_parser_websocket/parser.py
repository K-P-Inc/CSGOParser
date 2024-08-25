import asyncio
import os
import hydra
import logging
import json
import threading

from pathlib import Path
from utils import repo_path, get_weapons_array_by_type, get_stickers_dict, calculate_weapon_real_price, get_weapons_array_by_types
from dotenv import load_dotenv
from omegaconf import DictConfig
from classes import DBClient, RedisClient, create_market_client
from classes.markets import SkinportHelper, BitskinsHelper, CSFloatHelper


def market_factory(market_type):
    if market_type == "skinport":
        return SkinportHelper(), SkinportHelper().WS_LINK
    elif market_type == "bitskins":
        return BitskinsHelper(), BitskinsHelper().WS_LINK
    elif market_type == "csfloat":
        return CSFloatHelper(), ''
    else:
        raise Exception('Unknown market type: {0}'.format(market_type))

def run_action(market, db_client: DBClient, redis_client: RedisClient, message, weapons_type):
    parser_type = 'wss_parser'
    parsed_item = market.parse_item_wss(message)
    if parsed_item != None:
        if 'listed' in parsed_item:
            key_price, item_price, item_link, stickers_keys, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed = parsed_item['listed']

            stickers_dict = get_stickers_dict(db_client, redis_client)
            weapons, weapons_prices = get_weapons_array_by_types(db_client, redis_client, weapons_type, parsed_items=0, with_quality=True)

            if len(stickers_keys) == 0 or key_price not in weapons_prices:
                return

            actually_price = weapons_prices[key_price]["price"]
            weapon_uuid = weapons_prices[key_price]["uuid"]
            matched_stickers = [stickers_dict[key] for key in stickers_keys if key in stickers_dict]

            if item_price == 0 or len(stickers_keys) == 0 or len(matched_stickers) == 0:
                return

            num_stickers = len(set([sticker["name"] for sticker in matched_stickers]))

            stickers_pattern, stickers_overprice, future_profit_percentages_steam, future_profit_percentages_buff = calculate_weapon_real_price(
                item_price, key_price, matched_stickers, stickers_wears, stickers_dict, weapons_prices
            )

            sticker_sum = sum([sticker["price"] for sticker in matched_stickers])
            stickers_names_string = ', '.join([sticker["name"] for sticker in matched_stickers])

            stickers_variants = ['Glitter', 'Holo', 'Foil', 'Gold']
            stickers_distinct_variants = list(set(
                next((value for value in stickers_variants if f'({value.lower()})' in sticker["name"].lower()), "Paper")
                for sticker in matched_stickers
            ))

            if sticker_sum > 5:
                db_client.insert_skins([(
                    market.DB_ENUM_NAME,
                    item_link,
                    sticker_sum, item_price,
                    future_profit_percentages_steam,
                    future_profit_percentages_buff,
                    stickers_overprice,
                    weapon_uuid, stickers_pattern, num_stickers, len(matched_stickers), False,
                    [sticker["id"] for sticker in matched_stickers],
                    stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed, stickers_distinct_variants, parser_type
                )])
                logging.info(
                    f'Found new item:\n\n'
                    f'Link: {item_link}\n'
                    f'Name - price: {key_price} - {item_price:.2f} $\n'
                    f'Steam item price: {actually_price} $\n'
                    f'Found stickers: {stickers_names_string}\n'
                    f'Total stickers price: {sticker_sum:.2f} $, parsed stickers: {len(matched_stickers)}/{len(stickers_keys)}, stickers pattern: {stickers_pattern}\n'
                    f'Stickers overprice: {stickers_overprice} $\n'
                    f'Profit: {future_profit_percentages_steam:.2f} %\n'
                    f'Buff profit: {future_profit_percentages_buff:.2f} %\n\n'
                )
        elif 'sold' in parsed_item:
            logging.info(f'Item was sold {parsed_item["sold"]}')
            db_client.update_skins_as_sold_using_wss(parsed_item["sold"])


@hydra.main(config_path=str((Path(repo_path()) / 'conf').resolve()), config_name=f'global_parser_ws')
def main(cfg: DictConfig):
    db_client = DBClient()
    redis_client = RedisClient()

    market_types = os.environ.get("WS_MARKET_TYPES").split(",")

    def run_thread(market_type):
        market, wss_route = market_factory(market_type)

        client = create_market_client(
            market_type=market_type,
            on_message=lambda message: run_action(market, db_client, redis_client, message, cfg.weapons),
            wss_route=wss_route
        )
        client.run()

    for market_type in market_types:
        thread = threading.Thread(target=run_thread, args=(market_type,), name=market_type)
        thread.start()

if __name__ == "__main__":
    load_dotenv()
    main()
