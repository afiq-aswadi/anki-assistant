import sys
import os


addon_dir = os.path.dirname(__file__)
libs_dir = os.path.join(addon_dir, "libs")
if libs_dir not in sys.path:
    sys.path.insert(0, libs_dir)

import anthropic
from dotenv import load_dotenv

from .prompts import get_system_prompt, get_user_prompt

def get_suggestions_from_claude(prompt_type: str, custom_prompt:str,  current_text1: str, current_text2: str) -> tuple[str, str]:
    try:
        load_dotenv()
        client = anthropic.Anthropic(api_key=os.getenv("API_KEY")) # define API_KEY as an env variable.
        
        message = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1000,
            temperature=0.4,
            system=get_system_prompt(),
            messages=[{"role": "user",
                        "content": f"""
                {get_user_prompt(prompt_type, custom_prompt)}
                
                Current flashcard:
                Question/Answer: {current_text1}
                Explanation: {current_text2}
                
                Please improve this flashcard following the format requirements.
                """
            }]
        )
        
        # Extract content from message response
        content = message.content[0].text
        suggestions = content.split("|||")
        
        if len(suggestions) == 2:
            return suggestions[0].strip(), suggestions[1].strip()
        else:
            return "API Error: Invalid format", "Please try again"
            
    except Exception as e:
        return f"API Error: {str(e)}", "Please try again"