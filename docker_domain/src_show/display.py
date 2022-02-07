import sys
import numpy as np
import re

from math import exp
from PIL import Image


def main(filename):

    # try opening output_filename, if there is none, let's do it in stdout
    if(isinstance(filename, str)):
        f = open(filename, "r")
    else:
        f = sys.stdout

    # collecting the size of the array
    fileline = f.readline()
    size = re.sub(r"[\[-\]]", "", fileline).replace(" ", "").split(",")

    # preventing /n by retrieving 2 values from the width
    height, width = np.asarray(size, int)-[0, 2]

    # creating our array to have our image
    data = np.zeros((height, width, 3), dtype=np.float64)

    for h in range(0, height):
        line = f.readline()
        value = np.asarray(line.replace(
            " ", "").split(","), np.float64)[0:width]*255/5
        data[h] = np.array([value, value, value]).transpose()

    img = Image.fromarray(data, 'RGB')
    img.save('result.png')
    img.show('result.png')

    if(isinstance(filename, str)):
        f.close()


if(__name__ == "__main__"):
    main(sys.argv[1])
