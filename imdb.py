# https://travis-ci.org/alberanid/imdbpy
# build is currently failing, hopefully is resolved soon


from imdb import IMDb

# create an instance of the IMDb class
ia = IMDb()
top_movies = ia.get_top250_movies()
print ('Got top movies')
recent_top_movies = []

for movie in top_movies:
	if (movie['year'] in [2013, 2014, 2015, 2016, 2017, 2018, 2019]):
		recent_top_movies.append(movie)

actors = []
print ('Getting actors\n')
for movie in recent_top_movies:
	the_movie = ia.get_movie(movie.movieID)
	if the_movie:
		cast = the_movie.get('cast')
		topActors = 8
		for actor in cast[0:topActors]:
			actors.append(actor['name'])

print (recent_top_movies)
print (actors)