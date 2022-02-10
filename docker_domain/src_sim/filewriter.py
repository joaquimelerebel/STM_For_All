import sys
import os
import struct
from numpy import random, zeros, save
from time import sleep, time

import config as conf
import gen_var as gen


class FileWriter:
    def __init__(self, config: conf.Config):
        self.config = config
        self.isCaching = False
        self.isBin = False
        self.isTimed = False
        self.isCtable = config.isCtable
        self.isCtable16 = config.isCtable16

        if( config.time != 0 or config.vtime != 0 ) :
            self.ltime=time()*1000;
            self.isTimed = True;

        if( config.output_filename != "" ) :
            self.isCaching=True;
            if(config.is_bin):
                self.cache = b""
                self.isBin = True

                # file path generation
                if(config.isNumpyBin) :
                    self.filepath = config.output_filename if( ".npy" in config.output_filename ) else config.output_filename + ".npy"
                else : 
                    self.filepath = config.output_filename if( ".bst" in config.output_filename ) else config.output_filename + ".bst"
            elif( self.isCtable or self.isCtable16 ) :
                self.filepath = config.output_filename if( ".h" in config.output_filename ) else config.output_filename + ".h"
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
            if( self.isCtable16 ) :
                out = (     f"const int final_width = {width};\n" 
                        +   f"const int final_height = {height};\n"  
                        +   f"const unsigned short table [{width*height}] = " + "{");
            elif( self.isCtable ) :
                out = ("const double table [" + str(height) + "][" + str(width) + "] = {{");
            else : 
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
            out += struct.pack(">h", gen.VERSION)
            # patch control
            out += struct.pack(">h", gen.PATCH)
            # length of each data point, in power of 2
            out += struct.pack(">B", gen.LEN)
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


    def writePoint(self, h, w, point, isStop) :
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
            if( self.isCtable16 ) :
                # convert to the ADC format 
                # ADC of 16 bits : max val 65536
                nval = int((point*65536)/5);
                b_point = struct.pack(">H", nval).hex() 
            if( isStop ) :
                if( self.isCtable16 ) :
                    # convert to the ADC format 
                    # ADC of 16 bits : max val 65536
                    nval = int((point*65536)/5);

                    out = f"0x{b_point}, \n"
                    if( h == self.height - 1 and  w == self.width - 1 ):
                        out = f"0x{b_point}" + "};\n"
                elif( self.isCtable ) :
                    out = f"{point:.15f}" + "},\n{"
                    if( h == self.height - 1 and  w == self.width - 1 ):
                        out = f"{point:.15f}" + "}};"
                else : 
                    out = f"{point:.15f}\n"
            elif(self.isCtable16) :
                out = f"0x{b_point}, "
            else :
                out = f"{point:.15f}, ";

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

