import configparser
import os

config = configparser.ConfigParser()

DBWRITE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(DBWRITE_DIR)

# dont share this file with anyone
config.read(os.path.join(DBWRITE_DIR, "settings.ini"))

FILE_PATH = config.get("General", "file_path")
MONGO_URI = config.get("General", "mongo_uri")

# The data element names are stored in the settings.ini file as a string
data_element_names_str = config.get("General", "data_element_names")
data_element_names = [name.strip() for name in data_element_names_str[1:-1].split()]

