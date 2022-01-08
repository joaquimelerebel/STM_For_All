#!/bin/env python

import numpy as np
from PIL import Image


def createImage( array, save ) :
	img = Image.fromarray( array );
	if( save != "" ) : 
		img.save( save );
	img.show();