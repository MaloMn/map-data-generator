import requests
import logging
import json
from polygons import Polygon
import os
import shapely.geometry as sg
import matplotlib.pyplot as plt
import numpy as np

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="log.log",
                    level=logging.INFO,
                    format=LOG_FORMAT,
                    filemode='w')
logger = logging.getLogger()


def retrieve(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        logger.critical("Following url couldn\'t be reached: {}".format(url))
        raise ConnectionError("Website could not be reached")


def no_change(array):
    f = lambda x: [x[0]*36/155-180, -x[1]*36/155 + 90]
    return np.apply_along_axis(f, 1, array)


class Country:

    def __init__(self, folder, name):
        """
        Opens the json file of the country, and either collects the polygons online,
        or loads them from a file if it exists.
        :param folder: folder containing the country
        :param name: Name of the country (no need to specify ".json"
        """
        self.folder = folder
        self.name = name

        # Now we load the variable self.polygons
        try:
            with open(self.folder + self.name + ".json", "r") as f:
                self.polygons = json.load(f)
            print('Loaded from file.')
        except FileNotFoundError:
            try:
                self.polygons = self.get_polygons()
                with open(folder + self.name + ".json", "w") as f:
                    json.dump(self.polygons, f)
                print('Successfully collected the map online, {} polygons.'.format(len(self.polygons)))
                logger.info("{} has been found online.".format(self.name))
            except ValueError:
                print('Something went wrong with {}.'.format(self.name))
                logger.error("{} could not be found in OSM.".format(self.name))
                self.polygons = []

        self.polygons = [Polygon(p) for p in self.polygons]
        self.simplified = [a.array for a in self.polygons]

    def get_polygons(self):
        data = json.loads(retrieve("https://nominatim.openstreetmap.org/search?q=" + self.name + "&format=geojson"))
        id = None
        for i in data["features"]:
            p = i["properties"]
            if p["type"] == "administrative" and p["category"] == "boundary":
                id = p["osm_id"]
                break
            else:
                print('Following data was rejected: ', p)

        if id is None:
            raise ValueError("Nothing was found that corresponded to the requested name.")
        else:
            print('{} id: {}'.format(self.name, id))

        data = json.loads(retrieve("http://polygons.openstreetmap.fr/get_geojson.py?id=" + str(id) + "&params=0"))

        if data["geometries"][0]['type'] == "MultiPolygon":
            polygons = []
            for i in data["geometries"][0]['coordinates']:
                polygons.append(i[0])

            polygons = sorted(polygons, key=lambda x: len(x), reverse=True)
        else:
            print(data["geometries"][0]['type'])

        return polygons

    def draw(self, name=None):
        poly = [sg.Polygon(no_change(np.array(a))) for a in self.simplified]
        poly = sg.MultiPolygon(poly)

        fig, axs = plt.subplots()
        axs.set_aspect('equal', 'datalim')

        for geom in poly.geoms:
            xs, ys = geom.exterior.xy
            axs.fill(xs, ys, alpha=0.5, fc='r', ec='none')

        plt.savefig(str(name) + '.png')
        plt.close()

    def simplify(self, folder, thresh=None, nb_points=None):
        for i in range(len(self.polygons)):
            self.polygons[i].simplify(thresh=thresh, nb_points=nb_points)

        # Removing None values when an area has been oversimplified.
        self.simplified = [p.simplified.tolist() for p in self.polygons if p.simplified is not None]
        # self.simplified = list(filter(lambda a: a is not None, self.simplified))

        # Saving the simplified shape
        filename = self.name #+ "_" + str(thresh) + "_" + str(nb_points)
        with open(folder + filename + ".json", "w") as f:
            json.dump(self.simplified, f, indent=3)
        logger.info("Saved " + filename + ", {} polygons.".format(len(self.simplified)))
        print("Saved " + filename + ", {} polygons.".format(len(self.simplified)))


if __name__ == "__main__":
    folder = ""
    countries = os.listdir(folder)
    # countries.pop(0)
    countries = [a.replace('.json', '') for a in countries]
    print(countries)
    for n in countries:
        Country(n)
