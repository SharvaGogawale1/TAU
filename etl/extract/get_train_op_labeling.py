import json

def get_labels(_filename: str) -> dict:
    with open(_filename, 'r') as json_file:
        return json.load(json_file)