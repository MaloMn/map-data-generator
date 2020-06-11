from countries import Country
import os
import json

# Get ref tab
with open('cleaned_data.json', 'r', encoding='utf-8') as f:
    tab = json.load(f)

d = {}
for i in tab:
    image = i[7]
    a = image.find('"')
    path = image[a+1:]
    b = path.find('"')
    path = path[:b]
    path = 'maps/' + path.replace('.png', '')
    d[i[0]] = path


# List files of starting_data folder
folder = '0_starting_data/'
files = os.listdir(folder)
files = [a.replace('.json', '') for a in files]

for country_name in files:
    c = Country(folder, country_name)
    try:
        file_name = d[country_name]
    except KeyError:
        file_name = country_name

    if file_name == '':
        file_name = 'maps/' + country_name

    c.simplify('1_displayable_data/', thresh=0.1, nb_points=10)
    c.draw(file_name + '1')
    c.simplify('2_collisionable_data/', thresh=1.5)
    c.draw(file_name + '2')
