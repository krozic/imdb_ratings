from get_movie_rank import get_movie_rank, get_movie_info, highlight_rating
from plotly_creator import plot_genre_dist, plot_movie_rank
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc

# import data:
movie_rank = pd.DataFrame({'': [''], '': ['']})

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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

sidebar = html.Div(
    [
        dbc.Row(
            [
                html.H3("Film Search", className="display-6"),
            ],
            style={"height": "5vh"}, className='bg-primary text-white'
        ),
        dbc.Row(
            [
                html.Div(
                    [
                        html.Br(),
                        html.Div(id='output', children='Enter a link and press submit:'),
                        dbc.Input(id='url_input', placeholder='IMDB URL', type='text'),
                        dbc.Button('Submit', id='submit-val', n_clicks=0, color='secondary', className='me-1'),
                    ],
                    className="d-grid gap-2",
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
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
                html.Div(
                    [
                        html.Br(),
                        dbc.Checkbox(
                            id='isolate_query',
                            label='Isolate query traces',
                            value=False,
                        ),
                    ],
                ),
            ],
        ),
        html.Hr(),
        dbc.Row(
            [
                html.Div(
                    [
                        html.Br(),
                        html.H3(id='movie_title', children='', style={'textAlign': 'center'}),
                    ],
                    # className="d-grid gap-2",
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(id='poster', src='')
                    ],
                    width=7
                ),
                dbc.Col(
                    [

                    ],
                    width=1
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        html.B(id='imdb_rating', children='', className=''),
                                        html.B(id='rt_rating', children='', className=''),
                                        html.B(id='mc_rating', children='', className=''),
                                    ],
                                    # align='center',
                                ),
                            ],
                            # className='pad-row',
                        ),
                    ],
                    width=4,
                    align='center',
                ),
            ],
        ),
        html.Br(),
        html.Br(),
        html.Hr(),
        dbc.Row(
            [
                html.Div(
                    [
                        # html.Br(),
                        html.A(href='https://github.com/krozic/imdb_ratings',
                               children='Source code can be found on my github')
                    ],
                ),
            ],
            style={'height':'70vh'}
        ),
    ],
)

content = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1('Film Rank by Genre',
                                    style={'textAlign': 'center'},
                                    className="display-5"),
                        ],
                        width=12
                    )
                ],
                justify='center'
            ),
            dbc.Row(
                [
                    dcc.Graph(id='ratings_distribution',),
                ],
            ),
            dbc.Row(
                [
                    html.Br()
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            # html.H1(id='movie_title', children=''),
                        ]
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            # html.Img(id='poster', src='')
                        ],
                        # width=6
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    html.Br(),
                                    html.H3(id='rating', children='')
                                ]
                            ),
                            dbc.Row(
                                [
                                    html.Div(id='tbl1'),
                                    # dbc.Table.from_dataframe(movie_rank, id='tbl1'),
                                ]
                            ),
                            # dash_table.DataTable(
                            #     movie_rank.to_dict('records'),
                            #     [{'name': i, 'id': i} for i in movie_rank.columns],
                            #     id='tbl',
                            #     sort_action='native',
                            #     style_header_conditional=[{
                            #         'if': {'column_id': ''},
                            #         'backgroundColor': 'rgb(123, 138, 139)',
                            #         'color': 'white'
                            #     }],
                            # ),
                        ],
                        width=12
                    ),
                    html.Br()
                ]
            ),
        ]
    ),
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='bg-light'),
                dbc.Col(content, width=9)
            ]
        ),
    ],
    fluid=True
)

@app.callback(
    [Output('tbl1', 'children'),
     # Output('tbl', 'data'),
     # Output('tbl', 'columns'),
     Output('movie_title', 'children'),
     Output('poster', 'src'),
     # Output('rating', 'children'),
     Output('imdb_rating', 'children'),
     Output('imdb_rating', 'className'),
     Output('rt_rating', 'children'),
     Output('rt_rating', 'className'),
     Output('mc_rating', 'children'),
     Output('mc_rating', 'className'),
     Output('ratings_distribution', 'figure')],
    Input('submit-val', 'n_clicks'),
    Input('rating_choice', 'value'),
    Input('isolate_query', 'value'),
    State('url_input', 'value'),
)

def update_output(n_clicks, rating_choice, isolate_query, url_input):
    # genre_rank = rank_tables[f'{rating_choice}_genre_rank']
    # genre_medians = rank_tables[f'{rating_choice}_genre_medians']
    if n_clicks == 0:
        movie_rank = pd.DataFrame({'Genre': [' '], 'Rank': [' ']})
        fig = plot_genre_dist(rank_tables, rating_choice)
        # fig = plot_genre_dist(genre_rank, genre_medians)
        return '', '', '', '', '', '', '', '', '', fig
    else:
        url = url_input
        highlighter = highlight_rating(rating_choice)
        movie_info = get_movie_info(url)
        movie_rank = get_movie_rank(movie_info, rank_tables)
        fig = plot_movie_rank(movie_info, movie_rank, rank_tables, rating_choice, isolate_query)
        return dbc.Table.from_dataframe(movie_rank, hover=True), \
               movie_info['title'], \
               movie_info['poster'], \
               f'IMDB: {movie_info["imdb"]}', highlighter['imdb'], \
               f'RT: {movie_info["rt"]}', highlighter['rt'], \
               f'MC: {movie_info["mc"]}', highlighter['mc'], \
               fig

if __name__ == '__main__':
    app.run_server(debug=True)