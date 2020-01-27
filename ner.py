import pandas as pd
import re
import nltk

# Python program to find the k most frequent words 
# from data set 
from collections import Counter 

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

data_url = "./data/gg2020.json"
df = pd.read_json(data_url, orient='columns', lines=True)

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

master_name_list = []
master_award_list = []
master_nominee_list = []
master_winner_list = []

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
	names = []
	tokenized = preprocess(text)
	for word in tokenized:
		if word[1] == 'NNP':
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

	master_name_list += answer
	# print (answer,'\n')

	if "winner" in text or "Winner" in text:
		master_winner_list += answer

	if "nominee" in text or "Nominee" in text:
		master_nominee_list += answer

	if "award" in text or "Award" in text:
		master_award_list += answer
		# print (text, '\n')


# Pass the split_it list to instance of Counter class. 
Counter1 = Counter(master_name_list)
most_occur = Counter1.most_common(20)
print(most_occur)

Counter2 = Counter(master_award_list)
most_occur = Counter2.most_common(20)
print(most_occur)

Counter3 = Counter(master_winner_list)
most_occur = Counter3.most_common(20)   
print(most_occur)

Counter4 = Counter(master_nominee_list)
most_occur = Counter4.most_common(20) 
print(most_occur)



# from imdb import IMDb

# # create an instance of the IMDb class
# ia = IMDb()
# top_movies = ia.get_top250_movies()

# for movie in top_movies:
# 	if (movie['year'] == 2016):
# 		print (movie['title'], movie['year'])

# movies = ia.search_keyword('user_rating=7.0%2C')
# print (movies)