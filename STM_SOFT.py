#!/bin/env python3


import argparse 
from serial_com import Serial_COM 
import numpy as np
import createmap
import cmd_int as cmd
import simulation


#setting up the default config
class Config : 
	def __init__(self, args) :
		self.size = args.size;
		self.gui = args.gui;
		self.verbose = args.verbose;
		self.filter = args.filter;
		self.simulation = args.simulator;
		self.is_expodential = args.expodential;
		
		self.is_normal_error = args.normal_error;
		if args.normal_error is None  : 
			self.is_normal_error = 0;

		self.error = args.error;
	
		if( args.save != "" ) :
			self.save_file = args.save;
		else :
			self.save_file = "";
		#else :
			# self.save_file = "OutputFiles/output.png";
		
		if( args.kp != 0 ) :
			self.kp = args.kp;
		else :
			self.kp = 1;

		if( args.ki != 0 ) :
			self.ki = args.ki;
		else :
			self.ki = 1;

		if( args.frequence != 0 ) :
			self.frequence = args.frequence;
		else :
			self.frequence = 100;
		

#performs different tests
class Tests : 
	def __init__(self, config) :
		self.config = config;

	def scan( self ) :
		if( len( self.config.simulation ) > 0 ) :
			simulation.sim_image( self.config.simulation, 
				self.config.save_file, self.config.error, 
				self.config.is_expodential, self.config.is_normal_error );
			exit();


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

def main():
	#command-line parser 
	parser = argparse.ArgumentParser();

	parser.add_argument("-sim", "--simulator", type=str, help="simulates from the filename" );
	parser.add_argument("-err", "--error", type=float, help="amount of sim maximum error or standard error depending on the error model (default : 0)" );
	parser.add_argument("-err_norm", "--normal_error", action="store_true", help="the error is distributed normally" );
	parser.add_argument("-exp", "--expodential", action="store_true", help="does scale the sim output expodentialy" );
	

	parser.add_argument("-s", "--size", type=int, help="size the edge of the final image", required=True );
	parser.add_argument("-g", "--gui", help="graphical user interface result of the image", action="store_true");

	parser.add_argument("-kp", type=int, help="PID KP constant (default 1)");
	parser.add_argument("-ki", type=int, help="PID KI constant (default 1)");
	parser.add_argument("-fr", "--frequence", type=int, help="line rate in Hz (default 100Hz)");
	
	
	parser.add_argument("-v", "--verbose", action="store_true", help="print all the inner messages of the processing");
	parser.add_argument("-f", "--filter", type=str, help="filter type applied on the final image");

	parser.add_argument("--save", type=str, help="file name to which save the resulting image" );
	
	#parser.add_argument("-d", "--dan", type=str, help="uses dan's microcontrolleur interface", action="store_true");

	args = parser.parse_args();

	config = Config( args );
	tests = Tests( config );
	tests.scan();

	



if(__name__ == "__main__"  ) :
	main()

