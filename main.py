import requests
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
  print(response.text)

musicTitleList = downloadSongTitle()
downloadLyric(musicTitleList[0])

