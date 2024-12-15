import json
from aqt import mw
import os 
from os.path import dirname, abspath, realpath
import importlib

from aqt import mw


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

def get_note_query(note): ## gets query from the note
    field_names = mw.col.models.fieldNames(note.model())

    query_field = field_names.index(get_config()["query_field"])
    return note.fields[query_field]

def report(text):
    if importlib.util.find_spec("aqt"):
        from aqt.utils import showWarning

        showWarning(text, title="Anki Image Search v2 Addon")
    else:
        print(text)



