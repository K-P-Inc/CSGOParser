import os
import hydra
import logging

from pathlib import Path
from utils import repo_path

from classes import WSClient, DBClient, RedisClient

from classes.markets import SkinportHelper, BitskinsHelper, CSFloatHelper


def market_factory(market_type):
    if market_type == "skinport":
        return SkinportHelper(), SkinportHelper().WS_LINK
    elif market_type == "bitskins":
        return BitskinsHelper(), ''
    elif market_type == "csfloat":
        return CSFloatHelper(), ''
    else:
        raise Exception('Unknown market type: {0}'.format(market_type))

def run_action(market, message, weapon_type):
    db_client = DBClient()

    parsed_item = market.parse_item_wss(message, weapon_type)

    if parsed_item != None:
        if 'listed' in parsed_item:
            db_client.insert_skins(parsed_item['listed'])
        elif 'sold' in parsed_item:
            db_client.update_skins_as_sold_using_wss(parsed_item['sold'])


@hydra.main(config_path=str((Path(repo_path()) / 'conf').resolve()), config_name=f'global_parser_ws')
def main():
    market_types = os.environ.get("WS_MARKET_TYPES").split(",")
    weapon_type = os.environ.get("WEAPON_TYPE")

    market, wss_route = market_factory(market_types)

    client = WSClient(
        on_message=lambda ws, message: run_action(market, message, weapon_type),
        wss_route=wss_route
    )
    client.run()


if __name__ == "__main__":
    main()
