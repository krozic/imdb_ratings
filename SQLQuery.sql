
-- Categorizing films based on "popularity" level

SELECT tb.tconst, tb.primaryTitle, tb.titleType, tb.genres, tr.averageRating, tr.numVotes, --numVotes*averageRating AS metric,
	CASE WHEN tr.numVotes > 100000 THEN 'high'
			WHEN tr.numVotes > 50000 THEN 'medium'
			WHEN tr.numVotes > 10000 THEN 'low'
		ELSE 'verylow' END
		AS popularity
FROM IMDBRatings..TitleRatings AS tr
	LEFT JOIN IMDBRatings..TitleBasics AS tb
		ON tr.tconst = tb.tconst
WHERE (titleType = 'movie' OR titleType = 'tvMovie')
AND tb.genres LIKE '%Action%'
AND numVotes > 10000
ORDER BY averageRating ASC, numVotes ASC;
--ORDER BY popularity ASC, averageRating ASC;
--ORDER BY averageRating ASC, popularity ASC;
--ORDER BY metric ASC;

SELECT AVG(averageRating)
FROM IMDBRatings..TitleRatings AS tr
	LEFT JOIN IMDBRatings..TitleBasics AS tb
		ON tr.tconst = tb.tconst
WHERE (titleType = 'movie' OR titleType = 'tvMovie')
AND tb.genres LIKE '%Drama%'
AND numVotes > 10000;

--Playing around with ROW_NUMBER() to get a percent ranking

SELECT tb.tconst, tb.primaryTitle, tb.titleType, tb.genres, tr.averageRating, tr.numVotes, 
	ROW_NUMBER() OVER (
		ORDER BY averageRating ASC, numVotes ASC)/9635.0*100 AS percRank
FROM IMDBRatings..TitleRatings AS tr
	LEFT JOIN IMDBRatings..TitleBasics AS tb
		ON tr.tconst = tb.tconst
WHERE (titleType = 'movie' OR titleType = 'tvMovie')
AND numVotes > 10000;

--Using actual PERCENT_RANK() function

SELECT tb.tconst, tb.primaryTitle, tb.titleType, tb.genres, tr.averageRating, tr.numVotes, 
	PERCENT_RANK() OVER (
		ORDER BY averageRating ASC, numVotes ASC)*100 AS movierank
FROM IMDBRatings..TitleRatings AS tr
	LEFT JOIN IMDBRatings..TitleBasics AS tb
		ON tr.tconst = tb.tconst
WHERE (titleType = 'movie' OR titleType = 'tvMovie')
AND tb.genres LIKE '%Horror%'
AND numVotes > 10000;

-- Add country factor to control film location

SELECT tb.tconst, tb.primaryTitle, tb.titleType, tb.genres, tr.averageRating, tr.numVotes, te.country,
	PERCENT_RANK() OVER (
		ORDER BY averageRating ASC, numVotes ASC)*100 AS movierank
FROM IMDBRatings..TitleRatings AS tr
	LEFT JOIN IMDBRatings..TitleBasics AS tb
		ON tr.tconst = tb.tconst
	LEFT JOIN IMDBRatings..TitleExtras AS te
		ON tb.tconst = te.imdb_title_id
WHERE (titleType = 'movie' OR titleType = 'tvMovie')
AND te.country NOT LIKE '%India%'
--AND tb.genres LIKE '%Horror%'
AND numVotes > 10000;

-- Create View to categorize based on rating value

CREATE VIEW HorrorRank AS
SELECT tb.tconst, tb.primaryTitle, tb.titleType, tb.genres, tr.averageRating, tr.numVotes, te.country,
	PERCENT_RANK() OVER (
		ORDER BY averageRating ASC, numVotes ASC)*100 AS movierank
FROM IMDBRatings..TitleRatings AS tr
	LEFT JOIN IMDBRatings..TitleBasics AS tb
		ON tr.tconst = tb.tconst
	LEFT JOIN IMDBRatings..TitleExtras AS te
		ON tb.tconst = te.imdb_title_id
WHERE (titleType = 'movie' OR titleType = 'tvMovie')
AND te.country NOT LIKE '%India%'
AND tb.genres LIKE '%Horror%'
AND numVotes > 10000;

CREATE VIEW HistoryRank AS
SELECT tb.tconst, tb.primaryTitle, tb.titleType, tb.genres, tr.averageRating, tr.numVotes, te.country,
	PERCENT_RANK() OVER (
		ORDER BY averageRating ASC, numVotes ASC)*100 AS movierank
