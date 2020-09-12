import requests
import logging
import json
import numpy as np
from polygons import correct_rotation_and_scale

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


class City:

    def __init__(self, folder, name, short):
        """
        Opens the json file of the country, and either collects the polygons online,
        or loads them from a file if it exists.
        :param folder: folder containing the country
        :param name: Name of the country (no need to specify ".json")
        """
        base_data = "osm_pinpoints/"
        self.folder = folder
        self.name = name
        self.short = short

        # Now we load the variable self.pinpoint
        try:
            with open(base_data + self.short + ".json", "r") as f:
                self.pinpoint = json.load(f)
            print('Loaded {} from file.'.format(self.short))

        except FileNotFoundError:
            try:
                self.pinpoint = self.get_pinpoint()
                with open(folder + self.short + ".json", "w") as f:
                    json.dump(self.pinpoint, f)
                print('Successfully collected location of {} online: '.format(self.short))
                logger.info('Successfully collected location of {} online: '.format(self.short))
            except ValueError:
                print('Something went wrong with {}.'.format(self.short))
                logger.error("{} could not be found in OSM.".format(self.short))
                self.pinpoint = []

        # Saving the base_data in destination folder
        with open(base_data + self.short + ".json", "w") as f:
            json.dump(self.pinpoint, f)

        # Saving the data in destination folder
        with open(folder + self.short + ".json", "w") as f:
            self.pinpoint = correct_rotation_and_scale(self.pinpoint)
            json.dump(self.pinpoint, f)

    def get_pinpoint(self):
        data = json.loads(retrieve("https://nominatim.openstreetmap.org/search?q=" + self.name + "&format=geojson"))
        location = data["features"][0]["geometry"]["coordinates"]
        return location


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("anki_data/cleaned_data.csv", index_col=0)
    df = df[df['Capital'].notna()]

    for capital, short in zip(df.Capital, df.short):
        city = City("pinpoints/", capital, short)
        print(capital, city.pinpoint)
