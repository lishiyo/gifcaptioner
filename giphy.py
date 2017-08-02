from urllib.request import urlopen
import urllib.error
import json
import os
import config

def translate(search_text):
    response = urlopen('http://api.giphy.com/v1/gifs/translate?s=%s&api_key=%s' % (search_text.replace(' ', '+'), GIPHY_API_KEY))
    data = json.load(response)['data']
    return data['images']['original']['url']

def search(search_text):
    response = urlopen('http://api.giphy.com/v1/gifs/search?q=%s&limit=1&api_key=%s' % (search_text.replace(' ', '+'), GIPHY_API_KEY))
    data = json.load(response)['data']
    if len(data) > 0:
        return data[0]['images']['original']['url']
    else:
        raise Exception('The search query had no results')
