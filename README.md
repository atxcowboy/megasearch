# Megasearch
Megasearch for Oobabooga TextUI is an extension that allows a user to search multiple search engines and include the output in the context.
Initially we're using Google API or DuckDuckGo. 

As this is an Open Source project your PRs are very much welcome!

## Installation
1. To install the plugin, copy the megasearch folder to the text-generation-webui/extensions folder in your Ooobabooga installation.
2. Open script.py and fill in your Google API Key as well as the CSE_ID.
Follow the instructions at https://developers.google.com/custom-search/v1/overview?hl=en
3. Launch Oobabooga with the flag --extension megasearch as per their documentation at https://github.com/oobabooga/text-generation-webui/blob/main/docs/Extensions.md
4. In the Oobabooga interface check "Enable Search" and choose your Search Engine. Initially you have a choice between Google and DuckDuckGo.
Please note that Google Search is a paid API that relies on credentials whereas DuckDuckGo does not even need an API key and is free to use.
![prompt1](https://github.com/atxcowboy/megasearch/assets/8017357/1e3a1f5e-fa62-4980-a61a-476423a161f6)
