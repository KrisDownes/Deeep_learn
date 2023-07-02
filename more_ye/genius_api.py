import requests
from bs4 import BeautifulSoup
import os
import re
class genius_api():
    
    def __init__(self,artist,token,song_count,page):
        self.artist = artist
        self.token = token
        self.song_count = song_count
        self.page = page
    def get_artist_info(self,artist,page):
        base_url = 'https://api.genius.com'
        headers = {'Authorization': 'Bearer ' + self.token}
        search_url = base_url + '/search?per_page=10&page=' + str(page)
        data = {'q' : artist}
        response = requests.get(search_url,data=data,headers=headers)
        return response
    def get_song_url(self):
        urls = []
        while len(urls) < self.song_count:
            response = self.get_artist_info(self.artist,self.page)
            json = response.json()
            song_info = []
            for hit in json['response']['hits']:
                if self.artist.lower() in hit['result']['primary_artist']['name'].lower():
                    song_info.append(hit)
            for song in song_info:
                if len(urls) < self.song_count:
                    urls.append(song['result']['url'])
                if len(urls) == self.song_count:
                    break
                else:
                    self.page += 1
        return urls            
    def get_songs_lyrics(self,url):
        pg = requests.get(url)
        html = BeautifulSoup(pg.text,'html.parser')
        div = html.find("div", class_=re.compile("^lyrics$|Lyrics__Root") )
        lyrics = div.get_text()
        return lyrics
    def get_artist_lyrics(self,lyrics,artist):
        new_lyrics = []
        pattern = re.compile(r'([\[].*?[\]])(.*?[^\[]*)')
        for match in pattern.finditer(lyrics):
            if f"{artist}" in (match.group(1).split('&')[0]):
                new_lyrics.append(os.linesep.join([s for s in match.group(2).splitlines() if s]))
        return new_lyrics    
