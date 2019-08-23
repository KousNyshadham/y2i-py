#!/usr/bin/env/ python
from bs4 import BeautifulSoup
import requests
import os
import sys
import json
search = sys.stdin.readline()
search = search.replace(' ', '+')
imagepage = requests.get("https://www.google.com/search?q=" + search + "&tbm=isch")
soup = BeautifulSoup(imagepage.content,'html.parser')
imageurl = soup.find_all('img')[0]["src"]
os.system("wget -O albumart.jpg " + imageurl)
youtubepage = requests.get("https://www.youtube.com/results?search_query=" + search)
soup = BeautifulSoup(youtubepage.content,'html.parser')
youtubeurl = "https://www.youtube.com" + soup.find_all('h3',class_='yt-lockup-title')[0].a['href']
os.system("youtube-dl --extract-audio --audio-format mp3 " + youtubeurl)
os.system("mv *.mp3 rawvideo.mp3")
metadata = requests.get("https://itunes.apple.com/search?term=" + search).json()
name = metadata["results"][0]["trackName"];
artist = metadata["results"][0]["artistName"]
album = metadata["results"][0]["collectionName"]
genre = metadata["results"][0]["primaryGenreName"]
year = metadata["results"][0]["releaseDate"]
os.system('ffmpeg -i rawvideo.mp3 -i albumart.jpg -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" -metadata title="'+ name + '" -metadata artist="' + artist +'" -metadata album="' + album + '" -metadata genre="' + genre + '" -metadata date="' + year  + '" itunesready.mp3')
os.system('cp itunesready.mp3 ~/Music/iTunes/iTunes\ Media/Automatically\ Add\ to\ iTunes.localized')
os.system('rm *.jpg *.mp3')
