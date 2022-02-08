import re
from numpy import asarray, zeros, float64, array

from functions.readings.save_image import save_image

# Takes in the name of a file, a deals with the data by creating an image of the array and returns bath


def file_read(file, input_folder, output_folder):
    # try opening output_filename, if there is none, let's do it in stdout
    if(isinstance(file, str)):
        f = open(str(input_folder) + str(file), "r")

    # collecting the size of the array
    fileline = f.readline()
    size = re.sub(r"[\[-\]]", "", fileline).replace(" ", "").split(",")

    # preventing /n by retrieving 2 values from the width
    height, width = asarray(size, int)-[0, 1]

    # creating our array to have our image
    data = zeros((height, width, 3), dtype=float64)

    for h in range(0, height):
        line = f.readline()  # reading each line
        value = asarray(line.replace(" ", "").split(","), float64)[
            0:width]*(255/5)  # sanitizing the string and converting it (linear)
        data[h] = array([value, value, value]
                        ).transpose()  # making it RGB

    # closing the file
    if(isinstance(file, str)):
        f.close()

    return save_image(file, data, output_folder)
