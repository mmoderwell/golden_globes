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
"Best Performance", "Annual Golden Globe Awards", "Golden Globe Awards", "Best Director", "BEST PICTURE", 
"Look", "Btw", "’", "2015", "2016", "2017", "2018", "2019", "Best Actor", "Best Actress",
 "Golden Globes 2020", "2020 Golden Globes", "Best Original Score", "Best Original Song",
 "Best Foreign Language Film"]

def getWinnerPerson(title, relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list and not word[0].isnumeric():
			results.append(word[0])

	try:
		best = results[0]
	except:
		best = 'Unknown'
	print(title, best)
	return best

def getNomineesPerson(title, relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list and not word[0].isnumeric():
			results.append(word[0])

	try:
		best = results[0:5]
	except:
		best = ['Unknown']
	print(title, best)
	return best

def getPresenters(title, relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list and not word[0].isnumeric():
			results.append(word[0])

	try:
		best = results[0:2]
	except:
		best = ['Unknown']
	print(title, best)
	return best

def getWinnerMovie(title, relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list:
			results.append(word[0])

	try:
		best = results[0]
	except:
		best = 'Unknown'
	print(title, best)
	return best

def getNomineesMovie(title, relevant_list):
	aCounter = Counter(relevant_list)
	most_occur = aCounter.most_common(20)
	results = []
	for word in most_occur:
		if word[0] not in skip_list:
			results.append(word[0])

	try:
		best = results[0:5]
	except:
		best = ['Unknown']
	print(title, best)
	return best


lists = {}

awards = [
	"best performance by an actor in a television series - drama",
	"best performance by an actress in a television series - drama",
	"best performance by an actress in a motion picture - drama",
	"best performance by an actor in a motion picture - drama",
	"best performance by an actress in a mini-series or motion picture made for television",
	"best performance by an actor in a mini-series or motion picture made for television",
	"best performance by an actress in a supporting role in a series, mini-series or motion picture made for television",
	"best performance by an actor in a supporting role in a series, mini-series or motion picture made for television",
	"best performance by an actress in a supporting role in a motion picture",
	"best performance by an actor in a supporting role in a motion picture",
	"best performance by an actress in a television series - comedy or musical",
	"best performance by an actor in a television series - comedy or musical",
	"best performance by an actor in a motion picture - comedy or musical",
	"best performance by an actress in a motion picture - comedy or musical",
	"best mini-series or motion picture made for television",
	"best director - motion picture",
	"best screenplay - motion picture",
	"best original score - motion picture",
	"best foreign language film",
	"best animated feature film",
	"best original song - motion picture",
	"cecil b. demille award",
	"best motion picture - drama",
	"best motion picture - comedy or musical",
	"best television series - drama",
	"best television series - comedy or musical"
]

# Host list
lists["host"] = {}
lists["host"]["winner"] = []

# Initialize the lists for each award
for award in awards:
	lists[award] = {}
	# Initialize all the different kinds of fields for each award
	lists[award]["winner"] = []
	lists[award]["nominees"] = []
	lists[award]["presenters"] = []

for tweet in df.head(50000).itertuples():
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

	text = text.lower()

	# Build up the lists
	if all(word in text for word in ["host"]):
		lists["host"]["winner"] += nouns

	if all(word in text for word in []) and any(word in text for word in ["winner", "awarded", "cecil", "demille"]):
		lists["cecil b. demille award"]["winner"] += nouns

	# if all(word in text for word in ["screenplay", "best"]) and any(word in text for word in ["motion", "picture", "winner", "motion", "picture"]):
	# 	lists["best screenplay - motion picture"]["winner"] += nouns

	# if all(word in text for word in ["original", "score", "best"]) and any(word in text for word in ["motion", "picture", "winner", "awarded"]):
	# 	lists["best original score - motion picture"]["winner"] += nouns

	# if all(word in text for word in ["original", "song", "best"]) and any(word in text for word in ["motion", "picture", "winner", "awarded"]):
	# 	lists["best original song - motion picture"]["winner"] += nouns

	# if all(word in text for word in ["animated", "best"]) and any(word in text for word in ["film", "winner", "feature"]):
	# 	lists["best animated feature film"]["winner"] += nouns

	# if all(word in text for word in ["foreign", "best", "film"]) and any(word in text for word in ["winner", "language"]):
	# 	lists["best foreign language film"]["winner"] += nouns

	# if all(word in text for word in ["best"]) and any(word in text for word in ["mini", "tv", "television", "winner", "mini-series"]):
	# 	lists["best mini-series or motion picture made for television"]["winner"] += nouns

	# if all(word in text for word in ["drama", "best", "series"]) and any(word in text for word in ["tv", "television", "winner"]):
	# 	lists["best television series - drama"]["winner"] += nouns

	# # if all(word in text for word in [""]) and any(word in text for word in [""]):
	# # 	lists[""]["winner"] += nouns

	# if all(word in text for word in ["drama"]) and any(word in text for word in ["best motion picture", "best picture"]):
	# 	lists["best motion picture - drama"]["winner"] += nouns

	# if all(word in text for word in ["drama", "actor"]) and any(word in text for word in ["performance", "best performance"]):
	# 	lists["best performance by an actor in a motion picture - drama"]["winner"] += nouns
	# if all(word in text for word in ["drama", "actress"]) and any(word in text for word in ["performance", "best performance"]):
	# 	lists["best performance by an actress in a motion picture - drama"]["winner"] += nouns

	# if all(word in text for word in ["comedy"]) and any(word in text for word in ["best motion picture", "best picture"]):
	# 	lists["best motion picture - comedy or musical"]["winner"] += nouns

	# if all(word in text for word in ["best", "actor"]) and any(word in text for word in ["supporting", "supporting role"]):
	# 	lists["best performance by an actor in a supporting role in a motion picture"]["winner"] += nouns
	# if all(word in text for word in ["best", "actress"]) and any(word in text for word in ["supporting", "supporting role"]):
	# 	lists["best performance by an actress in a supporting role in a motion picture"]["winner"] += nouns

	# if all(word in text for word in ["best", "director"]):
	# 	lists["best director - motion picture"]["winner"] += nouns

	# if all(word in text for word in ["best", "actress"]) and any(word in text for word in ["comedy", "musical"]) and "television" not in text:
	# 	lists["best performance by an actress in a motion picture - comedy or musical"]["winner"] += nouns
	# if all(word in text for word in ["best", "actor"]) and any(word in text for word in ["comedy", "musical"]) and "television" not in text:
	# 	lists["best performance by an actor in a motion picture - comedy or musical"]["winner"] += nouns


	# Words to remove when parsing award title to make lists
	stop_words = ["by", "an", "in", "a", "-", "or"]

	# build up the lists for each award
	# can optionally do it manually and exclude from this part
	for award in [award for award in awards if award not in ["cecil b. demille award"]]:
		# print (award)
		split = award.split("-")
		try:
			key_needed = list(filter(lambda s: s not in stop_words, split[0].split()))
			key_maybes = list(filter(lambda s: s not in stop_words, split[1].split()))
		except:
			key_needed = list(filter(lambda s: s not in stop_words, split[0].split()))
			key_maybes = list(filter(lambda s: s not in stop_words, split[0].split()))

		key_words = list(filter(lambda s: s not in stop_words, award.split()))

		key_needed = [word.lstrip().rstrip() for word in key_needed]
		key_maybes = [word.lstrip().rstrip() for word in key_maybes]
		key_words = [word.lstrip().rstrip() for word in key_words]
	
		def winners():
			# set of words that need to be in tweet
			needed = set()
			# set of words where one or more could be in tweet
			maybe = set()
			# #  if an award is for actor
			# if (any(word in award for word in ["actor"])):
			# 	needed.update(["actor", "best"])
			# 	maybe.update(key_words)

			# # award for an actress
			# if (any(word in award for word in ["actress"])):
			# 	needed.update(["actress", "best"])
			# 	maybe.update(key_words)

			# if (any(word in award for word in ["television"])):
			# 	# needed += {"television"}
			# 	maybe.update(key_words)
			# 	maybe.update(["television", "tv"])

			# if (any(word in award for word in ["television"])):
			# 	maybe.update(key_words)


			maybe.update(key_maybes)
			needed.update(key_needed)

			if all(word in text for word in needed) and any(word in text for word in maybe):
				lists[award]["winner"] += nouns


		def nominees():
			# set of words that need to be in tweet
			needed = set()
			# set of words where one or more could be in tweet
			maybe = set()

			# maybe.update(key_words)
			maybe.update(["nominated", "nominees"])

			# needed.update(key_words[0:4])
			# needed.update(["nominee"])

			# maybe.update(key_maybes)
			needed.update(key_needed)
			
			if all(word in text for word in needed) and any(word in text for word in maybe):
				lists[award]["nominees"] += nouns

		def presenters():
			# set of words that need to be in tweet
			needed = set()
			# set of words where one or more could be in tweet
			maybe = set()

			# maybe.update(key_words)
			maybe.update(["presenters", "present", "presented"])

			# needed.update(key_words[0:4])
			needed.update(key_needed)
			# needed.update(["presented"])

			if all(word in text for word in needed) and any(word in text for word in maybe):
				lists[award]["winner"] += nouns

		winners()
		nominees()
		presenters()


results = {}
results["Host"] = getWinnerPerson("Host:", lists["host"]["winner"])

# Assign awards to the results dict
for award in awards:
	# person awardee
	if (any(word in award for word in ["actor", "actress"])):
		results[award] = {}
		results[award]["Winner"] = getWinnerPerson(f"{award} winner:", lists[award]["winner"])
		results[award]["Presenters"] = getPresenters(f"{award} presenters:", lists[award]["presenters"])
		results[award]["Nominees"] = getNomineesPerson(f"{award} nominees:", lists[award]["nominees"])
	# movie or tv show awardee
	else:
		results[award] = {}
		results[award]["Winner"] = getWinnerMovie(f"{award} winner:", lists[award]["winner"])
		results[award]["Presenters"] = getPresenters(f"{award} presenters:", lists[award]["presenters"])
		results[award]["Nominees"] = getNomineesMovie(f"{award} nominees:", lists[award]["nominees"])


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

# textblob
# TextBlob("I loved it")
# blob.sent.sentiment

# return the final results
print ('\n')
# print (json.dumps(results))
print (results)