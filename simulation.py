import sys

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

def sim_image( image_filename, output_filename ) : 
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

	for h in range(1, height): 
			for w in range( 1, width ) :
					if( w == width-1 ) :
						f.write( str( data[w, h][0] ) + '\n' );
					else :
						f.write( str( data[w, h][0] ) + ", " );

	if( isinstance(output_filename, str) ) :
		f.close()