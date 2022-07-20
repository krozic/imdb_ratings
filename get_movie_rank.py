import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import requests
import re
from typing import Dict, Any

with open('./tables/genre_rank.csv', 'r') as filehandle:
    genre_rank = pd.read_csv(filehandle)

def get_movie_info(url: str) -> Dict[str, Any]:
    '''Takes an IMDB movie url and returns
     the rating, genres, title, and poster link in a Dict'''
    movie_info = {}
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, 'html.parser')

    # movie_info['title'] = page_soup.find('h1', {'class':'sc-b73cd867-0 eKrKux'}).get_text()
    # movie_info['rating'] = float(page_soup.find('span', {'class':'sc-7ab21ed2-1 jGRxWM'}).get_text())
    movie_info['title'] = page_soup.find('h1', {'data-testid':'hero-title-block__title'}).get_text()
    movie_info['rating'] = float(page_soup.find('div', {'data-testid': 'hero-rating-bar__aggregate-rating'}).find('span').get_text())

    # genres_soup = page_soup.find('div', {'class':'ipc-chip-list__scroller'}).find_all('span')
    genres_soup = page_soup.find('div', {'data-testid': 'genres'}).find_all('span')
    genres = []
    for i in genres_soup:
        genres.append(i.get_text())
    movie_info['genres'] = genres

    poster_text = page_soup.find('img', {'class':'ipc-image'})
    poster_link = re.search('src=".*jpg"', str(poster_text)).group()
    movie_info['poster'] = poster_link[5:len(poster_link)-1]

    return movie_info

def get_movie_rank(movie_info: Dict[str, Any], genre_rank: pd.DataFrame) -> pd.DataFrame:
    '''Takes a movie_info Dict and genre_rank DataFrame
    returns the ranking for each genre'''
    # movie_rank = {}
    # genres = movie_info['genres']
    ranks = []
    movie_rank = pd.DataFrame({'Genre': movie_info['genres']})
    rating = movie_info['rating']

    for genre in movie_info['genres']:
        # movie_rank[genre] = genre_rank.loc[genre_rank['averageRating'] == rating, [genre]].values[0][0]
        ranks.append(genre_rank.loc[genre_rank['averageRating'] == rating, [genre]].values[0][0])
    movie_rank['Rank'] = ranks

    return movie_rank.sort_values('Rank', ascending=False)


# url = 'https://www.imdb.com/title/tt12004038/'
# movie_info = get_movie_info(url)
# print(movie_info)
# movie_rank = get_movie_rank(movie_info, genre_rank)
# print(movie_rank)