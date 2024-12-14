import sys
import os
from .ui_editor import init_editor


addon_dir = os.path.dirname(__file__)
libs_dir = os.path.join(addon_dir, "libs")
if libs_dir not in sys.path:
    sys.path.insert(0, libs_dir)

import anthropic
init_editor()

