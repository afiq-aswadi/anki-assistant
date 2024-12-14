## define api call here
from aqt import mw
from aqt.utils import showInfo, showWarning
import json
import requests

API_KEY = "YOUR_OPENAI_API_KEY"

def improve_card(editor):
    note = editor.note
    front_field = "Front"
    back_field = "Back"

    front_text = note[front_field]
    back_text = note[back_field]

    if not front_text and not back_text:
        showWarning("No content in the note fields.")
        return

    prompt = f"""
    You are an assistant that improves Anki cards. 
    The card has a Front and a Back.
    Front: "{front_text}"
    Back: "{back_text}"

    Return a JSON with "front" and "back" keys containing improved text versions.
    Example:
    {{
      "front": "Improved front text",
      "back": "Improved back text"
    }}
    """

    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "gpt-4",  # or gpt-3.5-turbo, etc.
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
            improved_content = result["choices"][0]["message"]["content"].strip()
            try:
                improved = json.loads(improved_content)
                note[front_field] = improved.get("front", front_text)
                note[back_field] = improved.get("back", back_text)
                editor.loadNote()
                showInfo("Card improved successfully!")
            except json.JSONDecodeError:
                note[back_field] = improved_content
                editor.loadNote()
                showWarning("The AI did not return valid JSON. The response was placed in the Back field.")
        else:
            showWarning(f"OpenAI API error: {response.status_code}\n{response.text}")
    except Exception as e:
        showWarning(f"An error occurred: {str(e)}")