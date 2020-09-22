import json
from polygons import Polygon

with open('tm_to_anki.json', 'r', encoding='utf-8') as f:
    table = json.load(f)


def extract(input: str, output: str):
    with open(input, 'r', encoding='utf-8') as f:
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

        polygons = [Polygon(p).array.tolist() for p in polygons]

        with open(output + name + ".json", 'w') as f:
            json.dump(polygons, f)


if __name__ == "__main__":
    extract("TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS.json", '../polygons_display/')
    extract("TM_WORLD_BORDERS_SIMPL-0.3/TM_WORLD_BORDERS_SIMPL.json", '../polygons_collision/')
