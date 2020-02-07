import pandas as pd
import re
import nltk
import json

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
	return best

def getAwardWinnerMovie(award, title, relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list:
			results.append(word[0])

	best = results[0]
	print(title, best)
	return best

lists = {}
# Host list
lists["host"] = {}
# Best director lists
lists["best director - motion picture"] = {}
# Random best lists
lists["best screenplay - motion picture"] = {}
lists["best original score - motion picture"] = {}
lists["best foreign language film"] = {}
lists["best animated feature film"] = {}
lists["best original song - motion picture"] = {}
# 
lists["cecil b. demille award"] = {}
# 
lists["best motion picture - drama"] = {}
lists["best motion picture - comedy or musical"] = {}

lists["best television series - drama"] = {}
lists["best television series - comedy or musical"] = {}
# 
lists["best mini-series or motion picture made for television"] = {}

# Best performance lists
lists["best performance by an actress in a motion picture - comedy or musical"] = {}
lists["best performance by an actor in a motion picture - comedy or musical"] = {}

lists["best performance by an actor in a television series - comedy or musical"] = {}
lists["best performance by an actress in a television series - comedy or musical"] = {}

lists["best performance by an actor in a supporting role in a motion picture"] = {}
lists["best performance by an actress in a supporting role in a motion picture"] = {}

lists["best performance by an actor in a supporting role in a series, mini-series or motion picture made for television"] = {}
lists["best performance by an actress in a supporting role in a series, mini-series or motion picture made for television"] = {}

lists["best performance by an actor in a mini-series or motion picture made for television"] = {}
lists["best performance by an actress in a mini-series or motion picture made for television"] = {}

lists["best performance by an actor in a motion picture - drama"] = {}
lists["best performance by an actress in a motion picture - drama"] = {}

lists["best performance by an actor in a television series - drama"] = {}
lists["best performance by an actress in a television series - drama"] = {}

# Initialize all the different kinds of fields for each award
for key in lists:
	lists[key]["winner"] = []
	lists[key]["nominees"] = []
	lists[key]["presenters"] = []


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

for tweet in df.head(6000).itertuples():
	text = tweet[3]

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
	# if "winner" in text:
	# 	master_winner_list += nouns

	# if "nominee" in text:
	# 	master_nominee_list += nouns

	# if "award" in text:
	# 	master_award_list += nouns

# best screenplay - motion picture
# best director - motion picture
# best original score - motion picture
# best motion picture - drama
# best original song - motion picture
# best motion picture - comedy or musical
# best animated feature film

# best foreign language film
# best mini-series or motion picture made for television
# cecil b. demille award

# best television series - drama
# best television series - comedy or musical

# best performance by an actress in a motion picture - comedy or musical
# best performance by an actor in a motion picture - comedy or musical

# best performance by an actress in a television series - comedy or musical
# best performance by an actor in a television series - comedy or musical

# best performance by an actor in a supporting role in a motion picture
# best performance by an actress in a supporting role in a motion picture

# best performance by an actress in a supporting role in a series, mini-series or motion picture made for television
# best performance by an actor in a supporting role in a series, mini-series or motion picture made for television

# best performance by an actress in a motion picture - drama
# best performance by an actor in a motion picture - drama

# best performance by an actress in a television series - drama
# best performance by an actor in a television series - drama

# best performance by an actor in a mini-series or motion picture made for television
# best performance by an actress in a mini-series or motion picture made for television

	if "host" in text:
		lists["host"]["winner"] += nouns

	if "drama" in text and ("best motion picture" in text or "best picture" in text):
		lists["best motion picture - drama"]["winner"] += nouns

	if "drama" in text and "actor" in text and ("performance" in text or "best performance" in text):
		lists["best performance by an actor in a motion picture - drama"]["winner"] += nouns
	if "drama" in text and "actress" in text and ("performance" in text or "best performance" in text):
		lists["best performance by an actress in a motion picture - drama"]["winner"] += nouns

	if "comedy" in text and ("best motion picture" in text or "best picture" in text):
		lists["best motion picture - comedy or musical"]["winner"] += nouns

	if "best" in text and "actor" in text and ("supporting" in text or "supporting role" in text):
		lists["best performance by an actor in a supporting role in a motion picture"]["winner"] += nouns
	if "best" in text and "actress" in text and ("supporting" in text or "supporting role" in text):
		lists["best performance by an actress in a supporting role in a motion picture"]["winner"] += nouns

	if "best" in text and ("director" in text or "best director" in text):
		lists["best director - motion picture"]["winner"] += nouns

	if "actress" in text and "best" in text and ("comedy" in text or "musical" in text) and "television" not in text:
		lists["best performance by an actress in a motion picture - comedy or musical"]["winner"] += nouns
	if "actor" in text and "best" in text and ("comedy" in text or "musical" in text) and "television" not in text:
		lists["best performance by an actor in a motion picture - comedy or musical"]["winner"] += nouns

	if "dressed" in text and "best" in text:
		best_dressed_list += nouns
		# print (text, '\n')

results = {}

results["Host"] = getAwardWinnerPerson("", "Host:", lists["host"]["winner"])

results["Best Motion Picture - Drama"] = {}
results["Best Motion Picture - Drama"]["Winner"] = getAwardWinnerMovie("", "Best Picture - Drama:", lists["best motion picture - drama"]["winner"])
results["Best Motion Picture - Drama"]["Presenters"] = []
results["Best Motion Picture - Drama"]["Nominees"] = []

results["best motion picture - comedy or musical"] = {}
results["best motion picture - comedy or musical"]["Winner"] = getAwardWinnerMovie("", "Best Picture - Comedy:", lists["best motion picture - comedy or musical"]["winner"])
results["best motion picture - comedy or musical"]["Presenters"] = []
results["best motion picture - comedy or musical"]["Nominees"] = []

results["best performance by an actress in a supporting role in a motion picture"] = {}
results["best performance by an actress in a supporting role in a motion picture"]["Winner"] = getAwardWinnerPerson("", "Best Actress in a Supporting Role:", lists["best performance by an actress in a supporting role in a motion picture"]["winner"])
results["best performance by an actress in a supporting role in a motion picture"]["Presenters"] = []
results["best performance by an actress in a supporting role in a motion picture"]["Nominees"] = []

results["best performance by an actor in a supporting role in a motion picture"] = {}
results["best performance by an actor in a supporting role in a motion picture"]["Winner"] = getAwardWinnerPerson("", "Best Actor in a Supporting Role:", lists["best performance by an actor in a supporting role in a motion picture"]["winner"])
results["best performance by an actor in a supporting role in a motion picture"]["Presenters"] = []
results["best performance by an actor in a supporting role in a motion picture"]["Nominees"] = []

results["best director - motion picture"] = {}
results["best director - motion picture"]["Winner"] = getAwardWinnerPerson("", "Best Director:", lists["best director - motion picture"]["winner"])
results["best director - motion picture"]["Presenters"] = []
results["best director - motion picture"]["Nominees"] = []

results["best performance by an actress in a motion picture - drama"] = {}
results["best performance by an actress in a motion picture - drama"]["Winner"] = getAwardWinnerPerson("", "Best Actress - Drama:", lists["best performance by an actress in a motion picture - drama"]["winner"])
results["best performance by an actress in a motion picture - drama"]["Presenters"] = []
results["best performance by an actress in a motion picture - drama"]["Nominees"] = []

results["best performance by an actor in a motion picture - drama"] = {}
results["best performance by an actor in a motion picture - drama"]["Winner"] = getAwardWinnerPerson("", "Best Actor - Drama:", lists["best performance by an actor in a motion picture - drama"]["winner"])
results["best performance by an actor in a motion picture - drama"]["Presenters"] = []
results["best performance by an actor in a motion picture - drama"]["Nominees"] = []

results["best performance by an actress in a motion picture - comedy or musical"] = {}
results["best performance by an actress in a motion picture - comedy or musical"]["Winner"] = getAwardWinnerPerson("", "Best Actress - Musical or Comedy:", lists["best performance by an actress in a motion picture - comedy or musical"]["winner"])
results["best performance by an actress in a motion picture - comedy or musical"]["Nominees"] = []

results["best performance by an actor in a motion picture - comedy or musical"] = {}
results["best performance by an actor in a motion picture - comedy or musical"]["Winner"] = getAwardWinnerPerson("", "Best Actor - Musical or Comedy:", lists["best performance by an actor in a motion picture - comedy or musical"]["winner"])
results["best performance by an actor in a motion picture - comedy or musical"]["Presenters"] = []
results["best performance by an actor in a motion picture - comedy or musical"]["Nominees"] = []


# best screenplay - motion picture
# best director - motion picture
# best original score - motion picture
# best motion picture - drama
# best original song - motion picture
# best motion picture - comedy or musical
# best animated feature film

# best foreign language film
# best mini-series or motion picture made for television
# cecil b. demille award

# best television series - drama
# best television series - comedy or musical

# best performance by an actress in a motion picture - comedy or musical
# best performance by an actor in a motion picture - comedy or musical

# best performance by an actress in a television series - comedy or musical
# best performance by an actor in a television series - comedy or musical

# best performance by an actor in a supporting role in a motion picture
# best performance by an actress in a supporting role in a motion picture

# best performance by an actress in a supporting role in a series, mini-series or motion picture made for television
# best performance by an actor in a supporting role in a series, mini-series or motion picture made for television

# best performance by an actress in a motion picture - drama
# best performance by an actor in a motion picture - drama

# best performance by an actress in a television series - drama
# best performance by an actor in a television series - drama

# best performance by an actor in a mini-series or motion picture made for television
# best performance by an actress in a mini-series or motion picture made for television



getAwardWinnerPerson("", "Best Dressed:", best_dressed_list)


# textblob
# TextBlob("I loved it")
# blob.sent.sentiment

# return the final results
print ('\n')
print (json.dumps(results))