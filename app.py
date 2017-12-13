from flask.ext.api import FlaskAPI, exceptions
from flask import request, send_file, jsonify
from gif_factory import GifFactory
from fileremover import FileRemover
import giphy
from random import randint
import os
from os.path import join, dirname
import requests

# DEV
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = FlaskAPI(__name__)
app.config.update(
    GIPHY_API_KEY=os.environ.get("GIPHY_API_KEY")
)

# app.config.from_object('config')
factory = GifFactory()
file_remover = FileRemover()

# constants
LIMIT = 4

@app.route('/', methods = ['GET', 'POST'])
def giffer():
    if request.method == 'POST':
        data = request.data
        if 'gif' in data and 'search' in data:
            raise exceptions.ParseError
        if 'gif' not in data and 'search' not in data:
            raise exceptions.ParseError

        if 'search' in data:
            if 'search_type' in data and data['search_type'] == 'translate':
                data['gif'] = giphy.translate(app.config['GIPHY_API_KEY'], data['search'])
            else:
                data['gif'] = giphy.search(app.config['GIPHY_API_KEY'], data['search'])
            data.pop('search')
            data.pop('search_type', None)

        # clean up params
        data.pop('limit', None)
        data.pop('offset', None)

        # A bug in moviepy requires ver_align and hor_align to be string, not unicode
        # https://github.com/Zulko/moviepy/issues/293
        for key in ['hor_align', 'ver_align']:
            if key in data and type(data[key]) == unicode:
                data[key] = str(data[key])

        gif_file = factory.create(**data)

        # upload it to file.io for temp storage (2 weeks)
        url = 'https://file.io/'
        files = {'file': open(gif_file, 'rb')}
        res = requests.post(url, files=files)
        # res_json = res.json()
        
        uploaded_url = res.json()['link']
        print('response from server: {} === uploaded_url === {} === '.format(res.text, uploaded_url))
      
        # resp = send_file(gif_file, mimetype='image/gif')
        # delete the file after it's sent
        # http://stackoverflow.com/questions/13344538/how-to-clean-up-temporary-file-used-with-send-file
        file_remover.cleanup_once_done(res, gif_file)

        return print_url(uploaded_url)
        # return resp
    else:
        return print_guide()

# GET /api/search?q=cats&offset=4 => hits giphy's /search api
# @return { 
#   offset: 4, 
#   urls: [ 
#      { 
#           preview: 'http://cat1_200.gif', 
#           original: 'http://cat1.gif'
#      }
#      ...
#   ] 
# }
# curl "http://127.0.0.1:5000/api/search?q=cats&limit=3&offset=1"
@app.route('/api/search', methods=['GET'])
def search():
    args = request.args.to_dict()
    if (args['limit'] and args['offset']):
        limit = args['limit'] # TODO: use later for pagination
        offset = args['offset']
    else:
        limit = LIMIT # TODO: use later for pagination
        offset = randint(0, LIMIT-1)
    
    resp = { "limit": limit, "offset": offset }
    resp["results"] = giphy.search(app.config['GIPHY_API_KEY'], args['q'], limit, offset)
    return jsonify(resp)

# curl -H "Content-Type: application/json" -X POST -d 
# '{"text": "my caption","random":"corgis"}' http://127.0.0.1:5000/api/caption
@app.route('/api/caption', methods=['POST'])
def caption():
    data = request.data
    # either `url: '*.gif'` or `random: 'blah'` to hit translation api 
    if 'url' in data and 'random' in data:
        raise exceptions.ParseError
    if 'url' not in data and 'random' not in data:
        raise exceptions.ParseError
    if 'text' not in data:
        raise exceptions.ParseError

    if 'random' in data: # get random gif, defaulting to translate api
        query = data['random']
        if 'search_type' in data and data['search_type'] == 'search':
            data['url'] = giphy.search(app.config['GIPHY_API_KEY'], query)
        else:
            data['url'] = giphy.translate(app.config['GIPHY_API_KEY'], query)

    for key in ['hor_align', 'ver_align']:
        if key in data and type(data[key]) == unicode:
            data[key] = str(data[key])

    filtered = dict([('gif', data['url']), ('text', data['text'])])
    gif_file = factory.create(**filtered)

    # this sends *.gif NOT json
    resp = send_file(gif_file, mimetype='image/gif')

    file_remover.remove_file(gif_file)
    
    return resp

def print_url(url):
    return { "download_url": url }

def print_guide():
    commands = {}
    commands['text'] = 'The text to put on the gif'
    commands['gif'] = 'The original gif url'
    commands['search'] = 'search giphy for an image'
    commands['search_type'] = "giphy search type, 'search' or 'translate' [search]"
    commands['hor_align'] = 'Horizontal alignment [center]'
    commands['ver_align'] = 'Vertical alignment [top]'
    commands['text_height'] = 'Height of text as percentage of image height [20]'
    commands['text_width'] = 'Maximum width of text as percentage of image width [60]'
    samples = []
    samples.append({"text": "time for work", "gif": "http://25.media.tumblr.com/tumblr_m810e8Cbd41ql4mgjo1_500.gif"})
    samples.append({"text": "oh hai", "search": "cute cats"})
    return {"Command Guide": commands, "Samples": samples}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
