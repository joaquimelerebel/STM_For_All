#!/bin/env python3 

import argparse 
import serial_com
import numpy as np

class config : 
	def init(self, _resolution) :
		self.resolution = _resolution;


def main():
	#command-line parser 
	parser = argparse.ArgumentParser();

	parser.add_argument("-v", "--verbose", help="print all the inner messages of the processing", action="store_true");

	parser.add_argument("-s", "--size", type=int, help="size the edge of the final image", required=True );
	parser.add_argument("-f", "--filter", type=str, help="filter type applied on the final image");

	parser.add_argument("--save", type=str, help="file name to which save the resulting image" );
	
	#parser.add_argument("-d", "--dan", type=str, help="uses dan's microcontrolleur interface", action="store_true");

	parser.add_argument("-g", "--gui", type=str, help="graphical user interface result of the image", required=True );

	parser.parse_args();


	serial = Serial_COM();
	serial.scan_size( parser.size );
	serial.init();

	arr = np.empty( (parser.size, parser.size) );
	
	for i in xrange(0, parser.size) : 
		for j in xrange(0, parser.size) : 
			res = serial.read();
			arr[i, j] = res;

	createmap( arr );



if(__name__ == "__main__"  ) :
	main()

