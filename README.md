# Gifcaptioner

A simple flask server to add a caption on top of a gif. Available online at: https://gifcaptioner.herokuapp.com/

![screenshot](https://media.giphy.com/media/3ohs7SIXVLf9HkE1HO/giphy.gif) ![screenshot](https://media.giphy.com/media/xT0xehettm94WhYamk/giphy.gif)

```
GET /api/search
  curl "http://127.0.0.1:5000/api/search?q=cats&limit=3&offset=1"

POST /api/caption
  curl -H "Content-Type: application/json" -X POST -d '{"text":"xyz","random":"corgis"}' http://127.0.0.1:5000/api/caption

```

#### Technology stack
- Flask w/ Flask-API for a useful front end
- moviepy for combining image and text
- giphy api for searching gifs

#### Dependencies
- Python 3
- Pip 3

## Development
```shell
git clone https://github.com/lishiyo/gifcaptioner.git
cd gifcaptioner
mkvirtualenv -p /usr/local/bin/python3 // OR virtualenv venv
workon venv // OR source venv/bin/activate
pip3 install -r requirements.txt
// get a GIPHY api key
// create .env in root and add `GIPHY_API_KEY` in it
python3 app.py
```

## Usage
- After running `python app.py` open at `localhost:5000`
  - the prod site is not working atm due to the timeouts with heroku (TODO)
- Create a gif by POSTing to `localhost:5000` with JSON data. The data should contain a key for `text` along with *either* `gif` or `search`:
  - `text`: the text to put on the gif
  - `gif`: URL of the gif image to use
  - `search`: a search phrase to query from giphy (will use a random gif from results)
  
Examples:
```json
{
  "text": "time for work", 
  "gif": "http://25.media.tumblr.com/tumblr_m810e8Cbd41ql4mgjo1_500.gif"
}
```
```json
{
  "text": "who's a good boy", 
  "search": "cute doggies"
}
```

