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
"Look", "Btw", "’", "2015", "2016", "2017", "2018", "2019"]

def getHost(relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(10)
	results = []
	for word in most_occur:
		if word[0] not in skip_list and not word[0].isnumeric():
			results.append(word[0])
	host = results[0]
	print('Host:', host)
	# print(most_occur)
	return host

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

def getBestDramaActor(relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list and not word[0].isnumeric():
			results.append(word[0])

	best = results[0]
	print('Best Performance by Actor - Drama:', best)

def getBestDramaActress(relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list and not word[0].isnumeric():
			results.append(word[0])

	best = results[0]
	print('Best Performance by Actress - Drama:', best)

def getBestComedyPicture(relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list:
			results.append(word[0])

	best = results[0]
	print('Best Picture - Comedy:', best)

def getBestSupportingRole(relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list and not word[0].isnumeric():
			results.append(word[0])

	best = results[0]
	print('Best Actor in Supporting Role:', best)

def getBestSupportingActress(relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list and not word[0].isnumeric():
			results.append(word[0])

	best = results[0]
	print('Best Actress in Supporting Role:', best)

def getBestDirector(relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list and not word[0].isnumeric():
			results.append(word[0])

	best = results[0]
	print('Best Director:', best)


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

best_drama_actor_list = []
best_drama_actress_list = []

for tweet in df.head(100000).iterrows():
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
	# print (answer,'\n')

	# build up our lists
	if "winner" in text:
		master_winner_list += nouns

	if "nominee" in text:
		master_nominee_list += nouns

	if "award" in text:
		master_award_list += nouns

	if "host" in text:
		master_host_list += nouns

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
		# print (text, '\n')

# get the most common name in the list
getHost(master_host_list)
# 
getBestDramaPicture(best_drama_picture_list)
getBestComedyPicture(best_comedy_picture_list)
getBestSupportingRole(best_supporting_role_list)
getBestSupportingActress(best_supporting_actress_list)
getBestDirector(best_director_list)

getBestDramaActress(best_drama_actress_list)
getBestDramaActor(best_drama_actor_list)

# Pass the split_it list to instance of Counter class. 
Counter1 = Counter(master_name_list)
most_occur = Counter1.most_common(10)
# print(most_occur)

Counter2 = Counter(master_award_list)
most_occur = Counter2.most_common(10)
# print(most_occur)

Counter3 = Counter(master_winner_list)
most_occur = Counter3.most_common(10)   
# print(most_occur)

Counter4 = Counter(master_nominee_list)
most_occur = Counter4.most_common(10) 
# print(most_occur)





# from imdb import IMDb

# # create an instance of the IMDb class
# ia = IMDb()
# top_movies = ia.get_top250_movies()

# for movie in top_movies:
# 	if (movie['year'] == 2016):
# 		print (movie['title'], movie['year'])

# movies = ia.search_keyword('user_rating=7.0%2C')
# print (movies)


# def getHost(text):
# 	if 'host' in text and 'next year' not in text:

