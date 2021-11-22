## IMDB Ratings

### Synopsis

The intent of this project is to compare the average imdb ratings between genres visualize the distribution of ratings for each genre in an effort to translate an IMDB rating to a genre specific ranking. 

The 'title.basics.tsv' and 'title.ratings.tsv' data were sourced from IMDB's openly available [datasets](https://www.imdb.com/interfaces/) and the 'IMDB movies.csv' data was sourced from Stefano Leone's [IMDb extensive dataset](https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset) to categorize films based on country of origin.

### Method

These three tables were loaded into Microsoft SQL Server which was used for exploratory data analysis and subsequent creation of the tables necessary for visualization.

The python package `pyodbc` was then used to load the tables from this database into `pandas` for visualization in `matplotlib`.

---

To do:

- Make a table for all other genres
- Create line plots containing each genre
- Create table of genre rating means