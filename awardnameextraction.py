#Putting together for a *.py file
import pandas as pd
import nltk
import os
import nltk.corpus
from nltk import ngrams
from nltk.probability import FreqDist
from itertools import chain
from nltk import everygrams
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import string
from nltk.corpus import stopwords


#Can change this to what's in the ner.py file later
data_url = "./data/gg2020.json"
df2 = pd.read_json(data_url, orient='columns', lines=True)
#url='http://drive.google.com/uc?export=view&id=1Ya7cxYANh-KDU7HfGmPPSR6wK7w1x1Tq'
#df2 = pd.read_json(url, orient='columns', lines=True)

cleantable = str.maketrans('', '', string.punctuation)
nltk.download('stopwords')
cleanstop_words = set(stopwords.words('english'))
cleanstop_words.add('golden')
cleanstop_words.add('globes')
cleanstop_words.add('globe')
cleanstop_words.add('https')
cleanstop_words.add('performance')
cleanstop_words.add('via')
#cleanstop_words.remove('in')
# - do some common translations TV-Television
def commonwords(inp):
  if inp == "tv":
    return "television"
  if inp == "lim":
    return "limited"
  if inp == "awd":  
    return "award"
  if inp == "awds":  
    return "awards"    
  return inp

#primary function to tokenize tweet
def cleantweet(inp):
  tokens = word_tokenize(inp)
  # convert to lower case
  tokens = [w.lower() for w in tokens]
  # remove punctuation from each word
  stripped = [w.translate(cleantable) for w in tokens]
  # remove remaining tokens that are not alphabetic
  words = [word for word in stripped if word.isalpha()]
  # filter out stop words  
  words = [commonwords(w) for w in words if not w in cleanstop_words]
  return words

#deduplication to the longest step
def tuple_subset(tup1, tup2):
  #Checks if tup1 is a subset of tup2
  if (len(tup1) >= len(tup2)):
    return False
  member = True
  for i in range(len(tup1)):
    if tup1[i] != tup2[i]:
      member = False
      break
  return member

#clean tweets to list of token tuples
sents = df2['text'].map(cleantweet).tolist()

#generate ngrams and select only best* and cecil* ngrams
non_relevant_words_list=('career', 'moments', 'carpet', 'win', 'fashion','jokes', 'part', 'dressed','goldenglobes','youtube','reactions','speech','presented', 'oscar', 'next', 'hollywood')
non_relevant_words=set(non_relevant_words_list)
cleanedawardnames=[[ sent for sent in list(everygrams(tweet,4,10)) if (sent[0]=='best' or sent[0]=='cecil') and not bool(non_relevant_words.intersection(sent)) ] for tweet in sents]
#concatenate them
allbests=list(chain.from_iterable(cleanedawardnames))
#group by and identify top most frequent
freqanalysis=FreqDist(allbests)

common=freqanalysis.most_common(80) #top is arbitrary

#one more group by leaving the longest from most frequent
return_arr = []
for test_set in common:
  keep = True
  test_list = test_set[0] #actual tuple, not freq
  for all_sets in common:
    check_list = all_sets[0] #actual tuple, not freq
    if (tuple_subset(test_list, check_list)):
      keep = False
      break
  if keep:
    return_arr.append(test_set)

#make output pretty
allawards=[string.capwords(' '.join(awtuple[0])) for awtuple in return_arr]
print(allawards)
