import sys
import os
import struct
from numpy import random, zeros, save
from time import sleep, time

import config as conf
import gen_var as gen


# packet communication of
# use of the Dan Berard pkt com protocol

class SerialWriter:
    def __init__(self, config: conf.Config):
        self.config = config
        self.isBin = False
        self.isTimed = False

        if( config.time != 0 or config.vtime != 0 ) :
            self.ltime=time()*1000;
            self.isTimed = True;
        if( config.is_bin ):
            self.isBin = True;

        try :
            self.f = serial.Serial( config.output_filename, gen.BAUD_RATE );
        except Exception as e :
            raise RuntimeError( f"dev : {config.output_filename} could not be open");

    def writeAll(self, arr):
        serial_disable;
        pass;

    def setWidthHeight(self, height, width):
        self.height = height
        self.width = width
        # ascii 
        if( not self.isBin ):
            out = ("[ " + str(height) + ", " + str(width) + " ]\n");
            self.cache += out;
        # binary output  
        elif( self.isBin ) :  
            # set the header up
            # file type identifier
            out = b"MST"
            # version control
            out += struct.pack(">h", VERSION)
            # patch control
            out += struct.pack(">h", PATCH)
            # length of each data point, in power of 2
            out += struct.pack(">B", LEN)
            # height
            out += struct.pack(">i", self.height)
            # width
            out += struct.pack(">i", self.width)
            # metadata(16 bytes)
            for i in range(0, 16):
                out += struct.pack(">b", 0x69);

            self.f.write(out);


    def writePoint(self, h, w, point, isStop) :
        if( self.isTimed ) :
            # wait time calculation and wait
            deltaT = (time()*1000) - self.ltime
            self.wtime = float(random.uniform(0-(self.config.vtime/2), self.config.vtime/2) + self.config.time - deltaT)/1000.0;
            if self.wtime > 0 :
                sleep( self.wtime );
            ctime = time()*1000;
            deltaT = ctime - self.ltime;
            self.ltime = time()*1000;


        # for binary points 
        if( self.isBin ) : 
            b_h = struct.pack(">i", h)
            b_w = struct.pack(">i", w)

            b_point = struct.pack(">d", point)
            self.f.write(b_point);

        if( self.isTimed ):
            return deltaT
        else :
            return 0;


    def serial_init(self):
        cmd.print_verbose_WHITE(config, "[out] SERIAL ENABLED")
        self.serial.write("SE")

    def serial_disable(self):
        cmd.print_verbose_WHITE(config, "[out] SERIAL DISABLED")
        self.serial.write("SD")

    # Scan size in LSBs
    def scan_size(self, scan_size):
        cmd.print_verbose_WHITE(config, "[out] SCAN-SIZE : " + str(scan_size))
        self.serial.write("SS" + scan_size)

    # Image pixels
    def img_pixel(self, image_pix):
        cmd.print_verbose_WHITE(
            config, "[out] IMAGE-PIXEL : " + str(image_pix))
        self.serial.write("IP" + image_pix)

    # Line rate in Hz
    def line_rate(self, freq):
        cmd.print_verbose_WHITE(config, "[out] FREQ : " + str(freq*100))
        self.serial.write("LR" + str(freq*100))

    def x_offset(self, x_off):
        cmd.print_verbose_WHITE(config, "[out] X-OFFSET : " + str(x_off))
        self.serial.write("XO" + x_off)

    def y_offset(self, y_off):
        cmd.print_verbose_WHITE(config, "[out] Y-OFFSET : " + str(y_off))
        self.serial.write("YO" + y_off)

    # Setpoint in LSBs
    def set_point(self, set_point):
        cmd.print_verbose_WHITE(config, "[out] SET_POINT : " + str(set_point))
        self.serial.write("SP" + set_point)

    # Sample bias in LSBs
    def sample_bias(self, sample_bias):
        cmd.print_verbose_WHITE(
            config, "[out] SAMPLE_BIAS : " + str(sample_bias))
        self.serial.write("SB" + sample_bias)

    def PID_KPGain(self, kp):
        cmd.print_verbose_WHITE(config, "[out] KP : " + str(kp))
        self.serial.write("KP" + kp)

    def PID_KIGain(self, ki):
        cmd.print_verbose_WHITE(config, "[out] KI : " + str(ki))
        self.serial.write("KI" + ki)

    def enable_scanning(self):
        cmd.print_verbose_WHITE(config, "[out] ENABLE SCAN")
        self.serial.write("EN")

    def disable_scanning(self):
        cmd.print_verbose_WHITE(config, "[out] DISABLE SCAN")
        self.serial.write("DL")

    def engage_tip(self):
        cmd.print_verbose_WHITE(config, "[out] ENGAGE TIP")
        self.serial.write("TE")

    def retract_tip(self):
        cmd.print_verbose_WHITE(config, "[out] RETRACT TIP")
        self.serial.write("TR")

    def read_until_DATA(self):
        stri = ""
        while True:
            stri = str(self.serial.read(4))
            if stri == "DATA":
                break
            time.sleep(1)
        # verify that stri is byte
        stri = self.serial.read(2)
        inte = int(stri)
        cmd.print_verbose_WHITE(config, "[in] DATA : " + str(inte))
        return inte


