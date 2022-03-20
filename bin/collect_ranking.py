#!/usr/bin/python3

import os
import requests
from bs4 import BeautifulSoup

URL_FORMAT = 'https://nendai-ryuukou.com/%d/song/%d.html'

class Song:
    year = 0
    title = ''
    artist = ''
    sales = 0

    def __init__(self, year, title, artist, sales):
        self.year = year
        self.title = title.replace('\n', '')
        self.artist = artist.replace('\n', '')
        sales = sales.replace('万', '')
        self.sales = float(sales) * 10000

    def format(self):
        return '%s\t%s\t%d' % (self.title, self.artist, self.sales)

def get_content(year):
    url = URL_FORMAT % (int(year / 10) * 10, year)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='songTable')
    trs = table.select('tr')

    songs = []
    for tr in trs:
        tds = tr.select('td')
        if len(tds) == 0:
            continue
        songs.append(Song(year, tds[1].text, tds[2].text, tds[3].text))

    return songs


def save_data(year, songs):
    os.makedirs('data', exist_ok=True)
    with open('data/%d.csv' % year, 'w') as f:
        for s in songs:
            f.write('%s\n' % s.format())


for year in range(1970, 2022):
    songs = get_content(year)
    save_data(year, songs)
    sleep(20)



#songs = get_content(2001)

#for s in songs:
#   print(s.format()) 
