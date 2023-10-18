import configparser
import os

config = configparser.ConfigParser()

DBWRITE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(DBWRITE_DIR)

print(DBWRITE_DIR)
print(PROJECT_DIR)

config.read(os.path.join(DBWRITE_DIR, "settings.ini"))

FILE_PATH = config.get("General", "file_path")
MONGO_URI = config.get("General", "mongo_uri")
