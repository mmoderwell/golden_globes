import pandas as pd
import re
import nltk

# Python program to find the k most frequent words from data set 
from collections import Counter 

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

data_url = "./data/gg2020.json"
df = pd.read_json(data_url, orient='columns', lines=True)

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def getProperNouns(text):
	names = []
	tokenized = preprocess(text)
	for word in tokenized:
		if word[1] == 'NNP' or word[0].isnumeric():
			names.append(word[0])
			# add to master list
		else:
			names.append(':')

	answer  = [] # final answer
	partial = [] # partial answer
	for e in names:
	    if e == ':':           # if current element is an empty string … 
	        if partial:       # … and there's a partial answer
	            answer.append(' '.join(partial)) # join and append partial answer
	            partial = []  # reset partial answer
	    else:                 # otherwise it's a new element of partial answer
	        partial.append(e) # add it to partial answer
	else:                     # this part executes after the loop exits
	    if partial:           # if one partial answer is left
	        answer.append(' '.join(partial)) # add it to final answer
	return answer


skip_list = ["Golden", "Globes", "Golden Globes", "Host", "Hollywood", "Golden Globe", 
"Best", "Comedy", "Best Picture", "Best Motion Picture", "Actor", "Actress", "Film", 
"Motion Picture", "Motion", "Performance", "Drama", "Comedy", "Director", "Musical", 
"Best Performance", "Annual Golden Globe Awards", "Best Director", "BEST PICTURE", 
"Look", "Btw", "’", "2015", "2016", "2017", "2018", "2019", "Best Actor", "Best Actress",
 "Golden Globes 2020", "2020 Golden Globes"]

def getAwardWinnerPerson(award, title, relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list and not word[0].isnumeric():
			results.append(word[0])

	best = results[0]
	print(title, best)


def getBestDramaPicture(relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list:
			results.append(word[0])

	best = results[0]
	print('Best Picture - Drama:', best)
	# print(results)

def getBestComedyPicture(relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list:
			results.append(word[0])

	best = results[0]
	print('Best Picture - Comedy:', best)


host_list = []
master_name_list = []
master_award_list = []
master_nominee_list = []
master_winner_list = []
master_host_list = []

# Awards lists
best_drama_picture_list = []
best_comedy_picture_list = []
best_supporting_role_list = []
best_supporting_actress_list = []
best_director_list = []

best_comedy_actress_list = []
best_comedy_actor_list = []

best_drama_actor_list = []
best_drama_actress_list = []

best_dressed_list = []

for tweet in df.head(60000).iterrows():
	text = tweet[1].text

	# pull out the urls and remove them
	text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
	# pull out the hashtags
	hashtags = re.findall(r'(?i)\#\w+', text)
	# take them out for now, can do something with them later
	text = re.sub(r'(?i)\#\w+', '', text)
	# pull out all the @'s
	mentions = re.findall(r'(?i)\@\w+', text)
	text = re.sub(r'(?i)\@\w+', '', text)
	# pull out all of the emojis
	text = re.sub(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])', '', text)

	titles = re.findall(r'^(.*)[\s]+[\s]?(.*)?', text)
	
	# get the proper nouns for the tweet
	nouns = getProperNouns(text)
	master_name_list += nouns

	text = text.lower()

	# build up our lists
	if "winner" in text:
		master_winner_list += nouns

	if "nominee" in text:
		master_nominee_list += nouns

	if "award" in text:
		master_award_list += nouns

	if "host" in text:
		host_list += nouns

	if "drama" in text and ("best motion picture" in text or "best picture" in text):
		best_drama_picture_list += nouns

	if "drama" in text and "actor" in text and ("performance" in text or "best performance" in text):
		best_drama_actor_list += nouns

	if "drama" in text and "actress" in text and ("performance" in text or "best performance" in text):
		best_drama_actress_list += nouns

	if "comedy" in text and ("best motion picture" in text or "best picture" in text):
		best_comedy_picture_list += nouns

	if "best" in text and "actor" in text and ("supporting" in text or "supporting role" in text):
		best_supporting_role_list += nouns

	if "best" in text and "actress" in text and ("supporting" in text or "supporting role" in text):
		best_supporting_actress_list += nouns

	if "best" in text and ("director" in text or "best director" in text):
		best_director_list += nouns

	if "actress" in text and "best" in text and ("comedy" in text or "musical" in text) and "television" not in text:
		best_comedy_actress_list += nouns

	if "actor" in text and "best" in text and ("comedy" in text or "musical" in text) and "television" not in text:
		best_comedy_actor_list += nouns

	if "dressed" in text and "best" in text:
		best_dressed_list += nouns
		# print (text, '\n')

print ('\n')
# get the most common name in the list
getAwardWinnerPerson("", "Host:", host_list)

getBestDramaPicture(best_drama_picture_list)
getBestComedyPicture(best_comedy_picture_list)

getAwardWinnerPerson("", "Best Actor in a Supporting Role:", best_supporting_role_list)
getAwardWinnerPerson("", "Best Actress in a Supporting Role:", best_supporting_actress_list)

getAwardWinnerPerson("", "Best Director:", best_director_list)

getAwardWinnerPerson("", "Best Actress - Drama:", best_drama_actress_list)
getAwardWinnerPerson("", "Best Actor - Drama:", best_drama_actor_list)

getAwardWinnerPerson("", "Best Actress - Musical or Comedy:", best_comedy_actress_list)
getAwardWinnerPerson("", "Best Actor - Musical or Comedy:", best_comedy_actor_list)

getAwardWinnerPerson("", "Best Dressed:", best_dressed_list)


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

# print (recent_top_movies)
# print (actors)



# textblob
# TextBlob("I loved it")
# blob.sent.sentiment