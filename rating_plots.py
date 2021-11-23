"""
Created on Mon Nov 22 01:12:34 2021

@author: kyler
"""

import pyodbc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

# Creating Table of Stats

medianVals = {}
for genre in genres:
    genre_db = db[db.genres.str.contains(genre, regex=True, na=False)]
    genre_db['movierank'] = ((np.arange(len(genre_db))+1)/len(genre_db)*100).round(2)
    median = genre_db[genre_db.movierank<52][genre_db.movierank>48].averageRating.mean()
#    medianVals[genre] = median
    medianVals.setdefault('genre', []).append(genre)
    medianVals.setdefault('median', []).append(median)

medianVals = pd.DataFrame(medianVals).sort_values('median')

NUM_COLORS = len(genres)

cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

for genre in medianVals.genre:
    genre_db = db[db.genres.str.contains(genre, regex=True, na=False)]
    genre_db['movierank'] = ((np.arange(len(genre_db))+1)/len(genre_db)*100).round(2)
    genre_db = genre_db.groupby('averageRating')['movierank'].mean()
    genre_db = genre_db.reset_index()
    ax.plot(genre_db.averageRating, genre_db.movierank, label=genre, alpha=0.4)
    if genre == 'Western':
        plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
        plt.ylabel('Percent Rank')
        plt.xlabel('User Rating')
        plt.xticks(np.arange(0, 11, 1))
        plt.yticks(np.arange(0, 101, 10))
        plt.title('Rating Distribution')
        plt.savefig('rating_distribution.png', dpi=600, bbox_inches='tight')









horror_sql = '''
SELECT * FROM HorrorRank;
'''

horror_db = pd.read_sql(horror_sql, cnxn)
horror_rating = horror_db.groupby('averageRating')['movierank'].mean()
horror_rating = horror_rating.reset_index()

plt.plot(horror_rating['averageRating'], horror_rating['movierank'])

history_sql = '''
SELECT * FROM HistoryRank;
'''

history_db = pd.read_sql(history_sql, cnxn)
history_rating = history_db.groupby('averageRating')['movierank'].mean()
history_rating = history_rating.reset_index()

plt.plot(history_rating['averageRating'], history_rating['movierank'])

plt.show()