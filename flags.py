import wikipedia as wiki
import urllib.request
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

folder = "flags/"

images = wiki.page("Gallery of sovereign state flags").images
print(len(images))

for i in images[1:]:
    try:
        filename = i.rsplit('/', 1)[-1]

        name = folder + filename
        name = name.replace("Flag_of_", "")
        name = name.replace("_", " ")
        print(name)
        urllib.request.urlretrieve(i, name)
        name = name.replace(".svg", ".png")
        drawing = svg2rlg(name)
        renderPM.drawToFile(drawing, name, fmt="PNG")
    except:
        print("NOT WORKING: " + i)
