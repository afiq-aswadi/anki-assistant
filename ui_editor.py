## add button to call api
from aqt.utils import tooltip
from anki.hooks import addHook

from . import utils
from . import api_call

from .tab_interface import ExampleDialog, CustomInstructionDialog

def format_for_anki(text: str) -> str:
    """Format text for Anki with proper HTML"""
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
                            editor=editor,
                            prompt_type= 'example')
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
                            editor=editor,
                            prompt_type= 'explanation',)
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
                             editor=editor,
                             prompt_type= 'instruction',
                             initial_prompt= instruction_dialog.prompt)
        if dialog.exec():
            editor.note.fields[0] = format_for_anki(dialog.text1)
            editor.note.fields[1] = format_for_anki(dialog.text2)
            editor.loadNote()
    



def create_related_card(editor):
    # Show prompt dialog
    instruction_dialog = CustomInstructionDialog(editor.parentWindow)
    if instruction_dialog.exec():
        # Get suggestions for new card
        new_text1, new_text2 = api_call.get_suggestions_from_claude(
            'related',
            instruction_dialog.prompt,
            editor.note.fields[0],
            editor.note.fields[1]
        )
        
        # Show preview dialog
        dialog = ExampleDialog(parent=editor.parentWindow, 
                             text1=new_text1,
                             text2=new_text2,
                             editor=editor,
                             prompt_type= 'related',
                             initial_prompt= instruction_dialog.prompt)
        
        if dialog.exec():
            # Create new note only if accepted
            new_note = editor.mw.col.new_note(editor.note.model())
            new_note.fields[0] = dialog.text1
            new_note.fields[1] = dialog.text2
            
            # Add to collection in same deck
            editor.mw.col.add_note(new_note, editor.note.cards()[0].did)
            
            # Show success message
            tooltip("Created new related card!")


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
        (
            "create_related_card",
            create_related_card,
            "Creates a related card based on the current card", ## can make this insert into different fields.
            "related",
        ),
    ]:
        icon_path = utils.path_to("images", "{}.png".format(icon))
        buttons.append(editor.addButton(icon_path,cmd, func, tip = tip))

    return buttons

def init_editor():
    addHook("setupEditorButtons", hook_image_buttons)
