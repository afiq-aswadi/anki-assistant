import json
import os 
from os.path import dirname, abspath, realpath


CURRENT_DIR = dirname(abspath(realpath(__file__)))

def get_config():
    try:
        config_path = os.path.join(CURRENT_DIR, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {"api_key": "", "model_id": "claude-3.5-latest", "temperature": 0.4}
    except:
        return {"api_key": "", "model_id": "claude-3.5-latest", "temperature": 0.4}

def save_config(config: dict) -> bool:
    try:
        config_path = os.path.join(CURRENT_DIR, 'config.json')
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {str(e)}")
        return False


def path_to(*args):
    return os.path.join(CURRENT_DIR, *args)

