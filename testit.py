import time
from dbwriter.data_file_reader import DataFileReader
from dbwriter.mongo_db_handler import MongoDBHandler
from dbwriter.settings import MONGO_URI, data_element_names

print("Initializing MongoDB...")
mongo_handler = MongoDBHandler(uri=MONGO_URI, collection_name="slow_control_data")
print("Initializing DataFileReader...")
reader = DataFileReader(header=data_element_names)

print("Starting loop...")
for i in range(120):
    print(f"Loop {i}")
    # Read the latest data from the data file:
    latest_data = reader.read_entry()
    # MongoDB writing
    mongo_handler.store(latest_data)
    # MongoDB cleanup
    mongo_handler.delete_old_entries()

    # Sleep for 60 seconds (1 minute)
    time.sleep(60)

# If you ever break out of the loop, close the MongoDB connection
mongo_handler.close()

