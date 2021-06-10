#!/bin/env python3 


import argparse 
import serial

class config : 
	def init(self, _resolution) :
		self.resolution = _resolution;


def main():
	#command-line parser 
	parser = argparse.ArgumentParser()

	parser.add_argument("-v", "--verbose", help="print all the inner messages of the processing", action="store_true")

	parser.add_argument("-r", "--resolution", type=int, help="resolution of the final image")
	parser.add_argument("-f", "--filter", type=str, help="filter type applied on the final image")

	parser.add_argument("-d", "--dan", type=str, help="uses dan's microcontrolleur interface", action="store_true")

	parser.add_argument("-g", "--gui", type=str, help="graphical user interface result of the image")

	parser.parse_args()


if(__name__ == "__main__"  ) :
	main()

