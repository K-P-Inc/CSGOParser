import socketio
import websocket
import logging
import json
import threading

# Socket.IO Client for markets using Socket.IO
class SocketMarketClient:
    def __init__(self, market_type, on_message, wss_route, currency='USD', game_id=730, locale='en'):
        self.sio = socketio.Client()
        self.currency = currency
        self.wss_route = wss_route
        self.market_type = market_type
        self.game_id = game_id
        self.locale = locale
        self.on_message_param = on_message

        # Attach event handlers
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('connect_error', self.on_error)
        self.sio.on('saleFeed', self.on_message)

    def on_connect(self):
        threading.current_thread().name = self.market_type
        logging.info("Connected to the server")
        self.send_initial_message()

    def on_disconnect(self):
        threading.current_thread().name = self.market_type
        logging.info("Disconnected from the server")
        self.reconnect()

    def on_error(self, error):
        threading.current_thread().name = self.market_type
        logging.error(f"Connection error: {error}")

    def on_message(self, result):
        threading.current_thread().name = self.market_type
        logging.debug(f"Message received: {result}")
        self.on_message_param(result)

    def send_initial_message(self):
        threading.current_thread().name = self.market_type
        logging.info("Joining market sale feed")
        self.sio.emit('saleFeedJoin', {
            "appid": self.game_id,
            "currency": self.currency,
            "locale": self.locale
        })

    def reconnect(self):
        threading.current_thread().name = self.market_type
        logging.info("Reconnecting...")
        self.connect()

    def connect(self):
        self.sio.connect(self.wss_route, transports=['websocket'])

    def run(self):
        self.connect()
        self.sio.wait()

class WebSocketMarketClient:
    def __init__(self, market_type, on_message, wss_route, game_id=730):
        self.wss_route = wss_route
        self.market_type = market_type
        self.game_id = game_id
        self.on_message_param = on_message
        self.ws = None

    def on_message(self, ws, message):
        logging.debug(f"Message received: {message}")
        action, data = json.loads(message)

        # Handle the action and data
        if action and action.startswith("WS_AUTH"):
            logging.info("Authenticated successfully, subscribing to channels...")
            self.subscribe_to_channels()

        # Pass the received message to the external handler
        self.on_message_param(message)

    def on_error(self, ws, error):
        logging.error(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logging.info("Connection closed, attempting to reconnect...")
        self.reconnect()

    def on_open(self, ws):
        logging.info("Connection opened, sending authentication...")
        self.socket_send("WS_AUTH_APIKEY", "0cf7612993146e47996a14cbd4e439d877af46360625b23798e6757f5c3765dc")

    def socket_send(self, action, data):
        self.ws.send(json.dumps([action, data]))

    def subscribe_to_channels(self):
        # Subscribe to the desired channels after successful authentication
        self.socket_send("WS_SUB", "listed")
        self.socket_send("WS_SUB", "price_changed")
        self.socket_send("WS_SUB", "delisted_or_sold")

    def reconnect(self):
        logging.info("Reconnecting...")
        self.connect()

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.wss_route,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        self.ws.run_forever()

    def run(self):
        self.connect()

# Factory function to create client instances based on market type
def create_market_client(market_type, on_message, wss_route, **kwargs):
    if market_type == 'skinport':
        return SocketMarketClient(market_type, on_message, wss_route, **kwargs)
    elif market_type == 'bitskins':
        return WebSocketMarketClient(market_type, on_message, wss_route, **kwargs)
    else:
        raise ValueError(f"Unknown market type: {market_type}")
