import gradio as gr
import requests
import json

SEARCH_ACCESS = False
SEARCH_ENGINE = None
API_KEY = ''
CSE_ID = ''

def ui():
    global SEARCH_ACCESS, SEARCH_ENGINE, API_KEY1, API_KEY2
    SEARCH_ACCESS = gr.inputs.Checkbox(label="Enable Search", default=False)
    SEARCH_ENGINE = gr.inputs.Radio(['Google', 'DuckDuckGo'], label="Choose Search Engine")
    API_KEY = gr.inputs.Textbox(lines=1, placeholder="Enter Google API Key if Google is selected")
    CSE_ID = gr.inputs.Textbox(lines=1, placeholder="Enter Google CSE ID if Google is selected")
    return [SEARCH_ACCESS, SEARCH_ENGINE, API_KEY1, API_KEY2]

def input_modifier(user_input):
    global SEARCH_ACCESS, SEARCH_ENGINE, API_KEY1, API_KEY2
    result_max_characters = 250
    max_results = 3
    if SEARCH_ACCESS:
        if user_input.lower().startswith("search:"):
            query = user_input[len("search:"):].strip()
            if SEARCH_ENGINE == 'Google':
                url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CSE_ID}&q={query}"
                response = requests.get(url)
                data = json.loads(response.text)
                texts = ''
                count = 0
                for result in data['items']:
                    if count <= max_results:
                        text = result['snippet']
                        texts = texts + ' ' + text
                        count += 1
                texts = texts[0:result_max_characters]
                print(texts)
                return texts
            elif SEARCH_ENGINE == 'DuckDuckGo':
                url = f"https://api.duckduckgo.com/?q={query}&format=json"
                response = requests.get(url)
                data = json.loads(response.text)
                texts = ''
                count = 0
                for result in data['Results']:
                    if count <= max_results:
                        text = result['Text']
                        texts = texts + ' ' + text
                        count += 1
                texts = texts[0:result_max_characters]
                print(texts)
                return texts
    return user_input

def output_modifier(output):
    return output

def bot_prefix_modifier(prefix):
    return prefix
