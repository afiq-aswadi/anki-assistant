import sys
import os
from .utils import get_config

addon_dir = os.path.dirname(__file__)
libs_dir = os.path.join(addon_dir, "libs")
if libs_dir not in sys.path:
    sys.path.insert(0, libs_dir)

import anthropic


from .prompts import get_system_prompt, get_user_prompt

def get_suggestions_from_claude(prompt_type: str, custom_prompt:str,  current_text1: str, current_text2: str) -> tuple[str, str]:
    try:
        config = get_config()
        api_key = config.get('api_key')
        if not api_key:
            return "API Error: No API key configured", "Please set your API key in Tools > Add-ons > Config"
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model= config.get('model_id'),
            max_tokens=1000,
            temperature= config.get('temperature'),
            system=get_system_prompt(),
            messages=[{"role": "user",
                        "content": f"""
                {get_user_prompt(prompt_type, custom_prompt)}
                
                The following flashcard needs improvement: 

                Question/Answer: {current_text1}
                Explanation: {current_text2}
                
                Please improve this flashcard following the instructions given.
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