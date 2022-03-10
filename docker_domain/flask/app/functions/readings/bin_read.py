from numpy import zeros, float64, array, load

from functions.readings.save_image_linear import save_image

# Takes in the name of a binary file, a deals with the data by creating an image of the array and returns bath


def binary_read(file, input_folder, output_folder, format=0):
    filedata = load(str(input_folder) + str(file))
    return save_image(file, filedata, output_folder, format)
