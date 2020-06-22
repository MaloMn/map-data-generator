import tkinter as tk
import json
import glob
import os
import numpy as np
from countries import no_change
from polygons import correct_rotation_and_scale

color_poly = 'black'
color_coll = "red"

# Upload every polygon from the data/ folder
polygons = []
names = []
for path in glob.glob('data/*.json'):
    if not os.path.exists(path.replace('data', 'output')):
        names.append(path)
        with open(path, 'r') as f:
            polygons.append(json.load(f))

print(names)
width = 500


def bounding_box(points):
    x_coordinates, y_coordinates = zip(*points)
    return min(x_coordinates), max(x_coordinates), min(y_coordinates), max(y_coordinates)


def compute_transformations(polygon, center, size):
    points = []
    for i in range(len(polygon)):
        points += list(polygon[i])

    extremum = bounding_box(points)

    # Translation matrix
    current_center = tuple([(extremum[i] + extremum[i + 1]) / 2 for i in [0, 2]])
    translation_1 = np.subtract((0, 0), current_center)

    # Scaling matrix
    current_size = max([abs(extremum[i] - extremum[i + 1]) for i in [0, 2]])
    scaling = size / current_size * np.eye(2)

    # Moving back to required center
    translation_2 = np.array(center)

    return translation_1, scaling, translation_2


def reverse_transformations(translation_1, scaling, translation_2):
    return -translation_1, 1 / scaling[0, 0] * np.eye(2), -translation_2


def apply_transformations(polygon, translation_1, scaling, translation_2):
    for i in range(len(polygon)):
        if type(polygon[i]) != np.ndarray:
            poly = np.array(polygon[i])
        else:
            poly = polygon[i]

        # Applying both matrices
        new_poly = poly + translation_1
        new_poly = [list(x.dot(scaling)) for x in new_poly]
        # Place it at required point
        new_poly = np.add(translation_2, new_poly)

        polygon[i] = new_poly.tolist()

    return polygon


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.bind("<Button-1>", self.left_click)
        self.parent.bind("<space>", self.right_click)

        self.canvas = tk.Canvas(parent, width=width, height=width)
        self.canvas.pack()
        self.display_polygon()

    def display_polygon(self):
        """
        Displays a polygon, and initializes the variables needed.
        :return: nothing
        """
        # Clear canvas
        self.canvas.delete("all")
        try:
            # Use first polygon of list
            print(names[0])
            polygon = polygons[0]
            for i in range(len(polygon)):
                polygon[i] = no_change(polygon[i])

            self.matrices = compute_transformations(polygon, (width/2,) * 2, width * 4 / 5)
            apply_transformations(polygon, *self.matrices)

            for p in polygon:
                self.canvas.create_polygon(p)

        except IndexError:
            print('No more polygons.')
            self.parent.destroy()

        self.collision = []

    def left_click(self, event):
        self.point(event.x, event.y)
        self.collision.append([event.x, event.y])

    def right_click(self, event):
        # Need to save that polygon
        if len(self.collision) > 0:
            reverse_matrices = reverse_transformations(*self.matrices)
            self.collision = apply_transformations([self.collision], *reverse_matrices[::-1])[0]
            self.collision = correct_rotation_and_scale(self.collision).tolist()
            self.collision.append(self.collision[0])

            with open(names[0].replace('data', 'output'), 'w') as f:
                json.dump(self.collision, f)

        polygons.pop(0)
        names.pop(0)
        self.display_polygon()

    def point(self, x, y):
        radius = 2
        x1, y1 = (x - radius), (y - radius)
        x2, y2 = (x + radius), (y + radius)
        self.canvas.create_oval(x1, y1, x2, y2, fill=color_coll)


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()
