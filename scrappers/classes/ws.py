import websocket
import threading
import logging

class WSClient:
    def __init__(self, on_message, wss_route, currency='USD', game_id=730, locale='en'):
        websocket.enableTrace(False) # Websocket logs
        self.currency = currency
        self.on_message = on_message
        self.wss_route = wss_route
        self.game_id = game_id
        self.locale = locale
        self.ws = None

    def on_error(self, ws, error):
        logging.error(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logging.info("Connection closed, attempting to reconnect...")
        self.reconnect()

    def on_open(self, ws):
        logging.info("Connection opened")
        ws.send("40")
        timer = threading.Timer(1, self.send_initial_message, [ws])
        timer.start()

    def send_initial_message(self, ws):
        ws.send(f'42["saleFeedJoin",{{"appid":{self.game_id},"currency":"{self.currency}","locale":"{self.locale}"}}]')

    def reconnect(self):
        logging.info("Reconnecting...")
        self.connect()

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
