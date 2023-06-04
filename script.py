# ---------------------------------------------------------------------------- #
#                            MEGASEARCH FOR OOBABOOGA                          #
# ---------------------------------------------------------------------------- #
# Copyright (C) 2023 Sascha Endlicher, M.A. / Panomity GmbH
# 
# This program is free software: you can redistribute it and/or modify it under the 
# terms of the GNU General Public License as published by the Free Software Foundation, 
# either version 3 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with this program. 
# If not, see <https://www.gnu.org/licenses/>.
# 
# Contact information:
# Panomity GmbH
# ATTN: Sascha Endlicher, M.A.
# Seilergasse 34
# 85570 Markt Schwaben
# Germany
# HRB 264411, München
# hello@panomity.com
# https://panomity.com
# ---------------------------------------------------------------------------- #

# Import the necessary modules.
# gradio: A Python library to create custom UI components for Python scripts.
# requests: A Python module for making HTTP requests.
# json: A module for working with JSON data.
# BeautifulSoup: A Python library for parsing HTML and XML documents.
# summarizer: A Python library to create extractive summarizations.
import gradio as gr
import requests
import json
from bs4 import BeautifulSoup
from summarizer import Summarizer

# This is a dictionary to hold parameters for search operation. Initial values are set here.
params = {
    'SEARCH_ACCESS': True,
    'SEARCH_ENGINE': 'Searx',
    'SEARX_SERVER' : '',
    'API_KEY': '',
    'CSE_ID': '',
    'QUERY': ''
}

# Define the UI components of the Gradio interface. 
def ui():
    # This is a list of the inputs for the interface. These include a checkbox, a radio button, and several textboxes.
    components = [
        gr.inputs.Checkbox(label='SEARCH_ACCESS', default=True),  # A checkbox to control search access. The default value is True.
        gr.inputs.Radio(['Google', 'DuckDuckGo', 'Searx'], label='SEARCH ENGINE', default='Searx'),  # A radio button to select the search engine. The default value is 'Google'.
        gr.inputs.Textbox(label='SEARX_SERVER', default=params['SEARX_SERVER']),  # A textbox for the search query that will be submitted to Google.
        gr.inputs.Textbox(label='API_KEY', default=params['API_KEY']),  # A textbox for the Google API key.
        gr.inputs.Textbox(label='CSE_ID', default=params['CSE_ID']),  # A textbox for the Google Custom Search Engine (CSE) ID.
        gr.inputs.Textbox(label='QUERY')  # A textbox for the search query that will be submitted to Google.
    ]
    return components

# This function is for calling the SEARX API and processing the output
def searx_api(string):
    url=f"{params['SEARX_SERVER']}?q={string}&format=json"
    try:
        response = requests.get(url)
        print(f"response text: '{response.text}'")
    except:
        return "Searx knows nothing about this."
    print(f"response text: '{response.text}'")
    # Load the response data into a JSON object.
    data = json.loads(response.text)
    # Initialize variables for the extracted texts and count of results.
    texts = ''
    count = 0
    max_results = 3
    result_max_characters = 250
    # If there are items in the data, proceed with parsing the result.
    if 'results' in data:
        # For each result, fetch the webpage content, parse it, summarize it, and append it to the string.
        for result in data['results']:
            # Check if the number of processed results is less than or equal to the maximum number of results allowed.
            if count <= max_results:
                # Get the URL of the result.
                link = result['url']
                # Fetch the webpage content of the result.
                content = result['content']
                if len(content) > 0:  # ensure content is not empty
                    # Append the summary to the previously extracted texts.
                    texts = texts + ' ' + content
                    # Increase the count of processed results.
                    count += 1
        # Add the first 'result_max_characters' characters of the extracted texts to the input string.
        string += texts[:result_max_characters]
    # Return the modified string.
    return string

# This function is for calling the Google API and processing the output
def google_api(string):
    # Construct the URL for Google's Custom Search JSON API.
    url = f"https://www.googleapis.com/customsearch/v1?key={params['API_KEY']}&cx={params['CSE_ID']}&q={params['QUERY']}"
    # Make a GET request to the API.
    try:
        response = requests.get(url)
    except:
        return "Google knows nothing about this."
    # Load the response data into a JSON object.
    data = json.loads(response.text)
    # Initialize variables for the extracted texts and count of results.
    texts = ''
    count = 0
    max_results = 3
    result_max_characters = 250
    # If there are items in the data, proceed with parsing the result.
    if 'items' in data:
        # For each result, fetch the webpage content, parse it, summarize it, and append it to the string.
        for result in data['items']:
            # Check if the number of processed results is less than or equal to the maximum number of results allowed.
            if count <= max_results:
                # Get the URL of the result.
                link = result['link']
                # Fetch the webpage content of the result.
                page_content = requests.get(link).text
                # Parse the webpage content using BeautifulSoup.
                soup = BeautifulSoup(page_content, 'html.parser')
                # Find all the 'p' tags in the parsed content, which usually contain the main text.
                paragraphs = soup.find_all('p')
                # Join all the text from the paragraphs.
                content = ' '.join([p.get_text() for p in paragraphs])
                # If the content is not empty, proceed with summarization.
                if len(content) > 0:  # ensure content is not empty
                    # Instantiate the Summarizer.
                    model = Summarizer()
                    # Generate a summary of the content. The summary will contain 3 sentences.
                    summary = model(content, num_sentences=3)
                    # Append the summary to the previously extracted texts.
                    texts = texts + ' ' + summary
                    # Increase the count of processed results.
                    count += 1
        # Add the first 'result_max_characters' characters of the extracted texts to the input string.
        string += texts[:result_max_characters]
    # Return the modified string.        
    return string

# this lists the processing functions specific to each search engine.
search_engine_processor = {
    'Google':google_api,
    'Searx':searx_api
}

# This function is for processing the inputs based on the chosen search engine and query.
def input_modifier(string):
    return search_engine_processor.get(params['SEARCH_ENGINE'])(string)

# This function is to handle the event of parameter updates. It updates the global 'params' dictionary with the new input values.
def update_params(inputs):
    global params  # Specify that we're going to use the global 'params' dictionary.
    # For each input, update the corresponding entry in the 'params' dictionary.
    for input_name, input_value in inputs.items():
        params[input_name] = input_value

# Create a Gradio interface with the specified inputs, outputs, function to process the inputs, and function to handle parameter updates.
iface = gr.Interface(inputs=ui(), outputs="text", fn=input_modifier, update_fn=update_params)
