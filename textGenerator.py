# Import the os package
import os

# Import the openai package
from openai import OpenAI

# From the IPython.display package, import display and Markdown
from IPython.display import display, Markdown

# Import yfinance as yf
import yfinance as yf


print("start")



def getTextToType(theme, wordsToInclude, targetLength, isCode):
    systemPrompt = "You are in charge of generating text for a typing test. You should follow any themes, and word limits as closely as possible. YOU MUST include all words in the given list of tricky words. Having tricky words show up multiple times is ideal, but the most important thing is that they appear at least once or the user will be severely, emotionally hurt. You should aim to make your output educational on the chosen subject."
    prompt = ""
    if isCode:
        userPrompt = f'Generate {targetLength} words of python code. Your output MUST be code or the user will be very upset! You must include all of the difficult words {wordsToInclude}. If you are missing one of these words, our program will be in serious risk of begin shut down and we will not be able to pay our rent. The code should follow the theme {theme}. Do not write anything other than code. Do not indicate where code starts or ends.'
    else:
        userPrompt = f'Generate n {targetLength} word passage containg all the difficult words {wordsToInclude}. You MUST include every word in {wordsToInclude}.  If you are missing one of these words, our program will be in serious risk of begin shut down and we will not be able to pay our rent. The passage should follow the theme {theme}.'
    
    client = OpenAI(
        api_key= os.environ.get("OPENAI_KEY"),
        base_url="https://hack.funandprofit.ai/api/providers/openai/v1"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or whatever model is supported by your proxy
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": userPrompt}
        ]
    )
    reply = response.choices[0].message.content
    return reply

difficultWords = ['hydroxide', 'glucose', 'cowabunga', 'orange']
theme = "dogs"
targetLength = 50
getTextToType(theme, difficultWords, targetLength, False)