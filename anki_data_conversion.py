# coding: utf-8
import csv
import logging
import json

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="anki_data_conversion.log",
                    level=logging.INFO,
                    format=LOG_FORMAT,
                    filemode='w')
logger = logging.getLogger()


class Data:

    def __init__(self, path):
        self.data = []
        self.heading = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, dialect='excel')
            for row in reader:
                self.data.append(row)

        self.clean()

    def clean(self):
        self.data = [[a[1], a[6], a[11], a[16], a[21], a[26], a[27], a[32], a[33]] for a in self.data]
        self.heading = self.data[0]
        self.data.pop(0)

    def replace(self, value, replacement):
        b = False
        n = 0
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.data[i][j] == value:
                    self.data[i][j] = replacement
                    b = True
                    n += 1

        if b:
            logger.info('Changing from /{}/ to /{}/ {} time{}'.format(value, replacement, n, '' if n <= 1 else 's'))
        else:
            logger.warning('Could not find /{}/ to replace it by /{}/'.format(value, replacement))

    def add_line(self, line):
        if len(line) == len(self.data[0]):
            self.data.append(line)
            logger.info('Added a new line for /{}/'.format(line[0]))
        else:
            logger.warning('Could not add new line for /{}/: {} != {}'.format(line[0], len(line), len(self.data[0])))

    def remove(self, country):
        line = None
        for i in range(len(self.data)):
            if self.data[i][0] == country:
                line = i

        if line is not None:
            self.data.pop(line)
            logger.info('Line n°{} ({}) was removed.'.format(line, self.data[line][0]))
        else:
            logger.warning('No line was found containing /{}/'.format(value))

    def column(self, name):
        try:
            i = self.heading.index(name)
            return [a[i] for a in self.data]
        except ValueError:
            print('The /{}/ column does not exist. Possible names are: '.format(name), self.heading)

    def save(self, name):
        print(self.heading)
        with open(name, 'w') as f:
            json.dump(self.data, f, indent=3)


if __name__ == "__main__":
    import os
    import numpy as np
    import cv2 as cv
    from scipy.interpolate import interp1d

    tab = Data('data/data.csv')
    tab.replace('Australia (Oceania)', 'Oceania')
    tab.add_line(['Saint Pierre and Miquelon', 'Saint Pierre'] + ['' for i in range(7)])
    tab.remove('United Kingdom')
    print(tab.column('Country'))
    tab.save('cleaned_data.json')

    # list_polygons = os.listdir("countries/")
    # list_polygons = [a.replace('.json', '') for a in list_polygons]
    #
    # for country, image in zip(tab.column('Country'), tab.column('Map')):
    #     if country in list_polygons and image != '':
    #         a = image.find('"')
    #         path = image[a+1:]
    #         b = path.find('"')
    #         path = path[:b]
    #         path = 'media/' + path.replace('.png', '') + '2.png'
    #         print(path)
    #
    #         with open('countries/' + country + '.json', 'r') as f:
    #             polygon = json.load(f)
    #
    #         # Create a black image
    #         img = np.zeros((500, 500, 3), np.uint8)
    #
    #         # Collect every x coordinates
    #         x, y = [], []
    #         for p in polygon:
    #             x += [a[0] for a in p]
    #             y += [a[1] for a in p]
    #
    #         a, b = min(x), max(x)
    #         c, d = min(y), max(y)
    #         x = interp1d([a, b], [0.0, 500.0])
    #         y = interp1d([c, d], [0.0, 500.0])
    #
    #         for p in polygon:
    #             pts = p.copy()
    #             for i in range(len(pts)):
    #                 pts[i] = [int(x(pts[i][0])), int(y(pts[i][1]))]
    #
    #             pts = np.array(pts, np.int32)
    #             pts = pts.reshape((-1, 1, 2))
    #             cv.polylines(img, [pts], True, (0, 255, 255))
    #
    #         cv.imwrite(path, img)
