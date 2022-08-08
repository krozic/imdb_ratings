from get_movie_rank import get_movie_rank, get_movie_info, highlight_rating
from plotly_creator import plot_genre_dist, plot_movie_rank
from imdb_search import imdb_search
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc

# import data:
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


chosen_movie = dbc.Row(
    [
        html.Div(
            [
                html.H3(id='movie_title', children='', style={'textAlign': 'center'}),
            ],
            # className="d-grid gap-2",
        ),
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
)

query_group = dbc.Row(
    [
        html.Div(
            [
                # html.Div(id='search_text', children='Enter a search query:'),
                dbc.Input(id='query_input', placeholder='IMDB Search Query', type='text'),
                dbc.Button('Search', id='query_clicks', n_clicks=0, color='secondary', className='me-1'),
            ],
            className="d-grid gap-2",
        ),
        html.Div(
            [
                html.Br(),
                dbc.RadioItems(
                    id='query_choice',
                    # className='btn-group-vertical',
                    # inputClassName='btn-check',
                    # labelClassName='btn btn-light btn-outline-primary',
                    labelCheckedClassName='active',
                    options=[],
                    value=1,
                ),
                html.Div(id='output2'),
                # dbc.Button('Search', id='submit-query', n_clicks=0, color='secondary', className='me-1'),
            ],
            className='radio-group d-grid gap-2 d-md-block',
        ),
    ],
)

url_search = dbc.Row(
    [
        html.Div(
            [
                # html.Div(id='output', children='Enter a link and press submit:'),
                dbc.Input(id='url_input', placeholder='IMDB URL', type='text'),
                dbc.Button('Submit', id='submit-val', n_clicks=0, color='secondary', className='me-1'),
            ],
            className="d-grid gap-2",
        ),
    ]
)

plot_settings = dbc.Row(
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
)

accordion = html.Div(
    [
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    query_group,
                    title="Search Query",
                    item_id="query",
                ),
                dbc.AccordionItem(
                    url_search,
                    title="IMDB URL Search",
                    item_id="url",
                ),
            ],
            id="accordion",
            active_item="query",
        ),
        html.Div(id="accordion-contents", className="mt-3"),
    ]
)

sidebar_title = dbc.Row(
    [
        html.H3("Film Search", className="display-6"),
    ],
    style={"height": "5vh"}, className='bg-primary text-white'
)

references = dbc.Row(
    [
        html.Div(
            [
                html.A(href='https://github.com/krozic/imdb_ratings',
                       children='Source code can be found on my github')
            ],
        ),
    ],
    style={'height': '70vh'}
)

sidebar = html.Div(
    [
        sidebar_title,
        html.Br(),
        chosen_movie,
        html.Br(),
        html.Br(),
        # html.Hr(),
        accordion,
        # query_group,
        # url_search,
        # html.Br(),
        html.Hr(),
        plot_settings,
        # chosen_movie,
        # html.Br(),
        # html.Br(),
        html.Hr(),
        references,
    ],
)

# dash_data_table = dash_table.DataTable(
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

content = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    html.H1('Film Rank by Genre',
                            style={'textAlign': 'center'},
                            className="display-5"),
                ],
                justify='center'
            ),
            # plot_settings,
            dbc.Row(
                [
                    dcc.Graph(id='ratings_distribution',),
                ],
            ),
            html.Br(),
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
            # dash_data_table,
        ]
    ),
)


app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='bg-light'),
                dbc.Col(content, width=9),
                dcc.Store(id='intermediate_values', data={'past_query': 0,
                                                          'options': [],
                                                          'past_url': 0,
                                                          'most_recent': '',
                                                          'accordion': ''
                                                          })
            ]
        ),
    ],
    fluid=True
)

@app.callback(
    Output('intermediate_values', 'data'),
    Output('query_choice', 'options'),
    [Input('intermediate_values', 'data'),
    Input('accordion', 'active_item'),
    Input('query_clicks', 'n_clicks'),
    State('query_input', 'value'),
    Input('submit-val', 'n_clicks'),
     ]

)
def update_choices(data, accordion, query_clicks, query_input, n_clicks):
    if query_clicks > data['past_query']:
        data['options'] = imdb_search(query_input)
        data['past_query'] += 1
        data['most_recent'] = 'query'
    if n_clicks > data['past_url']:
        data['past_url'] += 1
        data['most_recent'] = 'url'
    if accordion != None:
        data['accordion'] = accordion

    return data, data['options']


@app.callback(
    [Output('tbl1', 'children'),
     # Output('tbl', 'data'),
     # Output('tbl', 'columns'),
     Output('movie_title', 'children'),
     Output('poster', 'src'),
     Output('imdb_rating', 'children'),
     Output('imdb_rating', 'className'),
     Output('rt_rating', 'children'),
     Output('rt_rating', 'className'),
     Output('mc_rating', 'children'),
     Output('mc_rating', 'className'),
     Output('ratings_distribution', 'figure')],
    Input('intermediate_values', 'data'),
    Input('submit-val', 'n_clicks'),
    Input('rating_choice', 'value'),
    Input('isolate_query', 'value'),
    State('query_input', 'value'),
    Input('query_clicks', 'n_clicks'),
    Input('query_choice', 'value'),
    State('url_input', 'value'),
)

def update_output(data, n_clicks, rating_choice, isolate_query, query_input, query_clicks, query_choice, url_input):
    if (n_clicks == 0) and (query_clicks == 0):
        fig = plot_genre_dist(rank_tables, rating_choice)
        return '', '', '', '', '', '', '', '', '', fig
    else:
        url = url_input
        highlighter = highlight_rating(rating_choice)
        if data['accordion'] == 'query':
            movie_info = get_movie_info(query_choice, query=True)
        elif data['accordion'] == 'url':
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
