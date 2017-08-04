# Giffer

Add a caption on top of a gif.

See spec here: https://gifcaptioner.herokuapp.com/

```
GET /api/search
  curl "http://127.0.0.1:5000/api/search?q=cats&limit=3&offset=1"

POST /api/caption
  curl -H "Content-Type: application/json" -X POST -d '{"text":"xyz","random":"corgis"}' http://127.0.0.1:5000/api/caption

```
#### Technology stack
- Flask w/ Flask-API for a pretty front end
- moviepy

## Dependencies
- Python 3
- Pip
- Virtualenv (pip install virtualenv)

## Installation
```shell
git clone https://github.com/lishiyo/gifcaptioner.git
cd gifcaptioner
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
// get a GIPHY api key
// create config.py and add GIPHY_API_KEY in it
python app.py
```

## Using the app
- After running `python app.py` you should be able to reach the site at localhost:5000
- Create a gif by submitting a POST with JSON data.  At the least, you'll need `text` along with one of `gif` or `search`
  - text: the text to put on the gif
  - gif: URL of the gif image to use
  - search: the search phrase to query from giphy
  
For example:
```json
{"text": "time for work", "gif": "http://25.media.tumblr.com/tumblr_m810e8Cbd41ql4mgjo1_500.gif"}
```
```json
{"text": "hey guys", "search": "elf wave"}
```
