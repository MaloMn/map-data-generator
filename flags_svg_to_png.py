from wand.api import library
import wand.color
import wand.image
import os

folder_png = 'flags/'
width = '500'
height = 'x500'
heights = []

# List svg files
folder = 'wiki_flags/'
svg_files = os.listdir(folder)

for file in svg_files:
    svg_file = open(folder + file, "rb")

    future_name = file.replace('.svg', '.png')
    future_name = future_name.replace('flag-', '')

    try:
        with wand.image.Image() as image:
            with wand.color.Color('white') as background_color:
                library.MagickSetBackgroundColor(image.wand, background_color.resource)

            image.read(blob=svg_file.read())
            image.transform(resize=str(height))
            heights.append(image.height)
            png_image = image.make_blob("png32")

        with open(folder_png + future_name, "wb") as out:
            out.write(png_image)
    except :
        print('Problem with: ' + future_name)

print(heights)
