## add button to call api
from aqt import mw
from anki.hooks import addHook

from . import utils
from . import api_call

from .tab_interface import ExampleDialog

import sys


def add_example(editor):
    # Get initial suggestions from Claude
    example_text1, example_text2 = api_call.get_suggestions_from_claude(
        "Initial suggestions", 
        editor.note.fields[0], 
        editor.note.fields[1]
    )
    
    # Create and show dialog
    dialog = ExampleDialog(parent=editor.parentWindow, 
                         text1=example_text1,
                         text2=example_text2,
                         editor=editor)
    if dialog.exec():
        editor.note.fields[0] = dialog.text1
        editor.note.fields[1] = dialog.text2
        editor.loadNote()

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
