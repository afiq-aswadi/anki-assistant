from .ui_editor import init_editor
from aqt.utils import tooltip
from . import utils

config = utils.get_config()
api_key = config.get('api_key')
if not api_key:
    tooltip("API Error: No API key configured", "Please set your API key in Tools > Add-ons > Config")
else:
    tooltip("API key configured!")
    

init_editor()



