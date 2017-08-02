from urllib.request import urlopen
import urllib.error
import json
import os

# API_KEY = os.environ['GIPHY_API_KEY'] 
API_KEY = 'fbd8d8a211db4c5484fd2a3ff34bea4b'

def translate(search_text):
    response = urlopen('http://api.giphy.com/v1/gifs/translate?s=%s&api_key=%s' % (search_text.replace(' ', '+'), API_KEY))
    data = json.load(response)['data']
    return data['images']['original']['url']

def search(search_text):
    response = urlopen('http://api.giphy.com/v1/gifs/search?q=%s&limit=1&api_key=%s' % (search_text.replace(' ', '+'), API_KEY))
    data = json.load(response)['data']
    if len(data) > 0:
        return data[0]['images']['original']['url']
    else:
        raise Exception('The search query had no results')
