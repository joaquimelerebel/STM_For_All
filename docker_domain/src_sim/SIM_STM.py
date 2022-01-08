#!/bin/env python3

import sys
import argparse 
import numpy as np
import createmap
import cmd_int as cmd
import simulation
import config as conf


def main():

	if len( sys.argv ) <= 1 :
		cmd.eprint_RED( "Not enough arguments" );
		exit();
	

	#command-line parser 
	parser = argparse.ArgumentParser();

	parser.add_argument( 
		default="", dest="simulation_filename", 
		type=str, 
		metavar="SIM_FILENAME", 
		help="simulates from this file" );

	parser.add_argument("-err", "--error", 
		default=0, type=float, 
		metavar="ERROR", 
		help="amount of sim maximum error or standard error depending on the error model (default : 0)" );
	parser.add_argument("-err_norm", "--normal_error", 
		action="store_true", 
		help="the error is distributed normally (err is the mean of the distribution)" );
	parser.add_argument("-exp", "--expodential", 
		action="store_true", 
		help="does scale the sim output expodentialy" );
	

	parser.add_argument("-s", "--size", 
		type=int, help="size of an edge of the square image");
	parser.add_argument("-g", "--gui", 
		help="graphical user interface result of the image", action="store_true");

	
	parser.add_argument("-v", "--verbose", action="store_true", help="print all the inner messages of the processing");

	parser.add_argument("-o", "--save", 
		type=str, 
		metavar="filename", help="output filename" );
	
	#parser.add_argument("-d", "--dan", type=str, help="uses dan's microcontrolleur interface", action="store_true");

	args = parser.parse_args();

	config = conf.Config( args );
	simulation.sim_image( config );
	



if( __name__ == "__main__"  ) :
	main()

