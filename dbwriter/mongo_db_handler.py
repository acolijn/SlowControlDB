import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime, timedelta
import logging

class MongoDBHandler:
    def __init__(self, uri, collection_name):
        self.uri = uri
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
        self.latest_timestamp = None
        self.is_connected = False

    def connect(self):
        """Attempts to connect to MongoDB. Returns True if successful, False otherwise."""
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Test the connection
            self.client.admin.command('ping')
            self.db = self.client.get_default_database()
            self.collection = self.db[self.collection_name]
            self.is_connected = True
            logging.info("Successfully connected to MongoDB")
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            self.is_connected = False
            return False
        except Exception as e:
            logging.error(f"Unexpected error connecting to MongoDB: {e}")
            self.is_connected = False
            return False

    def store(self, data_entry):
        """Stores a data entry in the database.

        Args:
            data_entry (): DataEntry object to store in the database.

        Returns:
            bool: True if successful, False if connection issue
        """
        if not self.is_connected:
            logging.warning("Not connected to MongoDB, skipping store operation")
            return False

        try:
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
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logging.error(f"MongoDB connection lost during store: {e}")
            self.is_connected = False
            return False
        except Exception as e:
            logging.error(f"Error storing data: {e}")
            return False

    def delete_old_entries(self):
        if not self.is_connected:
            logging.warning("Not connected to MongoDB, skipping delete operation")
            return False

        try:
            cutoff_time = self.latest_timestamp - timedelta(hours=672)  # 7 days ago
            self.collection.delete_many({
                'timestamp': {'$lt': cutoff_time}
            })
            logging.info("Deleted entries older than 7 days.")
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logging.error(f"MongoDB connection lost during delete: {e}")
            self.is_connected = False
            return False
        except Exception as e:
            logging.error(f"Error deleting old entries: {e}")
            return False
        
    def close(self):
        if self.client:
            try:
                self.client.close()
                logging.info("MongoDB connection closed")
            except Exception as e:
                logging.error(f"Error closing MongoDB connection: {e}")
        self.is_connected = False