#encoding
import json
import pandas as pd

# with open("TM_WORLD_COUNTRIES.txt", 'r', encoding='utf-8') as f:
#     tm = f.read()
#
# with open("ANKI_COUNTRIES.txt", 'r', encoding='utf-8') as f:
#     anki = f.read()
#
# with open('tm_to_anki.json', 'r', encoding='utf-8') as f:
#     tm_to_anki = json.load(f)
#
# tm = tm.split('\n')
# anki = anki.split('\n')
#
# for k, e in tm_to_anki.items():
#     try:
#         tm.remove(k)
#         anki.remove(e)
#     except ValueError:
#         print(k, e)
#
# print(tm)
# print(anki)

data = pd.read_csv('../anki_data/cleaned_data.csv', encoding='utf-8')

name_to_short = dict(zip(list(data.Country), list(data.short)))


with open('tm_to_anki.json', 'r', encoding='utf-8') as f:
    tm_to_anki = json.load(f)

for k, e in tm_to_anki.items():
    try:
        tm_to_anki[k] = name_to_short[e]
    except KeyError:
        print(k)

with open('tm_to_anki.json', 'w', encoding='utf-8') as f:
    json.dump(tm_to_anki, f, indent=4)

print(tm_to_anki)
