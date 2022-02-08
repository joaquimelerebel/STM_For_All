import sys
import os
import struct
from math import exp, log
from PIL import Image
from numpy import asarray, random, std, zeros, save

import config as conf
VERSION=0
PATCH=1
LEN=6


# get
class FileWriter:
    def __init__(self, config: conf.Config):
        self.config = config
        self.cache = ""
        self.isCaching = False
        self.isBin = False

        if(isinstance(config.output_filename, str)):
            self.isCaching = True
            if(config.is_bin):
                self.isBin = True
                self.cache = b""
        else:
            self.f = sys.stdout

    def setWidthHeight(self, height, width):
        self.height = height
        self.width = width
        if(self.isCaching == False):
            print("[ " + str(width) + ", " + str(height) + " ]\n")
        elif(self.isBin == False):
            self.cache += "[ " + str(width) + ", " + str(height) + " ]\n"

    def writePoint(self, point, isStop):
        if(self.isCaching == False):
            print("{:.4f}, ".format(point), end="")
            if(isStop == True):
                print()
        elif(self.isBin == False):
            if(isStop == True):
                self.cache += "{:.4f}\n".format(point)
            else:
                self.cache += "{:.4f}, ".format(point)

    def writeAll(self, arr):
        if(self.isCaching == True):
            if(self.isBin == True):
                if( self.config.isNumpyBin == True ):
                    save(self.config.output_filename, arr)
                else : 
                    with open(os.open(self.config.output_filename, os.O_CREAT | os.O_WRONLY, 0o444), "wb") as f:
                        # set the header up
                        #file type identifier
                        f.write(b"MST");
                        #version control 
                        b_ver = struct.pack(">h", VERSION);
                        f.write(b_ver);
                        #patch control 
                        b_patch = struct.pack(">h", PATCH);
                        f.write(b_patch);
                        #length of each data point, in power of 2
                        b_len = struct.pack(">B", LEN);
                        f.write(b_len);
                        #height
                        b_height = struct.pack(">i", self.height);
                        f.write(b_height);
                        #width
                        b_width = struct.pack(">i", self.width);
                        f.write(b_width)
                        #metadata(16 bytes)
                        for i in range(0, 16):
                            b_blank = struct.pack(">b", 0);
                            f.write(b_blank);
                        #data
                        for h in range(0, self.height) :
                            for w in range(0, self.width) :
                                b_point = struct.pack(">d", arr[h, w]);
                                f.write( b_point )
            else :
                with open(os.open(self.config.output_filename, os.O_CREAT | os.O_WRONLY, 0o444), "w") as f:
                    f.write(self.cache)

# get pixel value of each pixel of the picture
# each point is a float64

# int width, int height

# string file format :
# [ width, height ]
# x1y1, x2y1, ... xwidthy1 \no\n
# x1y2, x2y2, ... xwidthy2
# .
# .
# .
# x1yheight, x2yheight, ... xwidthyheight

def sim_image(config: conf.Config):
    image = Image.open(config.simulation_filename).convert('L')
    width, height = image.size
    data = asarray(image)
    fw = FileWriter(config)

    # print in the chosen file (stdout or a file)
    # if( isinstance( config.output_filename, str) ) :
    #    if( config.bin ) :
    #        f = open( os.open(config.output_filename, os.O_CREAT | os.O_WRONLY, 0o777), "wb" );
    #    else :
    #        f = open( os.open(config.output_filename, os.O_CREAT | os.O_WRONLY, 0o777), "w" );
    # else :
    #    f = sys.stdout;
    #
    #f.write( "[ " + str( width ) + ", " + str( height )  + " ]\n" );
    fw.setWidthHeight(height, width)

    
    # creation of the image statistics
    if(config.is_statistical):
        dataflatten = data.flatten()
        maxImage = max(dataflatten)
        minImage = min(dataflatten)
        meanImage = sum(dataflatten)/len(dataflatten)
        stdevImage = std(dataflatten)
        statistics_set = {"Image": {
            "max": maxImage, "min": minImage, "mean": meanImage, "stdev": stdevImage}}

    # allocation of the output array of voltages
    data_voltages = zeros((height, width))
    dataSet = zeros((height, width))
    # create the map of voltages
    for h in range(0, height):
        for w in range(0, width):

            # error generation
            if(config.is_normal_error):
                dataSet[h, w] = data[h, w] + random.normal(config.error_mean, config.error)
            elif(config.is_uniform_error):
                dataSet[h, w] = data[h, w] + random.uniform(0-(config.error/2),
                                   config.error/2) + config.error_mean
            else:
                dataSet[h, w] = data[h, w]
            # breakpoint();
            #  convert point to 0-5V range
            if(config.is_exponential_scale):
                data_voltage = (exp(data[h, w]) * 5) / 5.5602316477276757e+110
            # elif( config.is_complexe_exponential_scale ) :
            #    pass;
                # J_T prop exp(-A\Phi^{1/2}s)
                # A=sqrt((4*\pi/h)*2m)=1.025 Ang^-1 eV^-(1/2)
                # m = mass of the free electron
                # cf surface studies by scanning tunneling mircroscopy 1982 G. Binning, H. Rohrer
                # trying to convert with realistic values

                # if constant tunneling current :
                # \Phi^(1/2)s=const
                # Pz is the index of the displacement : potential at the piezo borders
            else:
                data_voltage = (data[h, w]*5)/255

            # applying filters
            if data_voltage > 5:
                data_voltage = 5
            if data_voltage < 0:
                data_voltage = 0

            data_voltages[h, w] = data_voltage

            # printing result
            # if( w == width-1 ) :
            #    f.write( str( data_voltage ) + '\n' );
            # else :
            #    f.write( str( data_voltage ) + ", " );
            if(w == width-1):
                fw.writePoint(data_voltage, True)
            else:
                fw.writePoint(data_voltage, False)


    # if( isinstance(config.output_filename, str) ) :
    #    f.close()
    fw.writeAll(data_voltages)

    if(config.is_statistical):

        # creation of the image with error statistics
        dataflatten = data.flatten()
        maxWith_error = max(dataflatten)
        minWith_error = min(dataflatten)
        meanWith_error = sum(dataflatten)/len(dataflatten)
        stdevWith_error = std(dataflatten)
        statistics_set["ImageWithError"] = {
            "max": maxWith_error, "min": minWith_error, "mean": meanWith_error, "stdev": stdevWith_error}

        # creation of the output statistics
        data_voltages_flatten = data_voltages.flatten()
        maxVolt = max(data_voltages_flatten)
        minVolt = min(data_voltages_flatten)
        meanVolt = sum(data_voltages_flatten)/len(data_voltages_flatten)
        stdevVolt = std(data_voltages_flatten)
        statistics_set["Voltages"] = {
            "max": maxVolt, "min": minVolt, "mean": meanVolt, "stdev": stdevVolt}

        print(statistics_set)

        # output of the statistics
        print("-- image --")
        print("max : " + str(maxImage))
        print("min : " + str(minImage))
        print("mean : " + str(meanImage))
        print("st dev : " + str(stdevImage))
