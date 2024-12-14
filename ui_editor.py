## add button to call api
from aqt import mw
from anki.hooks import addHook

from . import utils
from . import api_call

from .tab_interface import ExampleDialog, CustomInstructionDialog

import re

def format_for_anki(text: str) -> str:
    """Format text for Anki with proper HTML"""
    # Convert code blocks
    text = re.sub(
        r'```(\w+)?\n(.*?)\n```',
        lambda m: f'<pre><code>{m.group(2)}</code></pre>',
        text,
        flags=re.DOTALL
    )
    
    # Preserve line breaks and indentation
    text = text.replace('\n', '<br>')
    text = text.replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')
    
    return text



def add_example(editor):
    # Get initial suggestions from Claude
    example_text1, example_text2 = api_call.get_suggestions_from_claude(
        'example',
        "",
        editor.note.fields[0], 
        editor.note.fields[1]
    )

    # Create and show dialog
    dialog = ExampleDialog(parent=editor.parentWindow, 
                            text1=example_text1,
                            text2=example_text2,
                            editor=editor)
    if dialog.exec():
        editor.note.fields[0] = format_for_anki(dialog.text1)
        editor.note.fields[1] = format_for_anki(dialog.text2)
        editor.loadNote()

def add_explanation(editor):
    example_text1, example_text2 = api_call.get_suggestions_from_claude(
    'explanation',
    "",
    editor.note.fields[0], 
    editor.note.fields[1]
)
    dialog = ExampleDialog(parent=editor.parentWindow, 
                            text1=example_text1,
                            text2=example_text2,
                            editor=editor)
    if dialog.exec():
        editor.note.fields[0] = format_for_anki(dialog.text1)
        editor.note.fields[1] = format_for_anki(dialog.text2)
        editor.loadNote()


def custom_instruction(editor):
    # Show custom instruction dialog
    instruction_dialog = CustomInstructionDialog(editor.parentWindow)
    if instruction_dialog.exec():
        # Get suggestions using custom prompt
        example_text1, example_text2 = api_call.get_suggestions_from_claude(
            'instruction',
            instruction_dialog.prompt,
            editor.note.fields[0], 
            editor.note.fields[1]
        )
        
        # Show results in example dialog
        dialog = ExampleDialog(parent=editor.parentWindow, 
                             text1=example_text1,
                             text2=example_text2,
                             editor=editor)
        if dialog.exec():
            editor.note.fields[0] = format_for_anki(dialog.text1)
            editor.note.fields[1] = format_for_anki(dialog.text2)
            editor.loadNote()
    


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
