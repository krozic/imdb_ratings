from get_movie_rank import get_movie_rank, get_movie_info
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc

# import data:
genre_rank = pd.read_csv('./tables/genre_rank.csv')
df = pd.DataFrame({'Genre': [' '], 'Rank': [' ']})

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
            dcc.Input(id='url_input', placeholder='IMDB URL', type='text'),
            html.Button('Submit', id='submit-val', n_clicks=0),
            html.Div(id='output', children='Enter a link and press submit'),
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H1(id='movie_title', children='')
        ], width=6),
        dbc.Col([
            html.H1(id='filler', children='')
        ], width=6),
    ]),
    dbc.Row([
        dbc.Col([
            html.Img(id='poster', src='')
        ], width=6),
        dbc.Col([
            dash_table.DataTable(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns], id='tbl'),
        ], width=6)
    ])
])

@app.callback(
    [Output('tbl', 'data'), Output('tbl', 'columns'), Output('movie_title', 'children'), Output('poster', 'src')],
    Input('submit-val', 'n_clicks'),
    State('url_input', 'value'),
)

def update_output(n_clicks, url_input):
    if n_clicks == 0:
        df = pd.DataFrame({'Genre': [' '], 'Rank': [' ']})
        return df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns], '', ''
    else:
        url = url_input
        movie_info = get_movie_info(url)
        df = get_movie_rank(movie_info, genre_rank)
        return df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns], movie_info['title'], movie_info['poster']

if __name__ == '__main__':
    app.run_server(debug=True)