from funcs import *
from bs4 import BeautifulSoup
import requests

dob = input('Enter your date of birth\nYYYY-MM-DD:\n')
pl_name = dob

response = requests.get(f'https://www.billboard.com/charts/hot-100/{dob}/')
bbpage = response.text

bs = BeautifulSoup(bbpage, 'html.parser')

rawdata = bs.findAll(class_='o-chart-results-list-row-container')

songlist = [ ]
artists = [ ]

# Find song title #
for e in rawdata:
    song = e.findAll(class_='c-title')[ 0 ].getText().strip()
    songlist.append(song.replace('"', '').replace("'", "").replace('(', '').replace(')', '').replace('&', ''))

# Find artists #
for a in rawdata:
    if a.findAll(class_='c-label')[ 1 ].getText().strip() == 'NEW':
        artist = a.findAll(class_='c-label')[ 3 ].getText().strip()
    else:
        artist = a.findAll(class_='c-label')[ 1 ].getText().strip()
    artists.append(artist.replace('"', '').replace("'", "").replace('(', '').replace(')', '').replace('&', ''))

itemlist = [ ]

for i, s in enumerate(songlist):
    item = getsongid(artists[ i ], s)
    if item[ 0 ] != 'No result':
        itemlist.append(item)


if len(itemlist) > 0:
    playlist = createplaylist(pl_name)
    for item in itemlist:
        addsong(item, playlist)
else:
    print('Found nothing!\nMaybe wrong date format?')

print('Done!')
