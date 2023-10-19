from dbwriter.data_file_reader import DataFileReader
from dbwriter.mongo_db_handler import MongoDBHandler
from dbwriter.settings import MONGO_URI, data_element_names

reader = DataFileReader(header=data_element_names)
latest_data = reader.read_entry()

# Access data:
print(latest_data.timestamp)
print(latest_data.get_keys())
print(latest_data.get_dict())

# MongoDB handling:
print("Storing data in MongoDB...")

#mongo_handler = MongoDBHandler(uri=MONGO_URI, collection_name="slow_control_data")
#mongo_handler.store(latest_data)
#mongo_handler.close()
