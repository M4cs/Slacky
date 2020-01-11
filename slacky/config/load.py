import json, os

def load_config(cp):
    if not os.path.exists(cp):
        return None
    with open(cp, 'rb') as config_file:
        config = json.load(config_file)
    return config