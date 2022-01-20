import sys
import config as conf
import cmd_int as cmd

from math import exp, log
from PIL import Image
from numpy import asarray, random, std, zeros


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
        pass
    except ValueError :
        return;
    else :

        image = Image.open( config.simulation_filename ).convert('L');
        width, height = image.size;
        data = asarray( image );

    # print in the chosen file (stdout or a file)
        if( isinstance( config.output_filename, str) ) :
            f = open( config.output_filename, "w")
        else :
            f = sys.stdout;

        f.write( "[ " + str( width ) + ", " + str( height )  + " ]\n" );

        # creation of the image statistics
        if( config.is_statistical ) : 
            dataflatten = data.flatten();
            maxImage = max(dataflatten);
            minImage = min(dataflatten);
            meanImage = sum(dataflatten)/len(dataflatten);
            stdevImage = std(dataflatten);
            statistics_set = {"Image" : {"max" : maxImage, "min" : minImage, "mean" : meanImage, "stdev" : stdevImage}};
        
        #allocation of the output array of voltages
        data_voltages = zeros((height, width));

        #create the map of voltages
        for h in range( 0, height ): 
            for w in range( 0, width ) :

                #error generation
                if( config.is_normal_error ) :
                    data_with_error = data[w, h] + random.normal( 0, config.error );
                elif( config.is_uniform_error ) :
                    data_with_error = data[w, h] + random.uniform( 0-(config.error/2), config.error/2 );
                else : 
                    data_with_error = data[w, h];

                #  convert point to 0-5V range
                if( config.is_expodential_scale ) :
                    data_voltage =	(exp( data_with_error ) *5)/ 5.5602316477276757e+110;
                else : 
                    data_voltage = (data_with_error*5)/255;


                # applying filters
                if  data_voltage > 5 : 
                    data_voltage = 5;
                if data_voltage < 0 :
                    data_voltage = 0;

                data_voltages[w, h] = data_voltage;

                # printing result
                if( w == width-1 ) :
                    f.write( str( data_voltage ) + '\n' );
                else :
                    f.write( str( data_voltage ) + ", " );

        if( isinstance(config.output_filename, str) ) :
            f.close()


        if( config.is_statistical ):

            # creation of the image with error statistics 
            dataflatten = data.flatten();
            maxWith_error = max(dataflatten);
            minWith_error = min(dataflatten);
            meanWith_error = sum(dataflatten)/len(dataflatten);
            stdevWith_error = std(dataflatten);
            statistics_set["ImageWithError"] = {"max" : maxWith_error, "min" : minWith_error, "mean" : meanWith_error, "stdev" : stdevWith_error};
            
            # creation of the output statistics
            data_voltages_flatten = data_voltages.flatten();
            maxVolt = max(data_voltages_flatten);
            minVolt = min(data_voltages_flatten);
            meanVolt = sum(data_voltages_flatten)/len(data_voltages_flatten);
            stdevVolt = std(data_voltages_flatten);
            statistics_set["Voltages"] = {"max" : maxVolt, "min" : minVolt, "mean" : meanVolt, "stdev" : stdevVolt};

            print(statistics_set)

            # output of the statistics
            print("-- image --");
            print("max : " + str(maxImage)); 
            print("min : " + str(minImage)); 
            print("mean : " + str(meanImage)); 
            print("st dev : " + str(stdevImage)); 

