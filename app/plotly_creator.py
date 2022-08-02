import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any

# with open('./tables/genre_rank.csv', 'r') as filehandle:
#     genre_rank = pd.read_csv(filehandle)
#
# with open('./tables/genre_medians.csv', 'r') as filehandle:
#     genre_medians = pd.read_csv(filehandle)
#
def plot_genre_dist(genre_rank: pd.DataFrame, genre_medians: pd.DataFrame):
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
        title='Rating Distribution',
        xaxis_title='User Rating',
        yaxis_title='Percent Rank',
        font=dict(
            size=18,
        )
    )
    return fig

def plot_movie_rank(movie_info: Dict[str, Any], movie_rank: pd.DataFrame, genre_rank: pd.DataFrame, genre_medians: pd.DataFrame, rating_choice: str):
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
        title='Rating Distribution',
        xaxis_title='User Rating',
        yaxis_title='Percent Rank',
        font=dict(
            size=18,
        )
    )
    return fig
