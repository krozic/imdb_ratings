import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any

def plot_genre_dist(rank_tables: Dict[str, pd.DataFrame], rating_choice: str):
    """
    Takes rank_tables Dict of dataframes and rating_choice as input.
    Returns a plot of rating distribution categorized by genre, colored by median.
    """
    rating_name = {
        'imdb': 'IMDB',
        'rt': 'Tomatometer',
        'mc': 'Metascore'
    }
    genre_rank = rank_tables[f'{rating_choice}_genre_rank']
    genre_medians = rank_tables[f'{rating_choice}_genre_medians']
    fig = go.Figure()
    genres = genre_medians['genre']
    color_pal = px.colors.sample_colorscale('Turbo_r', len(genres))
    genre_color = {genres[color_pal.index(col)]:col for col in color_pal}
    for genre in genres:
        genre_plot = genre_rank[['rating', genre]].dropna()
        fig.add_trace(go.Scatter(x=genre_plot['rating'],
                                 y=genre_plot[genre],
                                 name=genre,
                                 mode='lines',
                                 opacity=0.5,
                                 line=go.scatter.Line(color=genre_color[genre])
                                 )
                      )
    fig.update_layout(
        title=f'{rating_name[rating_choice]} Rating Distribution',
        xaxis_title='User Rating',
        yaxis_title='Percent Rank',
        font=dict(
            size=16,
        )
    )
    return fig

def plot_movie_rank(movie_info: Dict[str, Any], movie_rank: pd.DataFrame, rank_tables: Dict[str, pd.DataFrame], rating_choice: str, isolate_query: bool):
    """
    Uses movie_info and movie_rank to plot the films rating and genre to visualize how it ranks in its genres.
    isolate_query is used to plot only the traces for the films genres
    """
    rating_name = {
        'imdb': 'IMDB',
        'rt': 'Tomatometer',
        'mc': 'Metascore'
    }
    genre_rank = rank_tables[f'{rating_choice}_genre_rank']
    genre_medians = rank_tables[f'{rating_choice}_genre_medians']
    fig = go.Figure()
    genres = genre_medians['genre']
    color_pal = px.colors.sample_colorscale('Turbo_r', len(genres))
    genre_color = {genres[color_pal.index(col)]:col for col in color_pal}
    for genre in genres:
        genre_plot = genre_rank[['rating', genre]].dropna()
        fig.add_trace(go.Scatter(x=genre_plot['rating'],
                                 y=genre_plot[genre],
                                 name=genre,
                                 mode='lines',
                                 opacity=0.5,
                                 line=go.scatter.Line(color=genre_color[genre])
                                 )
                      )

    if isolate_query:
        genres = list(movie_rank['Genre'])
        fig.for_each_trace(lambda trace: trace.update(visible='legendonly')
        if trace.name not in genres else ())
    x = []
    for genre in genres:
        x.append(movie_info[rating_choice])

    if rating_choice == 'imdb':
        rank = 'IMDB Rank'
    elif rating_choice == 'rt':
        rank = 'Tomatometer Rank'
    elif rating_choice == 'mc':
        rank = 'Metascore Rank'
    fig.add_trace(go.Scatter(x=x,
                             y=movie_rank[rank],
                             name='query',
                             mode='markers',
                             marker=dict(size=[10, 10, 10], color=[3, 3, 3])))
    fig.update_layout(
        title=f'{rating_name[rating_choice]} Rating Distribution',
        xaxis_title='User Rating',
        yaxis_title='Percent Rank',
        font=dict(
            size=16,
        )
    )
    return fig

