import tkinter as tk
import json

color_poly = 'black'
color_coll = "#476042"

# Upload every polygon here.
for
polygons = None


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.bind("<Button-1>", self.left_click)
        self.parent.bind("<Button-3>", self.right_click)

        self.canvas = tk.Canvas(parent, width=500, height=500)
        self.canvas.pack()

        self.display_polygon()

    def display_polygon(self):
        """
        Displays a polygon, and initializes the variables needed.
        :return: nothing
        """
        self.canvas.delete("all")
        # Use first polygon of list
        try:
            polygon = polygons[0]
        except IndexError:
            # TODO check that function
            self.destruct()

        # TODO Scaling down and fitting it onto the screen
        # polygon = func(polygon)

        self.canvas.create_polygon([[100, 200], [300, 400], [100, 250]])
        self.collision = []

    def left_click(self, event):
        self.point(event.x, event.y)
        self.collision.append([event.x, event.y])

    def right_click(self, event):
        # Need to save that polygon
        print(self.collision)
        polygons.pop(0)
        self.display_polygon()

    def point(self, x, y):
        x1, y1 = (x - 1), (y - 1)
        x2, y2 = (x + 1), (y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill=color_coll)


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
