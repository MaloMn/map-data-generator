from wand.api import library
import wand.color
import wand.image
import os

folder_png = 'flags_png/'

# List svg files
folder = 'flags/'
svg_files = os.listdir(folder)

for file in svg_files:
    svg_file = open(folder + file, "rb")

    try:
        with wand.image.Image() as image:
            with wand.color.Color('transparent') as background_color:
                library.MagickSetBackgroundColor(image.wand,
                                                 background_color.resource)
            image.read(blob=svg_file.read())
            png_image = image.make_blob("png32")

        with open(folder_png + file.replace('.svg', '') + '.png', "wb") as out:
            out.write(png_image)
    except:
        print('Problem with: ' + folder_png + file.replace('.svg', '') + '.png')