#!/bin/env python 


import argparse 
from serial_com import Serial_COM 
import numpy as np
import createmap
import cmd_int as cmd


#setting up the default config
class Config : 
	def init(self, args) :
		self.size = args.size;
		self.gui = args.gui;
		self.verbose = args.verbose;
		self.filter = args.filter;
		if( args.save != "" ) :
			self.save_file = args.save;
		else 
			self.save_file = "output.png";
		
		if( args.nb_sample != 0 ) :
			self.nb_sample = args.nb_sample;
		else 
			self.nb_sample = 100;

def main():
	#command-line parser 
	parser = argparse.ArgumentParser();

	parser.add_argument("-s", "--size", type=int, help="size the edge of the final image", required=True );
	parser.add_argument("-g", "--gui", help="graphical user interface result of the image", action="store_true");

	parser.add_argument("-ns", "--nb_sample", type=int, help="number of sample by pixel, default 100");
	
	parser.add_argument("-v", "--verbose", help="print all the inner messages of the processing", action="store_true");
	parser.add_argument("-f", "--filter", type=str, help="filter type applied on the final image");

	parser.add_argument("--save", type=str, help="file name to which save the resulting image" );
	
	#parser.add_argument("-d", "--dan", type=str, help="uses dan's microcontrolleur interface", action="store_true");

	args = parser.parse_args();

	config = Config( args )

	serial = Serial_COM();
	serial.init();
	serial.scan_size( args.size );

	arr = np.empty( (args.size, args.size) );
	
	for i in xrange(0, args.size) : 
		for j in xrange(0, args.size) : 
			res = serial.read();
			arr[i, j] = res;

	createmap( arr, args.save );



if(__name__ == "__main__"  ) :
	main()

