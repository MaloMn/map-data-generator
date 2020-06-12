# Map data generator

This projects aims at creating the correct data to be used in a Godot game. 
The data consists of some polygons representing countries or regions of the world ;
the capitals of these countries, and the flags of the countries/regions.

The data created originated from an anki deck called 
[Ultimate Geography](https://github.com/axelboc/anki-ultimate-geography). I must thank
its creator for the amazing work done to collect all the information.

## Polygon creation

This part is definitely the most tidious one. Based on the name of the countries, 
I had to collect the polygons representing them in the world. I used the data from
[Natural Earth](https://www.naturalearthdata.com/), and from 
[Open Street Map](https://www.openstreetmap.org/#map=5/5.507/150.249). 
The data of Natural Earth is incredible. I was
a bit underwhelmed by OSM data as I only wanted the grounds of each country whereas
OSM also provides the water region surrounding the countries.

Once the high detail data had been retrieved, I had to simplify it in order to
diplay it in a game. I used [Visvalingam's algorithm](https://pypi.org/project/visvalingamwyatt/)
to do so, and then corrected the simplified shapes with Shapely.

## Flags

To be continued.

## Capitals locations

To be continued.