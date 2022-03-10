from numpy import zeros, float64, array, load

from functions.readings.save_image_linear import save_image

# Takes in the name of a file, and the input folder, and gives back the data array created from the reading (2D pixel array)


def binary_read(file, input_folder):
    filedata = load(str(input_folder) + str(file))
    return filedata
