import re
from numpy import asarray, zeros, float64, array

from functions.readings.save_image_linear import save_image

# Takes in the name of a file, and the input folder, and gives back the data array created from the reading (2D pixel array)


def file_read(file, input_folder):
    # try opening output_filename, if there is none, let's do it in stdout
    if(isinstance(file, str)):
        f = open(str(input_folder) + str(file), "r")

    # collecting the size of the array
    fileline = f.readline()
    size = re.sub(r"[\[-\]]", "", fileline).replace(" ", "").split(",")

    # preventing /n by retrieving 2 values from the width
    height, width = asarray(size, int)

    # creating our array to have our image
    data = zeros([height, width], dtype=float64)

    for h in range(0, height):
        line = f.readline()  # reading each line
        # sanitizing the string and converting it (linear)
        placeholder = line.replace(" ", "").split(",")
        placeholder = list(filter(None, placeholder))
        print(len(placeholder))
        data[h] = asarray(placeholder, float64)

    # closing the file
    if(isinstance(file, str)):
        f.close()

    return data
