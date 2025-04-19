import telegram
import os
import logging
from typing import List, Dict, Any
import asyncio
import time
import threading


class NotifyClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(NotifyClient, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        self.bot = telegram.Bot(token="7671055884:AAGoVraXq2146yh8O779wLqp_lJAyNrrglI")
        self.channel_id = "-1002671252215"
        self.message_queue = asyncio.Queue()
        self.messages_sent_times = []  # Track message timestamps
        self.MAX_MESSAGES_PER_MINUTE = 30
        self.consumer_task = None
        self._consumer_loop = None
        self._consumer_thread = None
        self._initialized = True

        logging.debug(f"TELEGRAM_BOT_TOKEN: {os.environ.get('TELEGRAM_BOT_TOKEN')}")
        logging.debug(f"TELEGRAM_CHANNEL_ID: {os.environ.get('TELEGRAM_CHANNEL_ID')}")

        # Start the consumer in a separate thread
        self._start_consumer_thread()

    def _start_consumer_thread(self):
        """Start a dedicated thread for the consumer with its own event loop"""
        if self._consumer_thread is None or not self._consumer_thread.is_alive():
            self._consumer_thread = threading.Thread(target=self._run_consumer_loop, daemon=True)
            self._consumer_thread.start()

    def _run_consumer_loop(self):
        """Run the consumer in its own event loop"""
        try:
            self._consumer_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._consumer_loop)
            self._consumer_loop.run_until_complete(self.message_consumer())
        except Exception as e:
            logging.error(f"Error in consumer loop: {e}")
        finally:
            if self._consumer_loop is not None:
                self._consumer_loop.close()


    def get_thread_id(self, type):
        thread_ids_mapper = {
            "csfloat": 2,
            "cs-money": 3,
            "haloskins": 4,
            "market-csgo": 5,
            "bitskins": 6,
            "skinbid": 7,
            "white-market": 8,
            "skinbaron": 9,
            "gamerpay": 10,
            "waxpeer": 11,
            "dmarket": 12
        }

        return thread_ids_mapper.get(type, "general")

    def get_chat_id(self, thread_id):
        return f"{self.channel_id}_{thread_id}"

    async def wait_for_rate_limit(self):
        """Wait if we've hit the rate limit"""
        current_time = time.time()
        # Remove messages older than 1 minute
        self.messages_sent_times = [t for t in self.messages_sent_times if current_time - t < 60]

        if len(self.messages_sent_times) >= self.MAX_MESSAGES_PER_MINUTE:
            # Wait until the oldest message is more than 1 minute old
            wait_time = 60 - (current_time - self.messages_sent_times[0])
            if wait_time > 0:
                logging.debug(f"Rate limit reached. Waiting {wait_time:.2f} seconds")
                await asyncio.sleep(wait_time)
            self.messages_sent_times = self.messages_sent_times[1:]

    async def message_consumer(self):
        """Consumer that processes messages from the queue"""
        while True:
            try:
                message_data = await self.message_queue.get()
                await self.wait_for_rate_limit()

                try:
                    # If we have an icon URL, send photo with caption
                    if message_data.get("icon_url"):
                        try:
                            logging.info(f"Sending photo: {message_data['icon_url']}")
                            await self.bot.send_photo(
                                chat_id=message_data["chat_id"],
                                photo=message_data["icon_url"],
                                caption=message_data["text"],
                                message_thread_id=message_data["thread_id"],
                                parse_mode='Markdown',
                            )
                        except Exception as e:
                            logging.error(f"Failed to send photo, falling back to text-only message: {e}")
                            await self.bot.send_message(
                                chat_id=message_data["chat_id"],
                                text=message_data["text"],
                                message_thread_id=message_data["thread_id"],
                                parse_mode='Markdown',
                                disable_web_page_preview=True
                            )
                    else:
                        # Fallback to text-only message
                        await self.bot.send_message(
                            chat_id=message_data["chat_id"],
                            text=message_data["text"],
                            message_thread_id=message_data["thread_id"],
                            parse_mode='Markdown',
                            disable_web_page_preview=True
                        )
                    self.messages_sent_times.append(time.time())
                    logging.debug(f"Message sent: {message_data['chat_id']}")
                except Exception as e:
                    logging.error(f"Error sending message: {e}")

                self.message_queue.task_done()
            except Exception as e:
                logging.error(f"Error in message consumer: {e}")
                await asyncio.sleep(1)  # Prevent tight loop in case of persistent errors

    def send_profitable_sticker_notification(
        self,
        market_name: str,
        item_link: str,
        profit_percentage: float,
        sticker_pattern: str,
        stickers_wears: List[float],
        weapon_name: str,
        weapon_quality: str,
        item_price: float,
        sticker_sum: float,
        stickers_names: List[str],
        item_float: float,
        icon_url: str = None
    ) -> None:
        stickers_info = "\n".join([f"   • {name}" for name in stickers_names])
        message_parts = [
            "🎯 *High Profit Sticker Opportunity!*\n\n",
            f"🏪 Market: `{market_name}`\n",
            f"🔫 Weapon: `{weapon_name}`\n",
            f"📊 Quality: `{weapon_quality}` (Float: {item_float:.4f})\n\n",
            f"💰 *Price Details:*\n",
            f"   • Item Price: ${item_price:.2f}\n",
            f"   • Stickers Value: ${sticker_sum:.2f}\n",
            f"   • Profit: {profit_percentage:.2f}%\n\n",
            f"🎨 *Sticker Info:*\n",
            f"   • Pattern: {sticker_pattern}\n",
            f"   • All stickers are fresh (wear = 0)\n",
            f"*Applied Stickers:*\n{stickers_info}\n\n",
            f"🔗 [View Item]({item_link})"
        ]
        message = "".join(message_parts)

        # Create a future in the consumer's event loop and add message to queue
        if self._consumer_loop is not None:
            future = asyncio.run_coroutine_threadsafe(
                self.message_queue.put({
                    "text": message,
                    "timestamp": time.time(),
                    "chat_id": self.get_chat_id(self.get_thread_id(market_name)),
                    "thread_id": self.get_thread_id(market_name),
                    "icon_url": icon_url
                }),
                self._consumer_loop
            )
            future.result()  # Wait for the message to be queued
            logging.debug(f"Message queued. Queue size: {self.message_queue.qsize()}")
        else:
            logging.error("Consumer loop not available. Message not queued.")
