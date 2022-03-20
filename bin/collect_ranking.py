#!/usr/bin/python3

import sys
import os
import time
import requests
from bs4 import BeautifulSoup

URL_FORMAT = 'https://nendai-ryuukou.com/%d/song/%d.html'
URL_FORMAT_2010 = 'https://nendai-ryuukou.com/%d/song.html'

class Song:
    year = 0
    title = ''
    artist = ''
    sales = 0

    def __init__(self, year, title, artist, sales):
        self.year = year
        self.title = title.replace('\n', '')
        self.artist = artist.replace('\n', '')
        sales = sales.replace('万', '').replace('b', '') # なぜか2018年の売上枚数にbがあるので除外する。
        if sales != '':
            self.sales = float(sales) * 10000

    def format(self):
        return '%s\t%s\t%d' % (self.title, self.artist, self.sales)

def get_content(year):
    if year > 2009:
        url = URL_FORMAT_2010 % year
    else:
        url = URL_FORMAT % (int(year / 10) * 10, year)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='songTable')
    if table == None:
        print('Error: %d: table.songTable テーブルを取得できませんでした。' % year, file=sys.stderr)
        print(soup)
        sys.exit(1)
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
    print('saved: %d' % year)
    time.sleep(20)

print('complate')
