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

    def __init__(self, folder, name):
        """
        Opens the json file of the country, and either collects the polygons online,
        or loads them from a file if it exists.
        :param folder: folder containing the country
        :param name: Name of the country (no need to specify ".json"
        """
        base_data = "data/0_pinpoints/"
        self.folder = folder
        self.name = name

        # Now we load the variable self.pinpoint
        try:
            with open(base_data + self.name + ".json", "r") as f:
                self.pinpoint = json.load(f)
            print('Loaded {} from file.'.format(self.name))
        except FileNotFoundError:
            try:
                self.pinpoint = self.get_pinpoint()
                with open(folder + self.name + ".json", "w") as f:
                    json.dump(self.pinpoint, f)
                print('Successfully collected location of {} online: '.format(self.name))
                # logger.info("{} city has been found online.".format(self.name))
            except ValueError:
                print('Something went wrong with {}.'.format(self.name))
                logger.error("{} could not be found in OSM.".format(self.name))
                self.pinpoint = []

        with open(folder + self.name + ".json", "w") as f:
            self.pinpoint = correct_rotation_and_scale(self.pinpoint)
            json.dump(self.pinpoint, f)
        # print(self.pinpoint)
        # self.pinpoint = correct_rotation_and_scale(self.pinpoint)
        # print(self.pinpoint)

    def get_pinpoint(self):
        data = json.loads(retrieve("https://nominatim.openstreetmap.org/search?q=" + self.name + "&format=geojson"))
        location = data["features"][0]["geometry"]["coordinates"]
        print(location)
        return location


if __name__ == "__main__":
    import pandas as pd
    folder = "pinpoints/"
    df = pd.read_csv("data/cleaned_data.csv")
    df = df[df['Capital'].notna()]

    for i in range(df.shape[0]):
        country = df.iloc[i, 1]
        capital = df.iloc[i, 3]
        print(country, capital)
        print(City(folder, capital).pinpoint)
