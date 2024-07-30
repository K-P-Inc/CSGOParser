import websocket
import time


class WSClient:
    def __init__(self, on_message):
        self.on_message = on_message
        self.ws = websocket.WebSocketApp(
            "wss://skinport.com/socket.io/?EIO=4&transport=websocket",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")

    def on_open(self, ws):
        print("Connection opened")
        ws.send("40")
        time.sleep(1)
        ws.send('42["saleFeedJoin",{"appid":730,"currency":"USD","locale":"en"}]')

    def run(self):
        self.ws.on_open = self.on_open
        self.ws.run_forever()
