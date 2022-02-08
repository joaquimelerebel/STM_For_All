import os
from PIL import Image
from numpy import uint8

# Takes in the name of a binary file, a deals with the data by creating an image of the array and returns bath


def save_image(filename, data, output_folder):

    # importing image
    img = Image.fromarray(uint8(data*255/5), 'L')

    # if there is no output folder, create one
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # set the path and save the image in it
    path = output_folder + filename[:-4] + '.jpg'
    img.save(path, 'JPEG')
    return path