FROM IMDBRatings..TitleRatings AS tr
	LEFT JOIN IMDBRatings..TitleBasics AS tb
		ON tr.tconst = tb.tconst
	LEFT JOIN IMDBRatings..TitleExtras AS te
		ON tb.tconst = te.imdb_title_id
WHERE (titleType = 'movie' OR titleType = 'tvMovie')
AND te.country NOT LIKE '%India%'
AND tb.genres LIKE '%History%'
AND numVotes > 10000;

-- Group By movierank

SELECT averageRating, AVG(movierank)
FROM IMDBRatings..HorrorRank
GROUP BY averageRating

-- Show average rating per genre

SELECT AVG(tr.averageRating)
FROM IMDBRatings..TitleRatings AS tr
	LEFT JOIN IMDBRatings..TitleBasics AS tb
		ON tr.tconst = tb.tconst
	LEFT JOIN IMDBRatings..TitleExtras AS te
		ON tb.tconst = te.imdb_title_id
WHERE (titleType = 'movie' OR titleType = 'tvMovie')
AND te.country NOT LIKE '%India%'
AND tb.genres LIKE '%History%'
AND numVotes > 10000;

SELECT AVG(tr.averageRating)
FROM IMDBRatings..TitleRatings AS tr
	LEFT JOIN IMDBRatings..TitleBasics AS tb
		ON tr.tconst = tb.tconst
	LEFT JOIN IMDBRatings..TitleExtras AS te
		ON tb.tconst = te.imdb_title_id
WHERE (titleType = 'movie' OR titleType = 'tvMovie')
AND te.country NOT LIKE '%India%'
AND tb.genres LIKE '%Horror%'
AND numVotes > 10000;

-- Creating Genre column categories

SELECT 
	CASE WHEN tb.genres LIKE '%Horror%' THEN 'True' 
		ELSE 'False' END
		AS horror,
	CASE WHEN tb.genres LIKE '%Sci-Fi%' THEN 'True' 
		ELSE 'False' END
		AS scifi,
	CASE WHEN tb.genres LIKE '%Crime%' THEN 'True' 
		ELSE 'False' END
		AS crime,
	CASE WHEN tb.genres LIKE '%Drama%' THEN 'True' 
		ELSE 'False' END
		AS drama,
	CASE WHEN tb.genres LIKE '%Romance%' THEN 'True' 
		ELSE 'False' END
		AS romance,
	CASE WHEN tb.genres LIKE '%Action%' THEN 'True' 
		ELSE 'False' END
		AS action,
	CASE WHEN tb.genres LIKE '%Adventure%' THEN 'True' 
		ELSE 'False' END
		AS adventure,
	CASE WHEN tb.genres LIKE '%Comedy%' THEN 'True' 
		ELSE 'False' END
		AS comedy,
	CASE WHEN tb.genres LIKE '%Thriller%' THEN 'True' 
		ELSE 'False' END
		AS thriller,
	CASE WHEN tb.genres LIKE '%History%' THEN 'True' 
		ELSE 'False' END
		AS history,
	CASE WHEN tb.genres LIKE '%Biography%' THEN 'True' 
		ELSE 'False' END
		AS biography
FROM IMDBRatings..TitleRatings AS tr
	LEFT JOIN IMDBRatings..TitleBasics AS tb
		ON tr.tconst = tb.tconst
	LEFT JOIN IMDBRatings..TitleExtras AS te
		ON tb.tconst = te.imdb_title_id

-- Creating views to plot results in python

CREATE VIEW TotalRank AS

SELECT tb.tconst, tb.primaryTitle, tb.titleType, tb.genres, tr.averageRating, tr.numVotes, te.country,
	PERCENT_RANK() OVER (
		ORDER BY averageRating ASC, numVotes ASC)*100 AS movierank
FROM IMDBRatings..TitleRatings AS tr
	LEFT JOIN IMDBRatings..TitleBasics AS tb
		ON tr.tconst = tb.tconst
	LEFT JOIN IMDBRatings..TitleExtras AS te
		ON tb.tconst = te.imdb_title_id
WHERE (titleType = 'movie' OR titleType = 'tvMovie')
AND te.country NOT LIKE '%India%'
-- AND tb.genres LIKE '%Horror%'
-- AND numVotes > 10000;