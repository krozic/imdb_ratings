from my_secrets import api_key
import pyodbc
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
plt.style.use('ggplot')

# define components of our connection string
DRIVER = '{ODBC DRIVER 17 for SQL Server}'
SERVER = 'DESKTOP-MH2FIN2\SQLEXPRESS'
DATABASE = 'IMDBRatings'

# define our connection string
CONNECTION_STRING = '''
Driver={driver};
Server={server};
Database={database};
Trusted_Connection=yes;
'''.format(
    driver=DRIVER,
    server=SERVER,
    database=DATABASE
)

# Connect to database
cnxn = pyodbc.connect(CONNECTION_STRING)

# Create the connection cursor
cursor = cnxn.cursor()

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

# Selecting data and plotting
ratings_sql = '''
SELECT * FROM PopularRatings
ORDER BY averageRating ASC, numVotes ASC;
'''

db = pd.read_sql(ratings_sql, cnxn)
db['averageRating'] = db['averageRating'].round(1)


# Accessing
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
#     'Authorization': 'Bearer {token}'.format(token=token)
}

extra_ratings = pd.DataFrame(columns=['tconst', 'rt_rating', 'mc_rating'])
for i in range(len(db['tconst'])):
    movie = db['tconst'][i]
    r = requests.get(
        f'http://www.omdbapi.com/?i={movie}&apikey={api_key}', headers=headers)
    data = r.json()
    try:
        if data['Ratings'][1]['Source'] == 'Rotten Tomatoes':
            rt = data['Ratings'][1]['Value'].replace('%', '')
        else:
            rt = np.nan
    except:
        rt = np.nan
    try:
        if data['Metascore'] != 'N/A':
            mc = data['Metascore']
        else:
            mc = np.nan
    except:
        mc = np.nan
    print(i)
    print([movie, rt, mc])
    extra_ratings.loc[i] = [movie, rt, mc]

all_ratings = pd.merge(db, extra_ratings, how='left', on='tconst')

with open('./tables/extra_ratings.csv', 'w') as filehandle:
    extra_ratings.to_csv(filehandle, index=False, line_terminator='\n')

with open('./tables/all_ratings.csv', 'w') as filehandle:
    all_ratings.to_csv(filehandle, index=False, line_terminator='\n')


# movie = 'tt0378793'
# r = requests.get(
#     f'http://www.omdbapi.com/?i={movie}&apikey={api_key}', headers=headers)
# data = r.json()
#
# rt = data['Ratings'][1]['Value'].replace('%', '')
# mc = data['Metascore']

















