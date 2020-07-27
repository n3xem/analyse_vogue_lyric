import requests
import base64
import os
from datetime import datetime
DOWNLOAD_SAVE_DIR = os.getenv("DOWNLOAD_SAVE_DIR")

url = 'https://rss.itunes.apple.com/api/v1/jp/apple-music/top-songs/all/100/explicit.json'
r = requests.get(url)

with open('explicit.json', mode='w') as f:
    f.write(r.text)
