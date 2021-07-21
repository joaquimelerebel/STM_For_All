
from PIL import Image
from numpy import asarray

#get pixel value of each pixel of the picture

def sim_image( image_name ) : 
	image = Image.open( image_name );
	width, height = image.size;
	gray_image = ImageOps.grayscale( image )
	px = image.load();
	data = asarray(gray_image)
	for w in range(1, width): 
		for h in range( 1, height ) :
			print (gray_image[w, h]);
