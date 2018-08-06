from urllib.request import urlopen
import urllib.error
import json
import os

def translate(api_key, search_text):
    response = urlopen('http://api.giphy.com/v1/gifs/translate?s=%s&api_key=%s' % (search_text.replace(' ', '+'), api_key))
    data = json.load(response)['data']
    return data['images']['original']['url']

def search(api_key, search_text, limit=1, offset=0):
    response = urlopen('http://api.giphy.com/v1/gifs/search?q=%s&limit=%s&api_key=%s&offset=%s' % (search_text.replace(' ', '+'), limit, api_key, offset))
    gifobjects = json.load(response)['data']
    if len(gifobjects) > 0:
      if limit == 1:
        return gifobjects[0]['images']['original']['url']
      else:
        mapped_arr = list(map(gifobject_to_urls, gifobjects))
        return mapped_arr
    else:
      raise Exception('The search query had no results')

def gifobject_to_urls(gifobject):
  original_url = gifobject['images']['original']['url']
  preview_url = gifobject['images']['fixed_width']['webp']
  return dict([('original_url', original_url), ('preview_url', preview_url)])
