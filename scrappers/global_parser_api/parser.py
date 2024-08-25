import time
import os
import traceback
import logging
import hydra
import threading
from pathlib import Path
from omegaconf import DictConfig
from dotenv import load_dotenv
# from prometheus_client import start_http_server
from classes import DBClient, RedisClient
from utils import repo_path, get_stickers_dict, get_weapons_array_by_type, calculate_weapon_real_price
from classes.markets import SkinbidHelper, CSMoneyHelper, MarketCSGOHelper, SkinportHelper, CSFloatHelper, BitskinsHelper, HaloskinsHelper, DmarketHelper, WhiteMarketHelper, SkinbaronHelper, GamerPayHelper, WaxPeerHelper


def parse_item(
    market_class,
    db_client: DBClient,
    items_list, display_name,
    weapon_config, weapons_prices, stickers_dict
):
    if len(items_list) == 0:
        logging.info(f'No weapons found for {display_name}')
        return []

    found_items = []
    parsed_urls = []
    parser_type = 'api_parser'

    logging.info(f'Parsing weapon {display_name} (found {len(items_list)})')
    for i in items_list:
        key_price, item_price, item_link, stickers_keys, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed = market_class.parse_item(i)
        parsed_urls.append(item_link)

        if len(stickers_keys) == 0 or key_price not in weapons_prices:
            continue

        actually_price = weapons_prices[key_price]["price"]
        weapon_uuid = weapons_prices[key_price]["uuid"]
        matched_stickers = [stickers_dict[key] for key in stickers_keys if key in stickers_dict]

        if item_price == 0 or len(stickers_keys) == 0 or len(matched_stickers) == 0:
            continue

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

        if sticker_sum > weapon_config.sticker_sum:
            found_items.append((
                market_class.DB_ENUM_NAME,
                item_link,
                sticker_sum, item_price,
                future_profit_percentages_steam,
                future_profit_percentages_buff,
                stickers_overprice,
                weapon_uuid, stickers_pattern, num_stickers, len(matched_stickers), False,
                [sticker["id"] for sticker in matched_stickers],
                stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed, stickers_distinct_variants, parser_type
            ))
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

    if found_items:
        db_client.insert_skins(found_items)

    return parsed_urls


def run_action(parsed_items, market_class, weapon_config):
    db_client = DBClient()
    redis_client = RedisClient()
    types = [
        'Factory New',
        'Minimal Wear',
        'Field-Tested',
        'Well-Worn',
        'Battle-Scarred'
    ]

    try:
        weapons, weapons_prices = get_weapons_array_by_type(db_client, redis_client, weapon_config, parsed_items, with_quality=market_class.PARSE_WITH_QUALITY)

        for weapon_type, weapon_name, weapon_is_stattrak in weapons:
            page_number = 0
            items_list = None
            parsed_urls = []
            display_name = f'{"StatTrak™ " if weapon_is_stattrak == True else ""}{weapon_type} | {weapon_name}'
            while (items_list == None and page_number == 0) or (items_list != None and len(items_list) == market_class.MAX_ITEMS_PER_PAGE):
                logging.info(f'Trying to find {display_name} on {page_number + 1} page {market_class.PARSE_WITH_QUALITY}')
                items_list = market_class.do_request(weapon_type, weapon_name, weapon_is_stattrak, weapon_config["max_steam_item_price"], page_number)
                if items_list != None:
                    stickers_dict = get_stickers_dict(db_client, redis_client)
                    _, updated_prices = get_weapons_array_by_type(db_client, redis_client, weapon_config, parsed_items, with_quality=market_class.PARSE_WITH_QUALITY)
                    parsed_urls_iter = parse_item(
                        market_class=market_class,
                        db_client=db_client,
                        items_list=items_list, display_name=display_name,
                        weapon_config=weapon_config, weapons_prices=updated_prices,
                        stickers_dict=stickers_dict
                    )
                    for url in parsed_urls_iter:
                        parsed_urls.append(url)

                    weapons_prices = updated_prices

                if items_list != None and len(items_list) == market_class.MAX_ITEMS_PER_PAGE:
                    page_number += 1

                logging.info(f'Parsed weapon {display_name} on {page_number + 1} page')
                time.sleep(market_class.REQUEST_TIMEOUT)

            if market_class.PARSE_WITH_QUALITY == False:
                uuids_for_update = [
                    weapons_prices[f"{display_name} ({key_price})"]["uuid"]
                    for key_price in types
                    if f"{display_name} ({key_price})" in weapons_prices
                ]
            else:
                uuids_for_update = [weapons_prices[display_name]["uuid"]]

            db_client.update_skins_as_sold(market_class.DB_ENUM_NAME, parsed_urls, uuids_for_update)

            parsed_items += 1
    except KeyboardInterrupt:
        logging.info('Closing parsing process (KeyboardInterrupt)')
    except Exception as e:
        logging.error(f'Got exception: {e}')
        logging.error(traceback.format_exc())
        parsed_items += 1
    finally:
        logging.info('End parsing process')


def market_factory(market_type):
    if market_type == "skinbid":
        return SkinbidHelper()
    elif market_type == "cs-money":
        return CSMoneyHelper()
    elif market_type == "market-csgo":
        return MarketCSGOHelper()
    elif market_type == "skinport":
        return SkinportHelper()
    elif market_type == "csfloat":
        return CSFloatHelper()
    elif market_type == "bitskins":
        return BitskinsHelper()
    elif market_type == "haloskins":
        return HaloskinsHelper()
    elif market_type == "dmarket":
        return DmarketHelper()
    elif market_type == "white-market":
        return WhiteMarketHelper()
    elif market_type == "skinbaron":
        return SkinbaronHelper()
    elif market_type == "gamerpay":
        return GamerPayHelper()
    elif market_type == 'waxpeer':
        return WaxPeerHelper()
    else:
        raise Exception('Unknown market type: {0}'.format(market_type))


@hydra.main(config_path=str((Path(repo_path()) / 'conf').resolve()), config_name=f'global_parser_api')
def main(cfg: DictConfig):
    market_types = os.environ.get("MARKET_TYPES").split(",")
    weapon_type = os.environ.get("WEAPON_TYPE")

    market_classes = {market_type: market_factory(market_type) for market_type in market_types}
    weapon = next((w for w in cfg.weapons if w.type == weapon_type), None)
    threads = {}

    def run_thread(market_class, weapon):
        parsed_items = 0
        while True:
            try:
                run_action(parsed_items, market_class, weapon)
                time.sleep(1)
            except Exception as e:
                print(f"Error in thread {market_class}: {e}")
                break

    while True:
        for market_type, market_class in market_classes.items():
            if market_type not in threads or not threads[market_type].is_alive():
                thread = threading.Thread(target=run_thread, args=(market_class, weapon), name=market_type)
                thread.start()
                threads[market_type] = thread

        # Clean up completed threads to avoid memory leaks
        threads = {mt: t for mt, t in threads.items() if t.is_alive()}

        # Sleep for a while before checking the threads again
        time.sleep(5)


if __name__ == "__main__":
    load_dotenv()
    # start_http_server(8080)
    main()
