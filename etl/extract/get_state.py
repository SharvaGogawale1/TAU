import json

def get_state(file_path: str) -> dict:
    with open(file_path) as json_file:
        return json.load(json_file)