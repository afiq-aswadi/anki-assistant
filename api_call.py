import anthropic

def get_suggestions_from_claude(prompt: str, current_text1: str, current_text2: str) -> tuple[str, str]:
    try:
        client = anthropic.Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")
        
        system_prompt = f"""
        You are helping improve Anki flashcards.
        Current content:
        Field 1: {current_text1}
        Field 2: {current_text2}
        
        User instructions: {prompt}
        
        Return exactly two suggestions, separated by ||| (triple pipe).
        Format: suggestion1|||suggestion2
        """
        
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.7,
            system=system_prompt,
            messages=[{"role": "user", "content": "Please provide improved suggestions."}]
        )
        
        # Split response into two fields
        suggestions = message.content.split("|||")
        if len(suggestions) == 2:
            return suggestions[0].strip(), suggestions[1].strip()
        else:
            return "API Error: Invalid format", "Please try again"
            
    except Exception as e:
        return f"API Error: {str(e)}", "Please try again"