import time
from pymongo import MongoClient
from datetime import datetime, timedelta
import logging

class MongoDBHandler:
    def __init__(self, uri, dbname, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[dbname]
        self.collection = self.db[collection_name]

    def store(self, data_entry):
        data_dict = data_entry.get_dict()
        # now = datetime.now()
        self.collection.insert_one(data_dict)
        logging.info(f"Stored data - Temperature: {temperature}, Pressure: {pressure}")

    def delete_old_entries(self):
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.collection.delete_many({
            'timestamp': {'$lt': cutoff_time}
        })
        logging.info("Deleted entries older than 24 hours.")

    def close(self):
        self.client.close()