# Anki Copilot - Tool to Enhance Your Flashcards!
#TODO: add illustrations.

Anki Copilot is an addon for Anki that enhances your flashcards by making AI-powered improvements to your cards. The addon uses the Claude API to provide suggestions for your cards. The suggestions are based on the content of your cards and the settings you choose.

The addon is *not* intended to independently create cards for you. It is meant to be used as a tool to help you improve your cards and thus make your study sessions more efficient. 

## Features

- **Add explanations**: Add explanations to cards that may be ambiguous or unclear.
- **Add examples**: Add examples to cards that may be difficult to understand.
- **Add related cards**: Add related cards to cards that may have missing context.
- **Custom suggestions**: Provide a prompt to the AI to generate custom suggestions based on your needs.


## Installation

1. Clone the repository into your addons folder:
   - Windows: `%APPDATA%\Anki2\addons21`
   - Mac: `~/Library/Application Support/Anki2/addons21`
   - Linux: `~/.local/share/Anki2/addons21`
2. Open Anki and navigate to `Tools` > `Anki-copilot`.
3. Add your Claude API Key and choose your desired settings.

## Usage

1. Open Anki and start a review session.
2. When you encounter a card that you would like to improve, click the edit button.
3. Click the relevant buttons in the edit menu to access the addon features.
4. Choose to accept, reject, or make further suggestions to the AI.

## Notes

- The addon outputs suggestions in markdown format. Use the Markdown and Katex support addon (https://ankiweb.net/shared/info/1087328706) to render the cards correctly. 
- The addon outputs suggestions in cloze format. You can modify this by changing the prompt in prompts.py.
- The output format is question,{{c1::answer}} ||| explanation. You can modify this by changing the prompt in prompts.py.


## Acknowledgements

Special thanks to the Anki community for their continuous support and feedback. Some code borrowed from https://ankiweb.net/shared/info/432495333. Prompt was modified from Anki-GPT: https://github.com/JoeRonaldson/Anki-GPT. Button icons from <a target="_blank" href="https://icons8.com/icon/117567/example">Example</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>.


## Disclaimer

This addon was intended for personal use. I don't plan on maintaining it, but feel free to fork it and make your own changes! 
