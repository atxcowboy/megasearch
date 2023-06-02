import gradio as gr
import requests
import json
from bs4 import BeautifulSoup
from summarizer import Summarizer

# Define the interface components
def ui():
    components = [
        gr.inputs.Checkbox(label='SEARCH_ACCESS', default=True),
        gr.inputs.Radio(['Google', 'DuckDuckGo'], label='SEARCH_ENGINE', default='Google'),
        gr.inputs.Textbox(label='API_KEY'),
        gr.inputs.Textbox(label='CSE_ID'),
        gr.inputs.Textbox(label='QUERY')
    ]
    return components

# Define the params dictionary
params = {
    'SEARCH_ACCESS': True,
    'SEARCH_ENGINE': 'Google',
    'API_KEY': '',
    'CSE_ID': '',
    'QUERY': 'Panomity GmbH'
}

def input_modifier(string):
    # Check if the search engine is Google
    if params["SEARCH_ENGINE"] == 'Google':
        url = f"https://www.googleapis.com/customsearch/v1?key={params['API_KEY']}&cx={params['CSE_ID']}&q={params['QUERY']}"
        response = requests.get(url)
        data = json.loads(response.text)
        texts = ''
        count = 0
        max_results = 3
        result_max_characters = 250
        if 'items' in data:
            for result in data['items']:

                if count <= max_results:
                    link = result['link']
                    page_content = requests.get(link).text
                    soup = BeautifulSoup(page_content, 'html.parser')
                    paragraphs = soup.find_all('p')
                    content = ' '.join([p.get_text() for p in paragraphs])
                    if len(content) > 0:  # ensure content is not empty
                        model = Summarizer()
                        summary = model(content, num_sentences=3)  # Adjusted line
                        texts = texts + ' ' + summary
                        count += 1
            string += texts[:result_max_characters]
    return string

# Define the event handler for parameter updates
def update_params(inputs):
    global params
    for input_name, input_value in inputs.items():
        params[input_name] = input_value

# Create the Gradio interface and bind the event handler
iface = gr.Interface(inputs=ui(), outputs="text", fn=input_modifier, update_fn=update_params)
