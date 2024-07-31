
from classes import WSClient

from classes.markets import SkinportHelper, BitskinsHelper, CSFloatHelper

def market_factory(market_type):
    if market_type == "skinport":
        return SkinportHelper()
    elif market_type == "bitskins":
        return BitskinsHelper()
    elif market_type == "csfloat":
        return CSFloatHelper()
    else:
        raise Exception('Unknown market type: {0}'.format(market_type))


def main():
    market = market_factory('skinport')

    client = WSClient(
        on_message=market.parse_item_wss,
        wss_route="wss://skinport.com/socket.io/?EIO=4&transport=websocket")
    client.run()


if __name__ == "__main__":
    main()
