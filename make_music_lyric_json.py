import requests
import re
import time
from bs4 import BeautifulSoup
import json


def download_lyric(lyricTitle):
    lyricSearchUrl = "https://www.uta-net.com/search/?Aselect=2&Bselect=4&Keyword={0}&sort=4".format(
        lyricTitle)
    response = requests.get(lyricSearchUrl)

    soup = BeautifulSoup(response.text, "html.parser")
    lyricUrlComp = soup.select(
        "tbody:first-of-type tr:first-of-type td:first-of-type a")
    if lyricUrlComp == []:
        return "none"
    lyricUrl = "https://www.uta-net.com" + lyricUrlComp[0].attrs['href']
    response = requests.get(lyricUrl)
    soup = BeautifulSoup(response.text, 'html.parser')
    lyricHtml = str(soup.find("div", id="kashi_area"))
    lyric = re.sub('<.+?>', '。', lyricHtml)
    lyric = lyric[1:]

    lyric = re.sub('！。', '！', lyric)
    lyric = re.sub('!。', '!', lyric)
    lyric = re.sub('。{2,}', '。', lyric)

    return lyric


def create_music_dic(orig_dic):
    music_title = orig_dic["name"]
    artist_name = orig_dic["artistName"]
    genre = orig_dic["genres"][0]["name"]
    lyric = download_lyric(music_title)

    table = str.maketrans({
        '\u3000': ''
    })

    lyric = lyric.translate(table)
    time.sleep(1)
    procced_dic = {'music_title': music_title,
                   'artist_name': artist_name, 'genre': genre, 'lyric': lyric}
    return procced_dic


dic = {}
with open('./explicit.json') as f:
    musicJson = json.load(f)
    for i in range(100):
        procced_dic = create_music_dic(musicJson["feed"]["results"][i])
        dic.update({i: procced_dic})
    print(dic)

with open('./music_lyric.json', 'w') as f:
    json.dump(dic, f, ensure_ascii=False, indent=4)
