import re, string
import pandas as pd
from urllib import request
from bs4 import BeautifulSoup
from unidecode import unidecode

translator = str.maketrans("", "",string.punctuation.replace("_",""))

def get_urls(artist, pagenum):
    d = {'title': [], 'url': [], 'lyrics': []}
    song_page = "http://www.metrolyrics.com/" + artist + "-alpage-{}.html"
    urls = []
    titles = []
    for i in range(pagenum):
        print("scraping title/url page {}".format(i+1))
        page = request.urlopen(song_page.format(i+1))
        soup = BeautifulSoup(page, 'html.parser')
        rows = soup.find('table').find('tbody').find_all('tr')
        for row in rows:
            a = row.find_all('td')[1].find('a', href=True)
            url = a['href']

            title = row.text.strip().lower().replace(" ", "_").split('\n')[0][:-7]
            title = title.translate(translator)

            d['title'].append(title)
            d['url'].append(url)
            d['lyrics'].append(" ")

    return pd.DataFrame(data=d)

def scrape_lyrics(songs):
    for index, row in songs.iterrows():
        page = request.urlopen(row['url'])
        soup = BeautifulSoup(page, 'html.parser')
        verses = soup.find_all('p', attrs={'class': 'verse'})

        lyrics = ''

        for verse in verses:
            text = verse.text.strip()
            text = re.sub(r"\[.*\]\n", "", unidecode(text))
            if lyrics == "":
                lyrics = lyrics + text.replace('\n', '|-|')
            else:
                lyrics = lyrics + '|-|' + text.replace('\n', '|-|')

        print("saving {}".format(row['title']))
        songs.at[index, 'lyrics'] = lyrics
    
    return songs

def save(filename, df):
    print("writing to .csv")
    df.to_csv(filename, sep=',', encoding='utf-8')

def load(filename):
    print("loading .csv")
    return pd.read_csv(filename)

def clean(df):
    return df.dropna()

artist = "eminem"
numpages = 8
old_filename = "../eminem-songs.csv"
new_filename = "../eminem-songs-new.csv"

#data = get_urls(artist, numpages)
#songs = scrape_lyrics(data)

#songs = load(old_filename)
#print("old shape: {}".format(songs.shape))
#cleaned_songs = clean(songs)
#print("new shape: {}".format(cleaned_songs.shape))
#save(new_filename, cleaned_songs)

