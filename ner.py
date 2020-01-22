import pandas as pd

data_url = "./data/gg2020.json"

df = pd.read_json(data_url, orient='columns', lines=True)

print (df.columns)