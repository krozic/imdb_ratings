from my_secrets import api_key
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import requests
import re
from typing import Dict, Any

def get_movie_info(url: str, query: bool = False) -> Dict[str, Any]:
    """
    Takes an IMDB movie url or tconst query result and returns
    the rating (imdb, rt, and mc), genres, title, poster link and IMDB link in a Dict
    """

    if query:
        url = f'https://www.imdb.com/title/{url}/'
    movie_info = {}
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, 'html.parser')

    movie_info['title'] = page_soup.find('h1', {'data-testid':'hero-title-block__title'}).get_text()
    movie_info['imdb'] = float(page_soup.find('div', {'data-testid': 'hero-rating-bar__aggregate-rating'}).find('span').get_text())

    movie = re.search('tt[0-9]+', url).group()
    r = requests.get(
        f'http://www.omdbapi.com/?i={movie}&apikey={api_key}')
    data = r.json()
    rt = np.nan
    try:
        for rating in data['Ratings']:
            if rating['Source'] == 'Rotten Tomatoes':
                rt = int(rating['Value'].replace('%', ''))
                break
            else:
                rt = np.nan
    except:
        rt = np.nan
    try:
        if data['Metascore'] != 'N/A':
            mc = int(data['Metascore'])
        else:
            mc = np.nan
    except:
        mc = np.nan
    if np.isnan(mc):
        try:
            mc = int(page_soup.find('span', {'class': 'score-meta'}).get_text())
        except:
            mc = np.nan

    movie_info['rt'] = rt
    movie_info['mc'] = mc

    genres_soup = page_soup.find('div', {'data-testid': 'genres'}).find_all('span')
    genres = []
    for i in genres_soup:
        if i.get_text() == 'Music':
            continue
        genres.append(i.get_text())
    movie_info['genres'] = genres

    poster_text = page_soup.find('img', {'class':'ipc-image'})
    poster_link = re.search('src=".*jpg"', str(poster_text)).group()
    movie_info['poster'] = poster_link[5:len(poster_link)-1]
    movie_info['url'] = url

    return movie_info

def get_movie_rank(movie_info: Dict[str, Any], rank_tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Takes a movie_info Dict and rank_tables Dict of DataFrames
    Returns the ranking for each genre for each rating system
    """

    ranks = []
    movie_rank = pd.DataFrame({'Genre': movie_info['genres']})
    rating = movie_info['imdb']
    genre_rank = rank_tables['imdb_genre_rank']

    for genre in movie_info['genres']:
        ranks.append(genre_rank.loc[genre_rank['rating'] == rating, [genre]].values[0][0])
    movie_rank['IMDB Rank'] = ranks

    if movie_info['rt'] == None:
        movie_info['rt'] = np.nan
    if movie_info['mc'] == None:
        movie_info['mc'] = np.nan
    if not np.isnan(movie_info['rt']):
        ranks = []
        rating = movie_info['rt']
        genre_rank = rank_tables['rt_genre_rank']
        for genre in movie_info['genres']:
            ranks.append(genre_rank.loc[genre_rank['rating'] == rating, [genre]].values[0][0])
        movie_rank['Tomatometer Rank'] = ranks

    if not np.isnan(movie_info['mc']):
        ranks = []
        rating = movie_info['mc']
        genre_rank = rank_tables['mc_genre_rank']
        for genre in movie_info['genres']:
            ranks.append(genre_rank.loc[genre_rank['rating'] == rating, [genre]].values[0][0])
        movie_rank['Metascore Rank'] = ranks

    return movie_rank.sort_values('IMDB Rank', ascending=False)


def highlight_rating(rating_choice: str) -> Dict:
    """
    Takes the rating_choice and returns the className for application formatting.
    """
    highlighter = {
        'imdb': '',
        'rt': '',
        'mc': '',
        rating_choice: 'bg-secondary text-white'
    }
    return highlighter

# url = 'https://www.imdb.com/title/tt3704428/?ref_=tt_rvi_tt_i_5'
# url = 'https://www.imdb.com/title/tt7144666/?ref_=hm_wls_tt_i_1'
# movie_info = get_movie_info(url)
# movie_rank = get_movie_rank(movie_info, rank_tables)
# movie_rank = get_movie_rank(movie_info, genre_rank)
