import json

with open('tm_to_anki.json', 'r', encoding='utf-8') as f:
    table = json.load(f)

with open("TM_WORLD_BORDERS_SIMPL-0.3/TM_WORLD_BORDERS_SIMPL.json", 'r', encoding='utf-8') as f:
    high = json.load(f)

for p in high['features']:
    country = p['properties']['NAME']
    name = table[country] if table[country] != "" else country

    if p["geometry"]['type'] == "MultiPolygon":
        polygons = []
        for i in p["geometry"]['coordinates']:
            polygons.append(i[0])
    else:
        polygons = p["geometry"]['coordinates']

    with open('low/' + name + ".json", 'w') as f:
        json.dump(polygons, f, indent=4)
