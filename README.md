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
[Open Street Map](https://www.openstreetmap.org/#map=5/5.507/150.249). 
Once the highly-detailed polygons were gathered (in the `osm_polygons/` folder), they had
to be simplified. I used [Visvalingam's algorithm](https://pypi.org/project/visvalingamwyatt/)
to do so. The idea is to get two simplified shapes : first, a precise map for displaying purpose 
(contained in `polygons_display/` folder) ; and then another less precise map for mouse in-game interaction purpose
(contained in `polygons_collision/` folder).  

After computing these things, I find out islands borders were poorly documented in OSM. Hence, I wrote a python script
that takes a png image from OSM of the island or archipelagos, and then uses OpenCV to get the borders.  
This process has a big manual part, and it is located in the `osm_maps/` folder.

## Flags

Base data for flags was recollected in the `.svg` format from Wikipedia (`flags_from_wikipedia.py` does this.). Missing
flags were added manually. These are located in the `wiki_flags/` folder.  
Then, the conversion to png images was done using `flags_svg_to_png.py`. The result is in the `flags/` folder.  
The choice was made to keep all flags to the same height. The width was computed accordingly in order not to disrupt the
real ratio of the flags.

## Capitals locations

I'll refer to the name *pinpoint* to talk about the countries capitals locations. I've also used OSM to gather them.
Then, they were slightly changed to have the same coordinates as their countries polygons. As before, the raw collected 
pinpoints from OSM are in `osm_pinpoints`, and the modified pinpoints are in `pinpoints/`.
