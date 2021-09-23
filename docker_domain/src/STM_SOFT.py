#!/bin/env python3

import sys
import argparse 
from serial_com import Serial_COM 
import numpy as np
import createmap
import cmd_int as cmd
import simulation
import config as conf

#performs different tests
class Tests : 
	def __init__(self, config : conf.Config) :
		self.config = config;

	def scan( self ) :
		if( len( self.config.simulation_filename ) > 0 ) :
			simulation.sim_image( self.config );
			exit();

		# will uncomment when the app will need something 
		# else than a simulator
		"""
		serial = Serial_COM( self.config );
		serial.init();
		serial.kp( self.config.kp );
		serial.ki( self.config.ki );
		serial.line_rate( self.config.freq );

		serial.scan_size( self.config.size );

		arr = np.empty( (self.config.size , self.config.size ) );
		
		for i in xrange( 0, self.config.size ) : 
			for j in xrange( 0, self.config.size ) : 
				res = serial.read();
				arr[i, j] = res;

		createmap( arr, self.config );
		"""
def main():

	if len( sys.argv ) <= 1 :
		print("\33[0;31mNot enough arguments\33[0m");
		exit();
	

	#command-line parser 
	parser = argparse.ArgumentParser();

	parser.add_argument("-sim", "--simulator", 
		default="", type=str,
		metavar="filename", 
		help="simulates from the filename" );

	parser.add_argument("-err", "--error", 
		default=0, type=float, 
		metavar="ERROR", 
		help="amount of sim maximum error or standard error depending on the error model (default : 0)" );
	parser.add_argument("-err_norm", "--normal_error", 
		action="store_true", 
		help="the error is distributed normally" );
	parser.add_argument("-exp", "--expodential", 
		action="store_true", 
		help="does scale the sim output expodentialy" );
	

	parser.add_argument("-s", "--size", 
		type=int, help="size of an edge of the square image");
	parser.add_argument("-g", "--gui", 
		help="graphical user interface result of the image", action="store_true");

	parser.add_argument("-kp", type=int, help="PID KP constant (default 1)");
	parser.add_argument("-ki", type=int, help="PID KI constant (default 1)");
	parser.add_argument("-fr", "--frequence", type=int, help="line rate in Hz (default 100Hz)");
	
	
	parser.add_argument("-v", "--verbose", action="store_true", help="print all the inner messages of the processing");
	parser.add_argument("-f", "--filter", type=str, help="filter type applied on the final image");

	parser.add_argument("-o", "--save", 
		type=str, 
		metavar="filename", help="output filename" );
	
	#parser.add_argument("-d", "--dan", type=str, help="uses dan's microcontrolleur interface", action="store_true");

	args = parser.parse_args();

	config = conf.Config( args );
	tests = Tests( config );
	tests.scan();
	



if( __name__ == "__main__"  ) :
	main()

