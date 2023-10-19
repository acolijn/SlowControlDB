import os
from datetime import datetime
from dbwriter.settings import FILE_PATH

class DataFileReader:
    """Reads the latest data from the data file."""

    BASE_DIR = FILE_PATH
    HEADERS_DIR = os.path.join(BASE_DIR, "SC_LOG_HEADERS")
    DATA_DIR = os.path.join(BASE_DIR, "SC_LOG")

    def __init__(self, header=None):
        if header:
            self.header = header
        else:
            # If no header is given parse header from SC directory
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
            """The header is the last line of the file."""	
            header_line = file.readlines()[-1]
            print(header_line.strip().split('\t'))
            return [key.replace(" ", "").replace("(", "_").replace(")", "") for key in header_line.strip().split('\t')]

    def read_entry(self):
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
        # the value format is a string with the following format: xxxx,yyyyy
        # where xxxx is the integer part and yyyyy is the decimal part
        # we need to convert it to a float
        for i in range(len(values)):
            if "," in values[i]:
                values[i] = float(values[i].replace(",", "."))
                
        print(len(self.header), len(values))

        # if the number of values is not equal to the number of keys in the header. Then I know
        # that the HV data is missing - so either 8 or 16 less elements in teh data. I want to add -999.0 as a placeholder.
        # the entries need to be added just before the last two elements in the list.

        if len(self.header) != len(values):
            print("Missing HV data - adding -999.0 as placeholder")
            n_patch = 0
            if len(self.header) == len(values) + 8:
                # add 8 entries
                n_patch = 8
            elif len(self.header) == len(values) + 16:
                n_patch = 16

            else:
                print("Something is wrong with the data - not adding -999.0 as placeholder")
                # throw an exception
                raise Exception("Missing HV data - not adding -999.0 as placeholder")
            
            # add the values
            for i in range(n_patch):
                values.insert(-2, -999.0)

        data_dict = dict(zip(self.header, values))
        data_dict = {k: v for k, v in data_dict.items() if 'NC' not in k}

        return DataEntry(**data_dict)

class DataEntry:
    """Represents a data entry."""	
    def __init__(self, **kwargs):
        # If "Time" is in kwargs and it's a string, convert it
        if 'timestamp' in kwargs and isinstance(kwargs['timestamp'], str):
            timestamp = self._convert_to_datetime(kwargs.pop('timestamp'))
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


