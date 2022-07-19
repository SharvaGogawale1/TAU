import json

def get_labels(_filename: str, _data_to_write: dict) -> dict:
    with open(_filename, 'r') as json_file:
        return json.dump(_data_to_write, json_file)