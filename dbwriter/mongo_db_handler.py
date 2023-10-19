import time
from pymongo import MongoClient
from datetime import datetime, timedelta
import logging

class MongoDBHandler:
    def __init__(self, uri, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client.get_default_database()
        self.collection = self.db[collection_name]
        self.timestamp_new = None

    def store(self, data_entry):
        data_dict = data_entry.get_dict()
        self.timestamp_new = data_dict['timestamp']
        self.collection.insert_one(data_dict)

        logging.info(f"Stored data entry: {data_dict}")

    def delete_old_entries(self):
        cutoff_time = self.timestamp_new - timedelta(hours=24)
        self.collection.delete_many({
            'timestamp': {'$lt': cutoff_time}
        })
        logging.info("Deleted entries older than 24 hours.")

    def close(self):
        self.client.close()