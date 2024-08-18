
import hydra
import logging

from pathlib import Path
from utils import repo_path

from classes import WSClient, DBClient, RedisClient

from classes.markets import SkinportHelper, BitskinsHelper, CSFloatHelper


def market_factory(market_type):
    if market_type == "skinport":
        return SkinportHelper(), "wss://skinport.com/socket.io/?EIO=4&transport=websocket"
    elif market_type == "bitskins":
        return BitskinsHelper(), ''
    elif market_type == "csfloat":
        return CSFloatHelper(), ''
    else:
        raise Exception('Unknown market type: {0}'.format(market_type))

def run_action(market, message):
    item_listed_marker = '"saleFeed",{"eventType":"listed"'
    item_sold_marker = '"saleFeed",{"eventType":"sold"'

    db_client = DBClient()

    parsed_item = market.parse_item_wss(message)

    if parsed_item != None:
        if item_listed_marker in message:
            db_client.insert_skins(parsed_item)

        elif item_sold_marker in message:
            print(parsed_item)
            # db_client.update_skins_as_sold(parsed_item)


@hydra.main(config_path=str((Path(repo_path()) / 'conf').resolve()), config_name=f'global_parser_ws')
def main():
    market, wss_route = market_factory('skinport')

    client = WSClient(
        on_message=lambda ws, message: run_action(market, message),
        wss_route=wss_route
    )
    client.run()


if __name__ == "__main__":
    main()
