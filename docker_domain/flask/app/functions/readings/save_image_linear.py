import os
from PIL import Image, ImageOps, ImagePalette
from numpy import uint8

# Takes in the name of a binary file, a deals with the data by creating an image of the array and returns bath


def save_image(filename, data, output_folder, format=0, colors=[]):

    # importing image
    img = Image.fromarray(uint8(data*255/5), 'L')
    if len(colors) == 3:
        # coloring
        img = ImageOps.colorize(img, black=colors[0],
                                mid=colors[1], white=colors[2])

    # if there is no output folder, create one
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # selecting the format
    if format == 1:
        # for PNG format
        name = filename[:-4] + '.png'
        # set the path and save the image in it
        path = str(output_folder + name)
        img.save(path, 'PNG')
    elif format == 2:
        # for TIFF format
        name = filename[:-4] + '.tiff'
        # set the path and save the image in it
        path = str(output_folder + name)
        img.save(path, 'TIFF')
    else:
        # for JPEG format
        name = filename[:-4] + '.jpg'
        # set the path and save the image in it
        path = str(output_folder + name)
        img.save(path, 'JPEG')

    img = Image.open(path)
    return name, img.size, img.mode, img.format, img.palette
