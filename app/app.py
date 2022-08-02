from get_movie_rank import get_movie_rank, get_movie_info
from plotly_creator import plot_genre_dist, plot_movie_rank
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc

# import data:
movie_rank = pd.DataFrame({'Genre': [' '], 'Rank': [' ']})

table_names = pd.read_csv('./tables/table_names.csv')
table_names = [name for name in table_names['0']]

rank_tables = {}
for name in table_names:
    rank_tables[name] = pd.read_csv(f'./tables/{name}.csv')

rating_name = {
    'imdb': 'IMDB',
    'rt': 'Tomatometer',
    'mc': 'Metascore'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('IMDB Film Rank by Genre')
        ], width=12)
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            # html.Label('IMDB URL:'),
            html.Br(),
            dbc.Input(id='url_input', placeholder='IMDB URL', type='text'),
            # html.Br(),
            # dbc.Button('Submit', id='submit-val', n_clicks=0),
            html.Div(id='output', children='Enter a link and press submit'),
        ], width=5),
        dbc.Col([
            html.Br(),
            dbc.Button('Submit', id='submit-val', n_clicks=0),
        ]),
    ]),
    dbc.Row([
       html.Br()
    ]),
    dbc.Row([
        dbc.Col([
            # html.Br(),
            html.H1(id='movie_title', children=''),
        ]),
        # ], width=6),
        # dbc.Col([
        #     html.H1(id='filler', children='')
        # ], width=6),
    ]),
    dbc.Row([
        dbc.Col([
            # html.H1(id='movie_title', children=''),
            html.Img(id='poster', src='')
        ], width=6),
        dbc.Col([

            dbc.Row([
                html.Br(),
                html.H3(id='rating', children='')
            ]),
            dbc.Row([
                html.Div(id='tbl1'),
                # dbc.Table.from_dataframe(movie_rank, id='tbl1'),
            ]),
            # dash_table.DataTable(movie_rank.to_dict('records'), [{'name': i, 'id': i} for i in movie_rank.columns], id='tbl'),
        ], width=6),
        html.Br()
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Br(),
            html.Div(id='system_label', children='Choose Rating System:'),
            dcc.Dropdown(
                id='rating_choice',
                options={
                    'imdb': 'IMDB',
                    'rt': 'Rotten Tomatoes',
                    'mc': 'Metascore'
                },
                value='imdb',
                searchable=False,
                clearable=False
            ),
        ],width=5),
    ]),
    dbc.Row([
        dcc.Graph(id='ratings_distribution')
    ])
])

@app.callback(
    [Output('tbl1', 'children'),
     # Output('tbl', 'data'),
     # Output('tbl', 'columns'),
     Output('movie_title', 'children'),
     Output('poster', 'src'),
     Output('rating', 'children'),
     Output('ratings_distribution', 'figure')],
    Input('submit-val', 'n_clicks'),
    Input('rating_choice', 'value'),
    State('url_input', 'value'),
)

def update_output(n_clicks, rating_choice, url_input):
    genre_rank = rank_tables[f'{rating_choice}_genre_rank']
    genre_medians = rank_tables[f'{rating_choice}_genre_medians']
    if n_clicks == 0:
        movie_rank = pd.DataFrame({'Genre': [' '], 'Rank': [' ']})
        fig = plot_genre_dist(genre_rank, genre_medians)
        return '', '', '', '', fig
    else:
        url = url_input
        movie_info = get_movie_info(url)
        # movie_rank = get_movie_rank(movie_info, genre_rank)
        movie_rank = get_movie_rank(movie_info, rank_tables)
        fig = plot_movie_rank(movie_info, movie_rank, genre_rank, genre_medians, rating_choice)
        return dbc.Table.from_dataframe(movie_rank, hover=True), \
               movie_info['title'], \
               movie_info['poster'], \
               f'{rating_name[rating_choice]} Rating: {movie_info[rating_choice]}', \
               fig

if __name__ == '__main__':
    app.run_server(debug=True)