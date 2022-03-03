#!/bin/env python3

import sys
import argparse
import numpy as np
import createmap
import cmd_int as cmd
import interaction
import config as conf 

def main():

    if len(sys.argv) <= 1:
        print("\33[0;31mNot enough arguments\33[0m")
        exit()

    # command-line parser
    parser = argparse.ArgumentParser()


    parser.add_argument("-t", "--type", choices=["SIMPLE"],
                        dest="test_type", type=str, default="SIMPLE",
                        help="SIMPLE test will just launch a test and then read until the end of the line")
    
    parser.add_argument("-ts", "--timestamp", action="store_true",
                        dest="ts", default=False,
                        help="set a timestamps before each output")
    
    parser.add_argument("-d", "--device", dest="device", type=str, default="/dev/ttyACM0",
                        help="device used for the communication, default, /dev/ttyACM0")
    
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print all the inner messages of the processing")

    parser.add_argument("-o", "--save",
                        type=str,
                        metavar="filename", help="output filename")

    #parser.add_argument("-d", "--dan", type=str, help="uses dan's microcontrolleur interface", action="store_true");

    args = parser.parse_args()

    config = conf.Config(args)
    interaction.test(config);


if(__name__ == "__main__"):
    main()
