import numpy as np
import math
from matplotlib import pyplot as plt
from shapely.geometry.polygon import Polygon
import visvalingamwyatt as vw
from shapely import geometry, ops


def distance(p1, p2):
    """
    Returns the euclidean distance between two points, using math.hypot()
    :param p1: list of length 2
    :param p2: list of length 2
    :return: euclidean distance between A and B
    """
    if len(p1) != 2 or len(p2) != 2:
        raise ValueError("distance function inputs must be of length 2")

    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def area_triangle(a, b, c):
    """
    Returns the area of the triangle formed by the three points
    :param a: list of length 2
    :param b: list of length 2
    :param c: list of length 2
    :return: area computed with Heron's formula
    """
    for i in [a, b, c]:
        if len(i) != 2:
            raise ValueError("area_triangle function inputs must be of length 2: {} is of length {}.".format(i, len(i)))

    side_a = distance(a, b)
    side_b = distance(b, c)
    side_c = distance(c, a)
    s = 0.5 * (side_a + side_b + side_c)
    return math.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))


def compute_triangles(array, triangles, indices):
    for i in indices:
        try:
            triangles[i] = area_triangle(array[i-1], array[i], array[i+1])
        except IndexError:
            if i == 0:
                triangles[i] = area_triangle(array[len(array) - 1], array[i], array[i + 1])
            elif i == len(array) - 1:
                triangles[i] = area_triangle(array[0], array[i], array[i - 1])
    return triangles


def correct_rotation_and_scale(array):
    # f = lambda x: [(x[0] + 180)*155/36, (-x[1] + 90)*155/36]
    f = lambda x: [x[0] + 180, -x[1] + 90]
    if len(np.array(array).shape) == 1:
        return f(array)
    else:
        return np.apply_along_axis(f, 1, array)


def resolve_geometry(original_poly):
    poly = geometry.Polygon(original_poly)
    if not poly.is_valid:
        poly = poly.buffer(0)
        try:
            x, y = poly.exterior.coords.xy
        except AttributeError:
            # We have a MultiPolygon! We just select the biggest one.
            poly = list(poly)
            poly = sorted(poly, key=lambda a: a.area)
            poly = poly[0]
            x, y = poly.exterior.coords.xy

        poly = list(zip(x, y))
        poly = [list(a) for a in poly]
        return np.array(poly)
    else:
        return np.array(original_poly)


class Polygon:

    def __init__(self, array):
        self.array = correct_rotation_and_scale(np.array(array))

    def simplify(self, thresh=None, nb_points=None):
        simplifier = vw.Simplifier(self.array)
        self.simplified = simplifier.simplify(threshold=thresh)
        if len(self.simplified) <= 2:
            self.simplified = None

        if nb_points is not None:
            if len(self.array) <= nb_points:
                self.simplified = self.array.copy()
            elif self.simplified is None or len(self.simplified) <= nb_points:
                self.simplified = simplifier.simplify(number=nb_points)
            else:
                pass

        # Checking the geometry and attempting to resolve it with shapely
        self.simplified = resolve_geometry(self.simplified)
        # poly = geometry.Polygon(self.simplified)
        # if not poly.is_valid:
        #     poly = poly.buffer(0)
        #     try:
        #         x, y = poly.exterior.coords.xy
        #     except AttributeError:
        #         # We have a MultiPolygon! We just select the biggest one.
        #         poly = list(poly)
        #         poly = sorted(poly, key=lambda a: a.area)
        #         poly = poly[0]
        #         x, y = poly.exterior.coords.xy
        #
        #     poly = list(zip(x, y))
        #     poly = [list(a) for a in poly]
        #     self.simplified = np.array(poly)
        print(len(self.simplified))
