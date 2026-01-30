import time
import logging
import os
from dbwriter.data_file_reader import DataFileReader
from dbwriter.mongo_db_handler import MongoDBHandler
from dbwriter.settings import MONGO_URI, data_element_names

# Configure logging to both file and console
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'db_writer.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # Also print to console
    ]
)

print("Initializing MongoDB...")
mongo_handler = MongoDBHandler(uri=MONGO_URI, collection_name="slow_control_data")
print("Initializing DataFileReader...")
reader = DataFileReader(header=data_element_names)

# Try initial connection
if not mongo_handler.connect():
    logging.warning("Initial MongoDB connection failed. Will retry on each cycle.")

print("Starting loop...")
while True:
    try:
        # Check if we need to reconnect
        if not mongo_handler.is_connected:
            logging.info("Attempting to reconnect to MongoDB...")
            if not mongo_handler.connect():
                logging.warning("Reconnection failed. Will retry in 60 seconds.")
                time.sleep(60)
                continue

        # Read the latest data from the data file:
        latest_data = reader.read_entry()
        
        # MongoDB writing
        if not mongo_handler.store(latest_data):
            logging.warning("Store operation failed, will retry on next cycle")
        
        # MongoDB cleanup
        mongo_handler.delete_old_entries()

    except KeyboardInterrupt:
        logging.info("Received interrupt signal, shutting down...")
        break
    except Exception as e:
        logging.error(f"Unexpected error in main loop: {e}")
    
    # Sleep for 60 seconds (1 minute)
    time.sleep(60)

# Close the MongoDB connection
mongo_handler.close()
print("Shutdown complete.")

