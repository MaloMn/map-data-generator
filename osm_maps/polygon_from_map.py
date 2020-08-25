import json
import cv2 as cv
import numpy as np
from scipy.interpolate import interp1d
from polygons import correct_rotation_and_scale, resolve_geometry

from matplotlib import pyplot as plt
from matplotlib.patches import Polygon as MatPolygon
from matplotlib.collections import PatchCollection


display_folder = "display/"
collision_folder = "collision/"


class Map:

    def __init__(self, img_path):
        self.original = cv.imread(img_path)
        self.size = self.original.shape[:2]
        self.name = img_path.replace('.png', '')
        print(self.name)

        self.contours = self.get_contours()
        self.polygons = self.get_polygons()
        self.corners = self.polygons[0]
        self.polygons = self.polygons[1:]

        self.save_polygons()

    def get_contours(self):
        img = self.original.copy()

        # Removing the sea
        img[np.where((img == [223, 211, 170]).all(axis=2))] = [0, 0, 0]
        img[np.where((img != [0, 0, 0]).all(axis=2))] = [255, 255, 255]

        # Getting the contours
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # Simplify the contours
        for i in range(len(contours)):
            cnt = contours[i]
            epsilon = 0.005 * cv.arcLength(cnt, True)
            contours[i] = cv.approxPolyDP(cnt, epsilon, True)

        # Sort them in descending order
        contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)

        big_area = sum([cv.contourArea(x) for x in contours[:2]]) / 3
        percent = 0.01

        # Remove small contours
        contours = [x for x in contours if cv.contourArea(x) > percent * big_area]
        return contours

    def get_polygons(self):
        poly = [a.tolist() for a in self.contours]

        for i in range(len(poly)):
            for j in range(len(poly[i])):
                poly[i][j] = poly[i][j][0]

        # poly is now a list of polygons
        # adding at the beginning the four corners of the image to form the collision shape
        poly = [[[0, 0], [0, self.size[0]], [self.size[1], self.size[0]], [self.size[1], 0]]] + poly

        # Mapping values based on maps_coordinates.json
        with open("maps_coordinates.json", "r") as g:
            coordinates = json.load(g)

        width_mapper = interp1d([0, self.size[1]], [coordinates[self.name]['left'], coordinates[self.name]['right']])
        # print(0, self.size[1], coordinates[self.name]['left'], coordinates[self.name]['right'])
        height_mapper = interp1d([0, self.size[0]], [coordinates[self.name]['top'], coordinates[self.name]['bottom']])
        # print(0, self.size[0], coordinates[self.name]['top'], coordinates[self.name]['bottom'])
        mapper = lambda x: [width_mapper(x[0]).tolist(), height_mapper(x[1]).tolist()]

        # correcting the coordinates
        for p in range(len(poly)):
            for c in range(len(poly[p])):
                # print(poly[p], poly[p][c])
                poly[p][c] = mapper(poly[p][c])
                poly[p][c] = correct_rotation_and_scale(poly[p][c])

        for i in range(len(poly)):
            poly[i] = resolve_geometry(poly[i]).tolist()

        return poly

    def save_polygons(self):
        with open(display_folder + self.name + ".json", "w") as g:
            json.dump(self.polygons, g, indent=4)
        with open(collision_folder + self.name + ".json", "w") as g:
            json.dump(self.corners, g, indent=4)

    def save_image(self, path):
        cv.drawContours(self.original, self.contours, -1, (0, 0, 255), 3)
        cv.imwrite(path, self.original)
        # print(len(self.contours), len(self.polygons))

    def display_polygons(self):
        fig, ax = plt.subplots()
        patches = [MatPolygon(poly, True) for poly in self.polygons]
        p = PatchCollection(patches, alpha=0.4)
        ax.add_collection(p)
        ax.autoscale_view()
        ax.set_title('Polygons_' + self.name)
        plt.show()


if __name__ == "__main__":
    contours_folder = "contours/"
    with open("maps_coordinates.json", "r") as f:
        data = json.load(f)

    for n in data.keys():
        name = n + ".png"
        island = Map(name)
        # island.display_polygons()
        island.save_image(contours_folder + name)
