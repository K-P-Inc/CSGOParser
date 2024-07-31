
import logging
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
    # TODO: Rework this variables
    item_listed_marker = '"saleFeed",{"eventType":"listed"'
    item_sold_marker = '"saleFeed",{"eventType":"sold"'

    db_client = DBClient()

    parsed_item = market.parse_item_wss(message)
    parsed_urls = parsed_item[2]
    uuids_for_update = ''

    if parsed_item != None:
        # TODO: Listed metric here
        if item_listed_marker in message:
            pass
        # TODO: Sold metric here
        elif item_sold_marker in message:
            db_client.update_skins_as_sold(market.DB_ENUM_NAME, parsed_urls, uuids_for_update)


def main():
    market, wss_route = market_factory('skinport')

    client = WSClient(
        on_message=lambda ws, message: run_action(market, message),
        wss_route=wss_route
    )
    client.run()


if __name__ == "__main__":
    main()
