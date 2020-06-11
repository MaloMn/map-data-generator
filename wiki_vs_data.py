# coding: utf-8
# Checking that names from data are the same as the ones from wiki
import json
import os

# Collect data country names
data_names = os.listdir('data/countries')
data_names = [a.replace('.json', '') for a in data_names]

with open('data/countries_capitals.json', 'r') as f:
    wiki_names = json.load(f)
wiki_names = list(wiki_names.keys())

for e in data_names:
    if e not in wiki_names:
        print(e)
    else:
        wiki_names.remove(e)

print('#####')
print('\n'.join(wiki_names))

