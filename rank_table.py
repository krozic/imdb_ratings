import numpy as np
import pandas as pd
from typing import Tuple, List

all_ratings = pd.read_csv('./tables/all_ratings.csv')

# Creating genres list
genres = [
    'Action',
    'Adventure',
    'Animation',
    'Biography',
    'Comedy',
    'Crime',
    'Drama',
    'Family',
    'Fantasy',
    'History',
    'Horror',
    'Musical',
    'Mystery',
    'Romance',
    'Sci-Fi',
    'Sport',
    'Thriller',
    'War',
    'Western'
]

def build_rank_tables(all_ratings: pd.DataFrame, genres: list[str], rating: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    db = all_ratings[['genres', rating]].dropna().sort_values(rating)
    genre_rank = None
    genre_medians = {
        'genre': [],
        'median': []
    }
    for genre in genres:
        genre_db = db[db.genres.str.contains(genre, regex=True, na=False)]
        genre_db[genre] = ((np.arange(len(genre_db)) + 1) / len(genre_db) * 100).round(2)
        median = genre_db[genre_db[genre]<52][genre_db[genre]>48][rating].mean()
        genre_medians['genre'].append(genre)
        genre_medians['median'].append(median)
        genre_db = genre_db.groupby(rating)[genre].mean().round(1)
        genre_db = genre_db.reset_index()
        if genre_rank is not None:
            genre_rank = pd.merge(genre_rank, genre_db, how='outer', on=rating)
        else:
            genre_rank = genre_db
    genre_rank = genre_rank.sort_values(rating)
    genre_rank.rename(columns={genre_rank.columns[0]: 'rating'}, inplace=True)
    genre_medians = pd.DataFrame(genre_medians).sort_values('median')
    return genre_rank, genre_medians

rating_source = {'imdb':'averageRating', 'rt':'rt_rating', 'mc':'mc_rating'}
rank_tables = {}
for source in rating_source:
    rank_tables[source+'_genre_rank'], rank_tables[source+'_genre_medians'] = build_rank_tables(all_ratings,
                                                                                                genres,
                                                                                                rating_source[source])
for table in rank_tables:
    rank_tables[table].to_csv(f'./tables/{table}.csv', index=False, line_terminator='\n')

table_names = pd.DataFrame(rank_tables.keys())
table_names.to_csv('./tables/table_names.csv', index=False, line_terminator='\n')

