# Import the os package
import os

# Import the openai package
from openai import OpenAI

# From the IPython.display package, import display and Markdown
from IPython.display import display, Markdown

# Import yfinance as yf
import yfinance as yf


print("start")
client = OpenAI(
    api_key= os.environ.get("OPENAI_KEY"),
    base_url="https://hack.funandprofit.ai/api/providers/openai/v1"
)

difficultWords = ['hydroxide', 'glucose', 'cowabunga', 'orange']
theme = "dogs"
targetLength = 50
systemPrompt = "You are in charge of generating text for a typing test. You should follow any themes, and word limits as closely as possible. YOU MUST include all words in the given list of tricky words. Having tricky words show up multiple times is ideal, but the most important thing is that they appear at least once or the user will be severely, emotionally hurt. You should aim to make your output educational on the chosen subject."
textPrompt = f'Generate an {targetLength} word passage containg the difficult words {difficultWords}. The passage should follow the theme {theme}.'
codePrompt = f'Generate {targetLength} words of python code. Your output MUST be code or the user will be very upset! You must include the difficult words {difficultWords}. The code should follow the theme {theme}. Do not write anything other than code. Do not indicate where code starts or ends.'
response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Or whatever model is supported by your proxy
    messages=[
        {"role": "system", "content": systemPrompt},
        {"role": "user", "content": textPrompt}
    ]
)
reply = response.choices[0].message.content
print(reply)
print("\n")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Or whatever model is supported by your proxy
    messages=[
        {"role": "system", "content": systemPrompt},
        {"role": "user", "content": codePrompt}
    ]
)
reply = response.choices[0].message.content
print(reply)

# #"Generate an 80 word passage containg the difficult words ['hydroxide', 'glucose', 'function', 'print']. The passage should follow the theme python code."
# #"Generate 80 words of code including the difficult words ['hydroxide', 'glucose', 'function', 'print']. The code should follow the theme python code. Do not write anything other than code. Do not indicate where code starts or ends."


