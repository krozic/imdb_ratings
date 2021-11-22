"""
Created on Mon Nov 22 01:12:34 2021

@author: kyler
"""

import pyodbc
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

# Selecting data and plotting
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