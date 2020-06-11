import json
from shapely import geometry
from shapely.validation import explain_validity

with open('1_displayable_data/Canada_0.1_10.json', 'r') as f:
    canada = json.load(f)

canada = sorted(canada, key=lambda a: len(a), reverse=True)
poly = geometry.Polygon(canada[0])
print(poly.is_valid)

poly = poly.buffer(0)
print(poly.is_valid)

x, y = poly.exterior.coords.xy

poly = list(zip(x, y))
poly = [list(a) for a in poly]

print(poly)



