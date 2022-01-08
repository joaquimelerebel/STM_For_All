import sys
import config as conf
import cmd_int as cmd

from math import exp
from PIL import Image
from numpy import asarray
from numpy import random


#get pixel value of each pixel of the picture

# file format : 
# [ width, height ]
# x1y1, x2y1, ... xwidthy1
# x1y2, x2y2, ... xwidthy2
# .
# .
# .
# x1yheight, x2yheight, ... xwidthyheight

def sim_image( config : conf.Config ) : 
	#check for wrong inputs
	try : 
		if( config.is_normal_error ) : 
			cmd.eprint_RED( "Not implemented yet" );
			exit();
	except ValueError :
		return;
	else :

		image = Image.open( config.simulation_filename ).convert('LA');
		width, height = image.size;
		px = image.load();
		data = asarray( image );

	# print in the chosen file (stdout or a file)
		if( isinstance( config.output_filename, str) ) :
			f = open( config.output_filename, "w")
		else :
			f = sys.stdout;

		f.write( "[ " + str( width ) + ", " + str( height )  + " ]\n" );

		#create the map of 
		for h in range( 0, height ): 
				for w in range( 0, width ) :
						
						#  convert point to 0-5V range
						if( config.is_expodential_scale ) :
							d =	(exp( data[w, h][0] ) *5)/ 5.5602316477276757e+110;
						else : 
							d = data[w, h][0]*0.01960784313;
						
						#error generation
						if( config.is_normal_error ) :
							d = d + random.normal( 0, config.error );
						else :
							d = ( d + random.uniform( 0-config.error/2, config.error/2 ) ) % 5;
						
						# applying filters
						if  d > 5 : 
							d = 5;
						if d < 0 :
							d = 0;

						if( w == width-1 ) :
							f.write( str( d ) + '\n' );
						else :
							f.write( str( d ) + ", " );

		if( isinstance(config.output_filename, str) ) :
			f.close()