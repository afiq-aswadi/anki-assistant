from aqt import mw
import os 
from os.path import dirname, abspath, realpath
import importlib

from aqt import mw


CURRENT_DIR = dirname(abspath(realpath(__file__)))

def get_config():
    return mw.addonManager.getConfig(__name__)

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

