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
    
    parser.add_argument( "-ot", "--output_type",
            dest="output_type", type=str,
            default="ASCII", 
            choices=["ASCII", "BIN_NP", "BIN_MST", "C_TABLE"],
            help="outputs type for the file format (ASCII, BIN_NP, BIN_MST, C_TABLE)" );
    
    parser.add_argument("-errM", "--error_mean", 
            default=0, type=float, 
            metavar="ERROR_MEAN", 
            help="mean of the error(default : 0)" );

    parser.add_argument("-err", "--error", 
            default=0, type=float, 
            metavar="ERROR", 
            help="maximum/standard error depending on the error model (default : 0)" );
    
    parser.add_argument("-errtype", "--error_type",  
            type=str,
            metavar="ERROR_TYPE",
            default="uniform",
            choices=["normal", "uniform"],
            help="""the error type can be : \"normal\"
            (ERROR is the standard deviation of the
            distribution and the mean is 0) or can be
            \"uniform\" (ERROR is the maximum error, default) Be careful, the error is applied before the uniform or exponential transformation to voltage""" );

    parser.add_argument("-exp", "--exponential", 
            action="store_true",
            default=False,
            help="scale the sim output exponentialy" );

    
    parser.add_argument("-vt", "--variation_time", 
            dest="vtime",
            default=0, type=float, 
            metavar="VTIME", 
            help="variation in time between each sample outputed to the file or CLI(default : 0) in ms" );
    
    parser.add_argument("-t", "--time", 
            dest="time",
            default=0, type=float, 
            metavar="TIME", 
            help="time between each sample outputed to the file or CLI(default : 0) in ms" );

    parser.add_argument("-stat", "--statisics",
                        default=False, action="store_true",
                        help="give statistical overview of the input image and the output")

    parser.add_argument("-s", "--size", 
            type=int, help="size of an edge of the square image");


    parser.add_argument("-o", "--save",
                        type=str,
                        default="",
                        metavar="PATH", help="output filepath")

    parser.add_argument("-serial",
                        metavar="PATH",
                        type=str,
                        default="",
                        help="should use the serial output PATH")

    # parser.add_argument("-d", "--dan", type=str, help="uses dan's microcontrolleur interface", action="store_true");

    args = parser.parse_args()

    config = conf.Config(args)
    simulation.sim_image(config)

if( __name__ == "__main__"  ) :
    main()
