import sys
import re

from numpy import asarray, zeros, float64, array, load
from PIL import Image


def main(filename, binary, output):

    if (binary == "-bin"):
        file = load(filename)
        height, width = file.shape 
        
        # creating our array to have our image
        data = zeros((height, width, 3), dtype=float64)
        value = file*255/5
        data = array([value, value, value]).transpose()

        # image
        img = Image.fromarray(data, 'RGB')
        img.save(output)
        img.show(output)
            
    elif (binary =="-f"):
        # try opening output_filename, if there is none, let's do it in stdout
        if(isinstance(filename, str)):
            f = open(filename, "r")
        else:
            f = sys.stdout
        # collecting the size of the array
        fileline = f.readline()
        size = re.sub(r"[\[-\]]", "", fileline).replace(" ", "").split(",")

        # preventing /n by retrieving 2 values from the width
        height, width = asarray(size, int)-[0, 1]

        # creating our array to have our image
        data = zeros((height, width, 3), dtype=float64)

        for h in range(0, height):
            line = f.readline()
            value = asarray(line.replace(" ", "").split(","), float64)[0:width]*(255/5)
            data[h] = array([value, value, value]).transpose()

        # image
        img = Image.fromarray(data, 'RGB')
        img.save(output)
        img.show(output)

        if(isinstance(filename, str)):
            f.close()
    else:
        print("Wrong parameters")

if(__name__ == "__main__"):
    if len( sys.argv ) <= 2 :
        print( "Not enough arguments" )
        exit()
    main(sys.argv[1], sys.argv[2], sys.argv[3])
