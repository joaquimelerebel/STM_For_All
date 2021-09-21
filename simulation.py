import sys
import random 

from math import exp
from PIL import Image
from numpy import asarray



#get pixel value of each pixel of the picture

# file format : 
# [ width, height ]
# x1y1, x2y1, ... xwidthy1
# x1y2, x2y2, ... xwidthy2
# .
# .
# .
# x1yheight, x2yheight, ... xwidthyheight

def sim_image( image_filename : str, 
				output_filename : str, 
				error : float, 
				is_expodential_scale : bool) : 
	# error = float(error);
	try : 
		error = float(error);
	except ValueError :
		return;
	else :

		image = Image.open( image_filename ).convert('LA');
		width, height = image.size;
		px = image.load();
		data = asarray(image)

	# print in the chosen file
		if( isinstance(output_filename, str) ) :
			f = open(output_filename, "w")
		else :
			f = sys.stdout;

		f.write( "[ " + str( width ) + ", " + str( height )  + " ]\n" );

		# float error = error;

		for h in range(1, height): 
				for w in range( 1, width ) :
						#  convert point to 0-5V range
						if( is_expodential_scale ) :
							d =	(exp( data[w, h][0] ) *5)/ 5.5602316477276757e+110;
						else : 
							d = data[w, h][0]*0.01960784313;
						#randomisation
						d = ( d + random.uniform(0-error/2, error/2) ) % 5;
						if( w == width-1 ) :
							f.write( str( d ) + '\n' );
						else :
							f.write( str( d ) + ", " );

		if( isinstance(output_filename, str) ) :
			f.close()