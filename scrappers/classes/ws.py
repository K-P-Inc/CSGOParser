import socketio
import websocket
import logging
import json
import threading

# Socket.IO Client for markets using Socket.IO
class SocketIOBaseClass:
    def __init__(self, **kwargs):
        self.sio = socketio.Client()

        self.locale = kwargs.get('locale', 'en')
        logging.debug(self.locale)
        self.game_id = kwargs.get('game_id', 730)
        logging.debug(self.game_id)
        self.currency = kwargs.get('currency', 'USD')
        logging.debug(self.currency)
        self.wss_route = kwargs.get('wss_route')
        logging.debug(self.wss_route)
        self.market_type = kwargs.get('market_type')
        logging.debug(self.market_type)
        self.on_message_param = kwargs.get('on_message')
        logging.debug(self.on_message_param)

        self.emit_message = kwargs.get('emit_message')

        # Attach event handlers
        self.sio.on('connect', self.on_connect)
        self.sio.on('saleFeed', self.on_message)
        self.sio.on('connect_error', self.on_error)
        self.sio.on('disconnect', self.on_disconnect)

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
        logging.info("Preparing to join market sale feed")
        try:
            self.emit_message()
            logging.info("Initial message sent successfully")
        except Exception as e:
            logging.error(f"Failed to send initial message: {e}")

    def reconnect(self):
        threading.current_thread().name = self.market_type
        logging.info("Reconnecting...")
        if self.sio.connected:
            logging.info("Client is still connected, disconnecting first...")
            self.sio.disconnect()
        self.connect()

    def connect(self):
        threading.current_thread().name = self.market_type
        try:
            logging.info("Connecting...")
            self.sio.connect(self.wss_route, transports=['websocket'])
            logging.info("Connect successful")
        except socketio.exceptions.ConnectionError as e:
            logging.error(f"Connection error: {e}")

    def run(self):
        self.connect()
        self.sio.wait()

class SkinportWSSHelper(SocketIOBaseClass):
    def __init__(self, **kwargs):
        emit_message = lambda: self.sio.emit('saleFeedJoin', {
            "appid": self.game_id,
            "currency": self.currency,
            "locale": self.locale
        })

        # Initialize the base class with the emit_message function
        super().__init__(emit_message=emit_message, **kwargs)

class WaxpeerWSSHelper(SocketIOBaseClass):
    # https://docs.waxpeer.com/?method=socketio
    def __init__(self, **kwargs):
        pass
        # emit_message = lambda: self.sio.emit('subscribed', {
        #     "event": "new",
        #     "game": "csgo"
        # })

        # # Initialize the base class with the emit_message function
        # super().__init__(emit_message=emit_message, **kwargs)

class MarketCSGOWSSHelper():
    # https://market.csgo.com/en/api/content/start#ws
    def __init__(self, **kwargs):
        pass

class WebsocketBaseClass:
    def __init__(self, **kwargs):
        self.ws = kwargs.get('ws', None)
        logging.debug(self.ws)
        self.game_id = kwargs.get('game_id', 730)
        logging.debug(self.game_id)
        self.wss_route = kwargs.get('wss_route')
        logging.debug(self.wss_route)
        self.market_type = kwargs.get('market_type')
        logging.debug(self.market_type)
        self.on_message_param = kwargs.get('on_message')
        logging.debug(self.on_message_param)

        self.subscribe_to_channels = kwargs.get('subscribe_to_channels')

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

    def socket_send(self, action, data):
        self.ws.send(json.dumps([action, data]))

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

class BitskinsWSSHelper(WebsocketBaseClass):
    def __init__(self, **kwargs):
        self.wss_key = "0cf7612993146e47996a14cbd4e439d877af46360625b23798e6757f5c3765dc"

        subscribe_to_channels = self.subscribe_to_channels

        super().__init__(
            subscribe_to_channels=subscribe_to_channels,
            **kwargs
        )

    def on_open(self, ws):
        logging.info("Connection opened, sending authentication...")
        self.socket_send("WS_AUTH_APIKEY", self.wss_key)

    def subscribe_to_channels(self):
        # Subscribe to the desired channels after successful authentication
        self.socket_send("WS_SUB", "listed")
        self.socket_send("WS_SUB", "price_changed")
        self.socket_send("WS_SUB", "delisted_or_sold")
        # self.socket_send("WS_SUB", "extra_info")

# Factory function to create client instances based on market type
def create_market_client(market_type, on_message, wss_route, **kwargs):
    if market_type == 'skinport':
        return SkinportWSSHelper(
            market_type = market_type,
            on_message = on_message,
            wss_route = wss_route,
            **kwargs)
    elif market_type == 'bitskins':
        return BitskinsWSSHelper(
            market_type = market_type,
            on_message = on_message,
            wss_route = wss_route,
            **kwargs)
    elif market_type == 'waxpeer':
        return WaxpeerWSSHelper(
            market_type = market_type,
            on_message = on_message,
            wss_route = wss_route,
            **kwargs)
    elif market_type == 'market-csgo':
        return MarketCSGOWSSHelper(
            market_type = market_type,
            on_message = on_message,
            wss_route = wss_route,
            **kwargs)
    else:
        raise ValueError(f"Unknown market type: {market_type}")

# WEAPON_TYPE="AK-47" MARKET_TYPES="skinport" python3 -m global_parser_websocket.parser hydra.job_logging.root.level=DEBUG
