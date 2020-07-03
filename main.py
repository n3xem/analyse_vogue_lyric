import requests
import re
import time
from bs4 import BeautifulSoup
import json

def downloadSongTitle():
  musicJsonUrl = "https://rss.itunes.apple.com/api/v1/jp/apple-music/top-songs/all/100/explicit.json"
  response = requests.get(musicJsonUrl)

  musicJson = response.json()

  musicTitleList = []
  for i in range(100):
    musicTitle = musicJson["feed"]["results"][i]["name"]
    musicTitleList.append(musicTitle)

  return musicTitleList

def downloadLyric(lyricTitle):
  lyricSearchUrl = "https://www.uta-net.com/search/?Aselect=2&Bselect=3&Keyword={0}&sort=6".format(lyricTitle)
  response = requests.get(lyricSearchUrl)

  time.sleep(2)
  soup = BeautifulSoup(response.text, "html.parser")
  lyricUrlComp = soup.select("tbody:first-of-type tr:first-of-type td:first-of-type a")
  if lyricUrlComp == []:
    return "none"
  lyricUrl = "https://www.uta-net.com" + lyricUrlComp[0].attrs['href']  
  response = requests.get(lyricUrl)
  soup = BeautifulSoup(response.text, 'html.parser')
  lyricHtml = str(soup.find("div", id="kashi_area"))
  lyric = re.sub('<.+?>', ' ', lyricHtml)
  return lyric

musicTitleList = downloadSongTitle()
for lyric in musicTitleList:
  print(lyric)
  print(downloadLyric(lyric))
