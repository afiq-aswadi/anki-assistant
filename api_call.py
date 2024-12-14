import sys
import os

addon_dir = os.path.dirname(__file__)
libs_dir = os.path.join(addon_dir, "libs")
if libs_dir not in sys.path:
    sys.path.insert(0, libs_dir)

import anthropic

from .prompts import get_full_prompt

def get_suggestions_from_claude(prompt_type: str, prompt:str,  current_text1: str, current_text2: str) -> tuple[str, str]:
    try:
        client = anthropic.Anthropic(api_key="REDACTED_API_KEY")
        
        system_prompt = f"""
        {get_full_prompt(prompt_type)}
        
        User instructions: "Also" + {prompt} + ". The card is the following:"

        Current content:
        Base Question and answer: {current_text1}
        Explanation : {current_text2}
        
        Return the suggested question and the answer as one field. With the answer wrapped around {{c1::clozed deletions}}. Afterwards, write a brief explanation of the card. Separate the question and the explanation using a ||| (triple pipe).
        Format: Question, {{c1:: answer }} ||| explanation
        """
        
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.7,
            system=system_prompt,
            messages=[{"role": "user", "content": "Please provide improved suggestions."}]
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