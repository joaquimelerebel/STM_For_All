import sys
import struct
from flask import flash
from numpy import zeros, float64, array

from functions.readings.save_image_linear import save_image


# Takes in the name of a file, and the input folder, and gives back the data array created from the reading (2D pixel array)
def custom_read(file, input_folder):
    try:
        with open(str(input_folder) + str(file), "rb") as f:
            filecontent = f.read()
    except IOError as err:
        sys.stderr.write(f"file does not exists : {err=}")
        flash("File does not exists : ", err)
        return 0

    try:
        if(len(filecontent) < 32):
            raise IOError("file is too short")
        b_header = filecontent[0:32]
        # read the header
        mst = b_header[0:3].decode("ascii")
        if(mst != "MST"):
            raise IOError("not a MST file type")
        version = struct.unpack(">h", b_header[3:5])[0]
        patch = struct.unpack(">h", b_header[5:7])[0]
        point_length = struct.unpack(">B", b_header[7:8])[0]
        height = struct.unpack(">i", b_header[8:12])[0]
        width = struct.unpack(">i", b_header[12:16])[0]
        metadata = b_header[16:32]
        point_byte_len = int((2**point_length)/8)
        supposed_len = width*height*point_byte_len
        if(len(filecontent[32:]) != supposed_len):
            raise IOError("file not the supposed length")

        # TODO to change according to the file format point size
        data = zeros((height, width), dtype=float64)
        for i in range(0, supposed_len, point_byte_len):
            point = struct.unpack(
                ">d", filecontent[32+i: 32+i+point_byte_len])[0]
            data[int((i/point_byte_len)/width),
                 int(i/point_byte_len) % width] = point

        # creating our array to have our image

        return data
    except IOError as err:
        sys.stderr.write(f"file does not corresponds to the format : {err=}")
        flash('File does not corresponds to the format :', err)
        return 0

    except ValueError as err:
        sys.stderr.write(f"could not convert data to right format : {err=}")
        flash('Could not convert data to right format  :', err)
        return 0
