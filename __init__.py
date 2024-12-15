from .ui_editor import init_editor
from .ui_menu import init_menu
from aqt.utils import showInfo
from . import utils

config = utils.get_config()
if not config.get('api_key'):
    showInfo("Please set your API key in Tools > Anki-Copilot > Settings")

init_editor()
init_menu()