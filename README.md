# Gifcaptioner

A simple flask server to add a caption on top of a gif. Demo and docs at: https://gifcaptioner.herokuapp.com/

<img src=https://media.giphy.com/media/3ohs7SIXVLf9HkE1HO/giphy.gif height=300> <img src=https://media.giphy.com/media/xT0xehettm94WhYamk/giphy.gif height=300>

```
GET /api/search
  curl "http://127.0.0.1:5000/api/search?q=cats&limit=3&offset=1"

POST /api/caption
  curl -H "Content-Type: application/json" -X POST -d '{"text":"sup", "search": "corgis"}' http://127.0.0.1:5000/api/caption

// returns "redirect" url to follow for the job
{
  "redirect": "/status/ec101759-438e-44fc-8a3a-ddf09f6418a2"
}
curl http://127.0.0.1:5000/status/ec101759-438e-44fc-8a3a-ddf09f6418a2
{
  "result": {
    "expiry": "14 days",
    "key": "gnLuV4",
    "link": "https://file.io/gnLuV4",
    "success": true
  },
  "status": "finished"
}

// download the result
curl https://file.io/gnLuV4 --output output.gif
```

#### Development
```shell
git clone https://github.com/lishiyo/gifcaptioner.git
cd gifcaptioner
mkvirtualenv -p /usr/local/bin/python3 // OR virtualenv venv
workon venv // OR source venv/bin/activate
pip3 install -r requirements.txt
// get a GIPHY api key
// create config.py in root and add `GIPHY_API_KEY` in it
python3 app.py
// open at localhost:5000
```

#### Usage
[online demo](https://gifcaptioner.herokuapp.com/):
- Create a gif by POSTing to filling the form with JSON data. The data should contain a key for `text` along with one of either `gif` or `search`:
  - `text`: the text to put on the gif
  - `gif`: (optional) URL of the gif image to use
  - `search`: (optional) a search phrase to query from giphy (will use a random gif from results)
  
Examples
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

- This redirects to the job status page. Wait a few seconds then refresh, should see a result with a one-time file.io `link` to download, ex `https://file.io/wtr13C`.

#### Technology stack
- Flask w/ Flask-API for a useful front end
- moviepy for combining image and text
- giphy api for searching gifs

#### Dependencies
- Python 3 and Pip 3
- imagemagick (see heroku buildpack)
- heroku buildpacks: 
  - https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
  - https://github.com/ello/heroku-buildpack-imagemagick.git
  - https://github.com/weibeld/heroku-buildpack-graphviz
  - heroku/python
