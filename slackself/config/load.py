import json, os

def load_config():
    if not os.path.exists('./config.json'):
        return None
    with open('./config.json', 'rb') as config_file:
        config = json.load(config_file)
    return config