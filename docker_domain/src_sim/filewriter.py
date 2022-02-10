import sys
import os
import struct
from numpy import random, zeros, save
from time import sleep, time

import config as conf

VERSION = 0
PATCH = 1
LEN = 6

class FileWriter:
    def __init__(self, config: conf.Config):
        self.config = config
        self.isCaching = False
        self.isBin = False
        self.isTimed = False

        if( config.time != 0 or config.vtime != 0 ) :
            self.ltime=time()*1000;
            self.isTimed = True;

        if( isinstance(config.output_filename, str) ) :
            self.isCaching=True;
            if(config.is_bin):
                self.cache = b""
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
        
        elif( config.is_bin ) : 
            raise RuntimeError("You cannot output binary data to stdout");

        if( self.isCaching and self.isBin ) :
            self.f = open(os.open(self.filepath, os.O_CREAT | os.O_WRONLY, 0o644), "wb");
        elif( self.isCaching ) :
            self.cache = ""
            self.f = open(os.open(self.filepath, os.O_CREAT | os.O_WRONLY, 0o644), "w");
        elif( not self.isBin ) : 
            self.f = sys.stdout;

    def setWidthHeight(self, height, width):
        self.height = height
        self.width = width
        # ascii 
        if( not self.isBin ):
            out = ("[ " + str(height) + ", " + str(width) + " ]\n");
            if( not self.isCaching ) :
                self.f.write( out );


class FileWriter:
    def __init__(self, config: conf.Config):
        self.config = config
        self.isCaching = False
        self.isBin = False
        self.isTimed = False

        if( config.time != 0 or config.vtime != 0 ) :
            self.ltime=time()*1000;
            self.isTimed = True;

        if( isinstance(config.output_filename, str) ) :
            self.isCaching=True;
            if(config.is_bin):
                self.cache = b""
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
        
        elif( config.is_bin ) : 
            raise RuntimeError("You cannot output binary data to stdout");

        if( self.isCaching and self.isBin ) :
            self.f = open(os.open(self.filepath, os.O_CREAT | os.O_WRONLY, 0o644), "wb");
        elif( self.isCaching ) :
            self.cache = ""
            self.f = open(os.open(self.filepath, os.O_CREAT | os.O_WRONLY, 0o644), "w");
        elif( not self.isBin ) : 
            self.f = sys.stdout;

    def setWidthHeight(self, height, width):
        self.height = height
        self.width = width
        breakpoint()
        # ascii 
        if( not self.isBin ):
            out = ("[ " + str(height) + ", " + str(width) + " ]\n");
            if( not self.isCaching ) :
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
                 self.f.write(out);


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
                out = "{:.15f}\n".format(point)
            else :
                out = "{:.15f}, ".format(point)
       
            if(self.isCaching) :
                self.cache += out;
            else:
                print(out, end="")
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

