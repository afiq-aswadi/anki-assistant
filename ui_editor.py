## add button to call api
from aqt import mw
from anki.hooks import addHook

from . import utils
from . import api_call

from .tab_interface import ExampleDialog

import sys


# def add_example(editor):
#     # Get the collection and note type from current note
#     col = editor.mw.col
#     model = editor.note.model()
    
#     # Create a new note
#     new_note = col.new_note(model)
    
#     # Set the test string
#     test_str = "anthropic is imported." if "anthropic" in sys.modules else "anthropic is not imported."
#     new_note.fields[1] = test_str
    
#     # Get default deck id (usually 1 for Default deck)
#     default_deck_id = col.decks.get_current_id()
    
#     try:
#         # Add the note to collection using default deck
#         col.add_note(new_note, default_deck_id)
        
#         # Open the new note in a new tab
#         editor.mw.onAddCard()
        
#         # Focus the new editor and load our note
#         new_editor = editor.mw.app.activeWindow().editor
#         new_editor.setNote(new_note)
#     except Exception as e:
#         print(f"Error adding note: {str(e)}")

def add_example(editor):
    # Generate example text
    example_text = "anthropic is imported." if "anthropic" in sys.modules else "anthropic is not imported."
    
    # Create and show dialog
    dialog = ExampleDialog(editor.parentWindow, example_text, editor)
    
    if dialog.exec():
        # If accepted, update the original note
        editor.note.fields[1] = example_text
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
