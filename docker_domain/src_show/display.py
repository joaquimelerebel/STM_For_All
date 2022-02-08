import sys
import re
import struct 

from numpy import asarray, zeros, float64, array, load
from PIL import Image


def readMSTfile(filename) :
        try :
            with open(filename, "rb") as f :
                filecontent = f.read();
        except IOError as err :
            sys.stderr.write( f"file does not exists : {err=}" );
            return 0;

        try : 
            if( len(filecontent) < 32 ) : 
                raise IOError("file is too short");
            b_header = filecontent[0:32];
            # read the header
            mst = b_header[0:3].decode("ascii");
            if(mst != "MST") :
                raise IOError("not a MST file type")

            version = struct.unpack(">h", b_header[3:5])[0];
            patch = struct.unpack(">h", b_header[5:7])[0];
            point_length = struct.unpack(">B", b_header[7:8])[0];
            height = struct.unpack(">i", b_header[8:12])[0];
            width = struct.unpack(">i", b_header[12:16])[0];
            metadata = b_header[16:32];
            
            point_byte_len = int((2**point_length)/8);
            supposed_len = width*height*point_byte_len;
            if( len(filecontent[32:] ) != supposed_len ) :
                raise IOError("file not the supposed length");
            
            #TODO to change according to the file format point size
            data = zeros((height, width), dtype=float64)
            for i in range(0, supposed_len, point_byte_len):
                point = struct.unpack(">d", filecontent[32+i: 32+i+point_byte_len])[0];
                data[int((i/point_byte_len)/width), int(i/point_byte_len)%width] = point;

            return (data, height, width)
        except IOError as err :
            sys.stderr.write( f"file does not corresponds to the format : {err=}" );
            return 0;

        except ValueError as err :
            sys.stderr.write( f"could not convert data to right format : {err=}" );
            return 0;



def main(filename, binary, output):

    if ("-bin" in binary ):
        if (binary == "-binNP"):
            file = load(filename)
            height, width = file.shape 
            
        if (binary == "-bin") :
            file, height, width = readMSTfile(filename);

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
