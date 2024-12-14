from aqt import mw
from aqt.qt import QAction
from aqt.gui_hooks import editor_did_init_buttons
from aqt.utils import showInfo, showWarning
import json
import requests

# Your OpenAI API key
API_KEY = "YOUR_OPENAI_API_KEY"

def improve_card(editor):
    """Send the card's fields to OpenAI's API and update them with the response."""
    note = editor.note
    # Adjust these field names to match your note type fields
    front_field = "Front"
    back_field = "Back"

    front_text = note[front_field]
    back_text = note[back_field]

    if not front_text and not back_text:
        showWarning("No content in the note fields.")
        return

    # Construct the prompt
    prompt = f"""
    You are an assistant that improves Anki cards. 
    The card has a Front and a Back. The Front currently says:
    "{front_text}"

    The Back currently says:
    "{back_text}"

    Please return a JSON with two keys: "front" and "back" containing improved versions of these fields. 
    Make them clear, concise, and factually correct. Example:
    {{
      "front": "Improved front text",
      "back": "Improved back text"
    }}
    """

    # OpenAI Chat Completions API payload
    # Using GPT-4 or GPT-3.5-turbo, adjust as needed
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt.strip()}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            # Extract the content
            improved_content = result["choices"][0]["message"]["content"].strip()
            # Parse the returned JSON
            try:
                improved = json.loads(improved_content)
                # Update the note fields
                note[front_field] = improved.get("front", front_text)
                note[back_field] = improved.get("back", back_text)
                editor.loadNote()
                showInfo("Card improved successfully!")
            except json.JSONDecodeError:
                # If the response isn't valid JSON, place entire response in back field
                note[back_field] = improved_content
                editor.loadNote()
                showWarning("The AI did not return proper JSON. The response was placed in the Back field.")
        else:
            showWarning(f"OpenAI API error: {response.status_code}\n{response.text}")
    except Exception as e:
        showWarning(f"An error occurred: {str(e)}")

def on_editor_init_buttons(editor):
    """Hook to add a custom button to the editor toolbar."""
    # Editor.addButton is available in recent versions of Anki.
    # If not available, you can inject HTML/JS, but this is simpler if supported.
    # The icon is optional, use None or provide a path to an icon.
    editor.addButton(
        icon=None,
        cmd="improve_card",
        label="Improve Card",
        func=lambda ed=editor: improve_card(ed),
        tip="Use AI to improve this card"
    )

editor_did_init_buttons.append(on_editor_init_buttons)
