from numpy import zeros, float64, array, load

from save_image import save_image

# Takes in the name of a binary file, a deals with the data by creating an image of the array and returns bath


def binary_read(file, input_folder, output_folder):
    filedata = load(str(input_folder) + str(file))
    height, width = filedata.shape

    # creating our array to have our image
    data = zeros((height, width, 3), dtype=float64)
    value = filedata*255/5
    data = array([value, value, value]).transpose()
    return save_image(file, data, output_folder)
