#!/bin/env python 

import argparse 
from serial_com import Serial_COM 
import numpy as np
import createmap

class config : 
	def init(self, _resolution) :
		self.resolution = _resolution;


def main():
	#command-line parser 
	parser = argparse.ArgumentParser();

	parser.add_argument("-s", "--size", type=int, help="size the edge of the final image", required=True );
	parser.add_argument("-g", "--gui", help="graphical user interface result of the image", action="store_true");

	parser.add_argument("-v", "--verbose", help="print all the inner messages of the processing", action="store_true");
	parser.add_argument("-f", "--filter", type=str, help="filter type applied on the final image");

	parser.add_argument("--save", type=str, help="file name to which save the resulting image" );
	
	#parser.add_argument("-d", "--dan", type=str, help="uses dan's microcontrolleur interface", action="store_true");


	args = parser.parse_args();


	serial = Serial_COM();
	serial.scan_size( args.size );
	serial.init();

	arr = np.empty( (args.size, args.size) );
	
	for i in xrange(0, args.size) : 
		for j in xrange(0, args.size) : 
			res = serial.read();
			arr[i, j] = res;

	createmap( arr, args.save );



if(__name__ == "__main__"  ) :
	main()

