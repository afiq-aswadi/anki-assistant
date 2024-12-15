from .menu_interface import ConfigDialog
from aqt import mw
from aqt.qt import *


def show_config_dialog():
    dialog = ConfigDialog(mw)
    dialog.exec()

def init_menu():
    menu = QMenu("Anki-Copilot", mw)
    config_action = QAction("Settings", mw)
    config_action.triggered.connect(show_config_dialog)
    menu.addAction(config_action)
    
    mw.form.menuTools.addMenu(menu)