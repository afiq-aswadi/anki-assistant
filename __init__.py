from .ui_editor import init_editor
import os
import sys
from aqt.utils import tooltip


addon_dir = os.path.dirname(__file__)
libs_dir = os.path.join(addon_dir, "libs")
if libs_dir not in sys.path:
    sys.path.insert(0, libs_dir)

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
if api_key:
    tooltip("API_KEY loaded successfully!")
else:
    tooltip("API_KEY is not set. load_dotenv() may not have run or the .env file is missing this key.")


init_editor()



