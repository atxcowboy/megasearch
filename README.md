# Megasearch
Megasearch for Oobabooga TextUI is an extension that allows a user to search multiple search engines and include the output in the context.
Initially we're using Google API or DuckDuckGo. 

As this is an Open Source project your PRs are very much welcome!

## Installation
1. To install the plugin, copy the megasearch folder to the extensions folder.
2. Open script.py and fill in your Google API Key as well as the CSE_ID.
Follow the instructions at https://developers.google.com/custom-search/v1/overview?hl=en
3. Launch Oobabooga with the flag --extension megasearch.
4. In the Oobabooga interface check "Enable Search" and choose your Search Engine. Initially you have a choice between Google and DuckDuckGo.
Please note that Google Search is a paid API that relies on credentials whereas DuckDuckGo does not even need an API key and is free to use.
