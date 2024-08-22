import websocket
import threading
import logging
import json
import time

class WSClient:
    def __init__(self, on_message, wss_route, market, currency='USD', game_id=730, locale='en'):
        websocket.enableTrace(False)  # Disable websocket logs
        self.currency = currency
        self.on_message = on_message
        self.wss_route = wss_route
        self.game_id = game_id
        self.locale = locale
        self.market = market
        self.ws = None

    def on_error(self, ws, error):
        logging.error(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logging.info("Connection closed, attempting to reconnect...")
        self.reconnect()

    def on_open(self, ws):
        logging.info(f"Connection opened to market: {self.market}")
        # Sending initial handshake and authentication
        if self.market == 'bitskins':
            self.socket_send(ws, "WS_AUTH_APIKEY", '0cf7612993146e47996a14cbd4e439d877af46360625b23798e6757f5c3765dc')
        elif self.market == 'skinport':
            ws.send("40")
        timer = threading.Timer(1, self.send_initial_message, [ws])
        timer.start()

    def send_initial_message(self, ws):
        if self.market == 'bitskins':
            ws.send(json.dumps(["WS_SUB", "listed"]))
            ws.send(json.dumps(["WS_SUB", "price_changed"]))
            ws.send(json.dumps(['WS_SUB', 'delisted_or_sold']))
        elif self.market == 'skinport':
            ws.send(f'42["saleFeedJoin",{{"appid":{self.game_id},"currency":"{self.currency}","locale":"{self.locale}"}}]')

    def reconnect(self):
        logging.info("Reconnecting...")
        self.connect()

    def socket_send(self, ws, action, data):
        ws.send(json.dumps([action, data]))

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.wss_route,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.on_open = self.on_open
        self.ws.run_forever(ping_interval=30, ping_timeout=10)

    def run(self):
        self.connect()
