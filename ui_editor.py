## add button to call api
from aqt import mw
from anki.hooks import addHook

from . import utils
from . import api_call

import sys

def add_example(editor):
    #query = utils.get_note_query(editor.note) ##need to set up config for this to work
    str = "test"
    if "anthropic" in sys.modules:
        str = "anthropic is imported."
    else:
        str = "anthropic is not imported."
    editor.note.fields[1] = str
    editor.loadNote()
    #editor.tabs.addTab()

def add_explanation(editor):
    pass


def custom_instruction(editor):
    pass


def hook_image_buttons(buttons, editor):
    for (cmd, func, tip, icon) in [
        (
            "add_example",
            add_example,
            "Adds examples to the card", ## can make this insert into different fields.
         "example",
        ),
        (
            "add_explanation",
            add_explanation,
            "Adds explanations to the card", ## can make this insert into different fields.
         "explanation",
         ),
        (
            "custom_instruction",
            custom_instruction,
            "Adds custom instructions to the card", ## can make this insert into different fields.'
            "instruction",
        ),
    ]:
        icon_path = utils.path_to("images", "{}.png".format(icon))
        buttons.append(editor.addButton(icon_path,cmd, func, tip = tip))
    
    return buttons

def init_editor():
    addHook("setupEditorButtons", hook_image_buttons)
