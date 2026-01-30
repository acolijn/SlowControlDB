import time
from pymongo import MongoClient
from datetime import datetime, timedelta
import logging

class MongoDBHandler:
    def __init__(self, uri, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client.get_default_database()
        self.collection = self.db[collection_name]
        self.latest_timestamp = None

    def store(self, data_entry):
        """Stores a data entry in the database.

        Args:
            data_entry (): DataEntry object to store in the database.

        """
        data_dict = data_entry.get_dict()

        # If the latest_timestamp is not set or if the new entry's timestamp 
        # is different from the latest known timestamp, then insert the new entry.
        if not self.latest_timestamp or self.latest_timestamp != data_dict['timestamp']:
            self.collection.insert_one(data_dict)
            logging.info(f"Stored data entry: {data_dict}")
            # Update the latest_timestamp with the timestamp of the new entry.
            self.latest_timestamp = data_dict['timestamp']
        else:
            logging.info(f"Skipped identical data entry: {data_dict}")

    def delete_old_entries(self):
        cutoff_time = self.latest_timestamp - timedelta(hours=168)  # 7 days ago
        self.collection.delete_many({
            'timestamp': {'$lt': cutoff_time}
        })
        logging.info("Deleted entries older than 7 days.")
        
    def close(self):
        self.client.close()