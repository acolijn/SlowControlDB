import os
from datetime import datetime
from dbwriter.settings import FILE_PATH

class DataFileReader:
    """Reads the latest data from the data file."""

    BASE_DIR = FILE_PATH
    HEADERS_DIR = os.path.join(BASE_DIR, "SC_LOG_HEADERS")
    DATA_DIR = os.path.join(BASE_DIR, "SC_LOG")

    def __init__(self):
        self.header = self._parse_header()

    def _latest_file(self, directory):
        """Returns the path to the latest file in the given directory."""	
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            return None
        # Sort files by modification date
        files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)), reverse=True)
        return os.path.join(directory, files[0])

    def _parse_header(self):
        """Returns the header as a list of strings."""	
        header_file = self._latest_file(self.HEADERS_DIR)
        if not header_file:
            raise Exception("No header file found!")
        with open(header_file, 'r') as file:
            header_line = file.readline()
            #return header_line.strip().split('\t')
            #return [key.replace(" ", "") for key in header_line.strip().split('\t')]
            return [key.replace(" ", "").replace("(", "_").replace(")", "") for key in header_line.strip().split('\t')]



    def read_last_line_as_entry(self):
        """Returns the latest data as a DataEntry object."""	
        data_file = self._latest_file(self.DATA_DIR)
        if not data_file:
            raise Exception("No data file found!")
        with open(data_file, 'r') as file:
            last_line = file.readlines()[-1]
            return self._parse_data_line(last_line)

    def _parse_data_line(self, data_line):
        """Returns the data as a DataEntry object."""
        values = data_line.strip().split('\t')
        data_dict = dict(zip(self.header, values))
        return DataEntry(**data_dict)

class DataEntry:
    """Represents a data entry."""	
    def __init__(self, **kwargs):
        # If "Time" is in kwargs and it's a string, convert it
        if 'Time' in kwargs and isinstance(kwargs['Time'], str):
            timestamp = self._convert_to_datetime(kwargs.pop('Time'))
            if timestamp:
                kwargs['timestamp'] = timestamp
            else:
                # Handle the conversion failure as you see fit
                pass
        
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_keys(self):
        return list(self.__dict__.keys())
    
    def get_dict(self):
        return self.__dict__
    
    @staticmethod
    def _convert_to_datetime(timestamp_str):
        try:
            return datetime.strptime(timestamp_str, "%d-%m-%Y %H:%M:%S")
        except ValueError:
            # Handle incorrect formats or any other issues gracefully
            return None


