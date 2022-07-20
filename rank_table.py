import pyodbc
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

genre_rank = None
for genre in genres:
    genre_db = db[db.genres.str.contains(genre, regex=True, na=False)]
    genre_db[genre] = ((np.arange(len(genre_db)) + 1) / len(genre_db) * 100).round(2)
    genre_db = genre_db.groupby('averageRating')[genre].mean().round(1)
    genre_db = genre_db.reset_index()
    if genre_rank is not None:
        genre_rank = pd.merge(genre_rank, genre_db, how='outer', on='averageRating')
    else:
        genre_rank = genre_db

genre_rank = genre_rank.sort_values('averageRating')
with open('./tables/genre_rank.csv', 'w') as filehandle:
    genre_rank.to_csv(filehandle, index=False, line_terminator='\n')

