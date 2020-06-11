# Purpose is to convert data from countries.geojson to the countries/ folder
import json

folder = 'countries/'

with open("countries.geojson", 'r') as f:
    data = json.load(f)

data = data['features']

names = []
for d in data:
    name = d['properties']['ADMIN']
    names.append(name)
    polygons = d['geometry']['coordinates']
    ptype = d['geometry']['type']
    if ptype == 'MultiPolygon':
        polygons = [a[0] for a in polygons]

    # print(name, len(polygons))
    #
    # with open(folder + name + '.json', 'w') as f:
    #     json.dump(polygons, f, indent=3)

names = sorted(names)

with open('data_countries.json', 'w') as f:
    json.dump(names, f, indent=3)
