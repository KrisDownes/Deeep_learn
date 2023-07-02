import requests 
from bs4 import BeautifulSoup 
from genius_api import genius_api


genius_api_token = 'l3DZFPC98CPkUTx82Oj45KMCRW0xYoK4dzS70sI0sjrDvfx2S7_fbqcOxSbNu_FK'


test = genius_api('Kanye West',genius_api_token,65,1) 

urls = test.get_song_url()

##lyrics = test.get_songs_lyrics(str(urls[1]))
##print(lyrics)
##print(urls)
##print(test.get_artist_lyrics(lyrics,"Kanye West"))
lyrics = []
for url in urls:
    lyrics.append(test.get_songs_lyrics(str(url)))
ye_lyrics = []
for lyr in lyrics:
    ye_lyrics.append(test.get_artist_lyrics(lyr,"Kanye West"))
ye_lyrics = [''.join (e) for i in ye_lyrics for e in  i]
with open('kanye_lyrics.txt','w',encoding = "utf-8") as f:
    f.writelines('\n'.join(ye_lyrics))
    