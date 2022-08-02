import pandas as pd
import matplotlib.pyplot as plt

all_ratings = pd.read_csv('./tables/all_ratings.csv')

def top_50_films(all_ratings: pd.DataFrame, rating_system: str) -> pd.DataFrame:
    rating_options = ['averageRating', 'rt_rating', 'mc_rating']
    if rating_system not in rating_options:
        print(f'Invalid rating system provided. Choose one of {rating_options}.')
        return
    top_films = all_ratings.dropna(subset=rating_system).sort_values(rating_system)[['primaryTitle', rating_system]].tail(n=50)
    return top_films

def bottom_50_films(all_ratings: pd.DataFrame, rating_system: str) -> pd.DataFrame:
    rating_options = ['averageRating', 'rt_rating', 'mc_rating']
    if rating_system not in rating_options:
        print(f'Invalid rating system provided. Choose one of {rating_options}.')
        return
    bottom_films = all_ratings.dropna(subset=rating_system).sort_values(rating_system)[['primaryTitle', rating_system]].head(n=50)
    return bottom_films

def count_per_score(all_ratings: pd.DataFrame, rating_system: str) -> pd.DataFrame:
    rating_options = ['averageRating', 'rt_rating', 'mc_rating']
    if rating_system not in rating_options:
        print(f'Invalid rating system provided. Choose one of {rating_options}.')
        return
    score_counts = all_ratings.groupby(rating_system, dropna=True)['tconst'].count().reset_index()
    return score_counts

def plt_score_counts(score_counts):
    x = score_counts[score_counts.columns[0]]
    y = score_counts[score_counts.columns[1]]
    width = (score_counts[score_counts.columns[0]].max()/100).round(1) * 0.8
    return plt.bar(x,y, width=width)

plt_score_counts(count_per_score(all_ratings, 'rt_rating'))
imdb_counts = count_per_score(all_ratings, 'averageRating')
rt_counts = count_per_score(all_ratings, 'rt_rating')
