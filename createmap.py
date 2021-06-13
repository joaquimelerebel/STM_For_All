#!/bin/env python3 

import numpy as np
from PIL import Image



def createImage( array ) :
	img = Image.fromarray(array);
	#img.save('my.png');
	img.show();