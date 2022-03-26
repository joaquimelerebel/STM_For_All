import sys
import os
import struct
from math import exp, log
from PIL import Image
from numpy import asarray, random, std, zeros, save, uint8
from time import sleep, time
from json import dumps

import config as conf
import filewriter as fwc
import serialwriter as swc

VERSION = 0
PATCH = 1
LEN = 6

def sim_image(config: conf.Config):
    image = Image.open(config.simulation_filename).convert('L')
    width, height = image.size
    data = asarray(image)

    if( not config.isSerial ) :
        fw = fwc.FileWriter(config);
    else :
        fw = swc.SerialWriter(config);
    fw.setWidthHeight(height, width)

    # allocation of the output array of voltages
    data_voltages = zeros((height, width))
    dataSet = zeros((height, width)) 
    tpoints = zeros((height, width))

    if( config.time != 0 or config.vtime != 0 ) :
        isTimed = True;
    else :
        isTimed = False;
    # create the map of voltages
    for h in range(0, height):
        for w in range(0, width):

            # error generation
            if (config.is_normal_error) :
                dataSet[h, w] = data[h, w] + random.normal(config.error_mean, config.error)
            elif(config.is_uniform_error) :
                dataSet[h, w] = data[h, w] + random.uniform(0-(config.error/2), config.error/2) + config.error_mean
            else :
                dataSet[h, w] = data[h, w]

            #  convert point to 0-5V range
            if(config.is_exponential_scale):
                data_voltage = (exp(dataSet[h, w]) * 5) / 5.5602316477276757e+110
            # elif( config.is_complexe_exponential_scale ) :
            #    pass;
                # J_T prop exp(-A\Phi^{1/2}s)
                # A=sqrt((4*\pi/h)*2m)=1.025 Ang^-1 eV^-(1/2)
                # m = mass of the free electron
                # cf surface studies by scanning tunneling mircroscopy 1982 G. Binning, H. Rohrer
                # trying to convert with realistic values

                # if constant tunneling current :
                # \Phi^(1/2)s=const
                # Pz is the index of the displacement : potential at the piezo borders
            else:
                data_voltage = (dataSet[h, w]*5)/255

            # applying borders
            #if data_voltage > 5:
             #   data_voltage = 5
            #if data_voltage < 0:
             #   data_voltage = 0

            data_voltages[h, w] = data_voltage

            # printing result
            if(w == width-1):
                tpoints[h, w] = fw.writePoint(h, w, data_voltage, True)
            else:
                tpoints[h,w] = fw.writePoint(h, w, data_voltage, False)

    fw.writeAll(data_voltages)

    if(config.is_statistical):
        # creation of the image statistics
        dataflatten = data.flatten()
        maxImage = float(max(dataflatten))
        minImage = float(min(dataflatten))
        meanImage = float(sum(dataflatten)/len(dataflatten))
        stdevImage = float(std(dataflatten))
        statistics_set = {"Image": {
            "max": maxImage, "min": minImage, "mean": meanImage, "stdev": stdevImage}}
        
        # creation of the image stats with error statistics
        dataflatten = dataSet.flatten()
        maxWith_error = float(max(dataflatten))
        minWith_error = float(min(dataflatten))
        meanWith_error = float(sum(dataflatten)/len(dataflatten))
        stdevWith_error = float(std(dataflatten))
        statistics_set["ImageWithError"] = {
            "max": maxWith_error, "min": minWith_error, "mean": meanWith_error, "stdev": stdevWith_error}

        # creation of the output statistics
        data_voltages_flatten = data_voltages.flatten()
        maxVolt = float(max(data_voltages_flatten))
        minVolt = float(min(data_voltages_flatten))
        meanVolt = float(sum(data_voltages_flatten)/len(data_voltages_flatten))
        stdevVolt = float(std(data_voltages_flatten))
        statistics_set["Voltages"] = {
            "max": maxVolt, "min": minVolt, "mean": meanVolt, "stdev": stdevVolt}
        
        #timing data
        if( isTimed ):
            dataflatten = tpoints.flatten()
            maxWith_error = float(max(dataflatten))
            minWith_error = float(min(dataflatten))
            meanWith_error = float(sum(dataflatten)/len(dataflatten))
            stdevWith_error = float(std(dataflatten))
            statistics_set["TimeMS"] = {
                "max": maxWith_error, "min": minWith_error, "mean": meanWith_error, "stdev": stdevWith_error}

        json_object = dumps(statistics_set, indent = 4) 
        print(json_object)
