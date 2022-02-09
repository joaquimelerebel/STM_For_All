import sys
import os
import struct
from math import exp, log
from PIL import Image
from numpy import asarray, random, std, zeros, save, uint8
from time import sleep, time
from json import dumps

import config as conf
VERSION = 0
PATCH = 1
LEN = 6


# get
class FileWriter:
    def __init__(self, config: conf.Config):
        self.config = config
        self.cache = b""
        self.isCaching = False
        self.isBin = False
        self.isTimed = False

        if( config.time != 0 or config.vtime != 0 ) :
            self.ltime=time()*1000;
            self.isTimed = True;

        if( isinstance(config.output_filename, str) ) :
            self.isCaching=True;
            if(config.is_bin):
                self.isBin = True

                # file path generation
                if(config.isNumpyBin) :
                    self.filepath = config.output_filename if( ".npy" in config.output_filename ) else config.output_filename + ".npy"
                else : 
                    self.filepath = config.output_filename if( ".bst" in config.output_filename ) else config.output_filename + ".bst"
            else :
                self.filepath = config.output_filename if( ".mst" in config.output_filename ) else config.output_filename + ".mst"

            if( config.isNumpyBin and (not self.isCaching )) : 
                raise RuntimeError("You cannot ask for a Numpy array output and a timed output at the same time");
            if( not self.isCaching ) :
                self.f = open(os.open(self.filepath, os.O_CREAT | os.O_WRONLY, 0o644), "wb");
        elif(config.is_bin) : 
                raise RuntimeError("You cannot output binary data to stdout");

    def setWidthHeight(self, height, width):
        self.height = height
        self.width = width
        # ascii 
        if( not self.isBin ):
            out = ("[ " + str(width) + ", " + str(height) + " ]\n").encode("ascii");
            if( self.isCaching ) :
                self.f.write( out );
            else : 
                self.cache += out;
        # binary output  
        elif( self.isBin and not self.config.isNumpyBin ) :  
            # set the header up
            # file type identifier
            out = b"MST"
            # version control
            out += struct.pack(">h", VERSION)
            # patch control
            out += struct.pack(">h", PATCH)
            # length of each data point, in power of 2
            out += struct.pack(">B", LEN)
            # height
            out += struct.pack(">i", self.height)
            # width
            out += struct.pack(">i", self.width)
            # metadata(16 bytes)
            for i in range(0, 16):
                out += struct.pack(">b", 0x69);

            if( self.isCaching ) :
                self.cache += out;
            else :
                if( self.isBin ):
                    self.f.write(out);
                else :
                    self.f.write(out.decode("ascii"))

    def writePoint(self, point, isStop) :
        if( self.isTimed ) :
            # wait time calculation and wait
            deltaT = (time()*1000) - self.ltime
            self.wtime = float(random.uniform(0-(self.config.vtime/2), self.config.vtime/2) + self.config.time - deltaT)/1000.0;
            if self.wtime > 0 :
                sleep( self.wtime );
            ctime = time()*1000;
            deltaT = ctime - self.ltime;
            self.ltime = time()*1000;


        # for binary points 
        if( self.isBin and not self.config.isNumpyBin ) :  
            b_point = struct.pack(">d", point)
            if( self.isCaching ) :
                self.cache += b_point;
            else : 
               self.f.write(b_point);
        #ASCII output
        elif( not self.config.isNumpyBin ) :
            if( isStop == True ) :
                out = "{:.15f}\n".format(point).encode("ascii")
            else :
                out = "{:.15f}, ".format(point).encode("ascii")
       
            if(self.isCaching) :
                self.cache += out;
            else:
                print(out.decode("ascii"), end="")
        if( self.isTimed ):
            return deltaT
        else :
            return 0;


    def writeAll(self, arr):
        if( self.config.isNumpyBin ) :
            save(self.filepath, arr)
        elif( self.isCaching ) :
            if( self.isBin ) :
                with open(os.open(self.filepath, os.O_CREAT | os.O_WRONLY, 0o644), "wb") as f:
                    f.write(self.cache);
            else:
                with open(os.open(self.filepath, os.O_CREAT | os.O_WRONLY, 0o644), "w") as f:
                    f.write(self.cache) 
        elif( self.isBin ) :
            self.f.close();

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
    fw.setWidthHeight(height, width)

    # allocation of the output array of voltages
    data_voltages = zeros((height, width))
    dataSet = zeros((height, width)) 
    tpoints = zeros((height, width))

    if( config.time != 0 or config.vtime != 0 ) :
        isTimed = True;
    else :
        isTimed = False;
    # create the map of voltages
    for h in range(0, height):
        for w in range(0, width):

            # error generation
            if (config.is_normal_error) :
                dataSet[h, w] = data[h, w] + random.normal(config.error_mean, config.error)
            elif(config.is_uniform_error) :
                dataSet[h, w] = data[h, w] + random.uniform(0-(config.error/2), config.error/2) + config.error_mean
            else :
                dataSet[h, w] = data[h, w]

            #  convert point to 0-5V range
            if(config.is_exponential_scale):
                data_voltage = (exp(dataSet[h, w]) * 5) / 5.5602316477276757e+110
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
                data_voltage = (dataSet[h, w]*5)/255

            # applying borders
            if data_voltage > 5:
                data_voltage = 5
            if data_voltage < 0:
                data_voltage = 0

            data_voltages[h, w] = data_voltage

            # printing result
            if(w == width-1):
                tpoints[h, w] = fw.writePoint(data_voltage, True)
            else:
                tpoints[h,w] = fw.writePoint(data_voltage, False)


    fw.writeAll(data_voltages)

    if(config.is_statistical):
        # creation of the image statistics
        dataflatten = data.flatten()
        maxImage = float(max(dataflatten))
        minImage = float(min(dataflatten))
        meanImage = float(sum(dataflatten)/len(dataflatten))
        stdevImage = float(std(dataflatten))
        statistics_set = {"Image": {
            "max": maxImage, "min": minImage, "mean": meanImage, "stdev": stdevImage}}
        # creation of the image with error statistics
        dataflatten = dataSet.flatten()
        maxWith_error = float(max(dataflatten))
        minWith_error = float(min(dataflatten))
        meanWith_error = float(sum(dataflatten)/len(dataflatten))
        stdevWith_error = float(std(dataflatten))
        statistics_set["ImageWithError"] = {
            "max": maxWith_error, "min": minWith_error, "mean": meanWith_error, "stdev": stdevWith_error}

        # creation of the output statistics
        data_voltages_flatten = data_voltages.flatten()
        maxVolt = float(max(data_voltages_flatten))
        minVolt = float(min(data_voltages_flatten))
        meanVolt = float(sum(data_voltages_flatten)/len(data_voltages_flatten))
        stdevVolt = float(std(data_voltages_flatten))
        statistics_set["Voltages"] = {
            "max": maxVolt, "min": minVolt, "mean": meanVolt, "stdev": stdevVolt}
        
        #timing data
        if( isTimed ):
            dataflatten = tpoints.flatten()
            maxWith_error = float(max(dataflatten))
            minWith_error = float(min(dataflatten))
            meanWith_error = float(sum(dataflatten)/len(dataflatten))
            stdevWith_error = float(std(dataflatten))
            statistics_set["TimeMS"] = {
                "max": maxWith_error, "min": minWith_error, "mean": meanWith_error, "stdev": stdevWith_error}

        json_object = dumps(statistics_set, indent = 4) 
        print(json_object)
