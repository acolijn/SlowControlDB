from dbwriter.data_file_reader import DataFileReader
# Example usage:

reader = DataFileReader()
latest_data = reader.read_last_line_as_entry()

# Access data:
print(latest_data.timestamp)
print(latest_data.get_keys())