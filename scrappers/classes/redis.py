import redis
import os
import logging

class RedisClient:
    def __init__(self) -> None:
        logging.info("Initializing Redis client.")
        self.r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), password=os.getenv("REDIS_PWD"), decode_responses=True)
        logging.info("Redis client initialized.")

    def set(self, key, value, ex=3600):
        logging.info(f"Setting key: {key} with value: {value}")
        self.r.set(key, value, ex=ex)
        logging.debug(f"Key: {key} set successfully.")

    def get(self, key):
        logging.info(f"Getting value for key: {key}")
        value = self.r.get(key)
        logging.debug(f"Retrieved value for key: {key}: {value}")
        return value

    def hset(self, key, mapping, ex=3600):
        logging.info(f"Setting hash for key: {key} with mapping: {mapping}")
        self.r.hset(key, mapping=mapping)
        logging.debug(f"Hash set for key: {key} with mapping: {mapping}")

    def hgetall(self, key):
        logging.info(f"Getting all hash values for key: {key}")
        hash_values = self.r.hgetall(key)
        logging.debug(f"Retrieved hash values for key: {key}: {hash_values}")
        return hash_values

    def exists(self, key):
        logging.info(f"Checking existence of key: {key}")
        existence = self.r.exists(key)
        logging.debug(f"Key: {key} exists: {existence}")
        return existence

    def __del__(self):
        logging.info("Deleting Redis client instance.")
        if self.r:
            self.r.close()
            logging.info("Redis client connection closed.")