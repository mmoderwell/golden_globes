import pandas as pd
import re

data_url = "./data/gg2020.json"
df = pd.read_json(data_url, orient='columns', lines=True)

# print (df.columns)

for tweet in df.head(100).iterrows():
	text = tweet[1].text

	# pull out the urls and remove them
	text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
	# pull out the hashtags
	hashtags = re.findall(r'(?i)\#\w+', text)
	text = re.sub(r'(?i)\#\w+', '', text)
	# pull out all the @'s
	mentions = re.findall(r'(?i)\@\w+', text)
	text = re.sub(r'(?i)\@\w+', '', text)

	print (text,'\n')
