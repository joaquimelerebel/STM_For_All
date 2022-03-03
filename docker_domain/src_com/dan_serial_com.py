#!/bin/env python3

import serial as serialLib
import cmd_int as cmd
import time 
# inspiration of Dan Berard serial communication protocol 
# used to communicate with a teesee through serial communication

class Serial_COM:
    def __init__(self, config): 
        try:
            self.config = config
            self.serial = serialLib.Serial(config.device, 115200)
        except Exception as e :
            raise RuntimeError("could not connect to : {path_to_device}");

    def serial_init(self):
        cmd.print_verbose_WHITE(self.config, "[out] SERIAL ENABLED")
        self.serial.write(b"SE")
        self.read_until_cmd();

    def serial_disable(self):
        cmd.print_verbose_WHITE(self.config, "[out] SERIAL DISABLED")
        self.serial.write(b"SD")

    # Scan size in LSBs
    def scan_size(self, scan_size):
        cmd.print_verbose_WHITE(self.config, "[out] SCAN-SIZE : " + str(scan_size))
        self.serial.write(b"SS" + scan_size)

    # Image pixels
    def img_pixel(self, image_pix):
        cmd.print_verbose_WHITE(
            self.config, "[out] IMAGE-PIXEL : " + str(image_pix))
        self.serial.write(b"IP" + image_pix)

    # Line rate in Hz
    def line_rate(self, freq):
        cmd.print_verbose_WHITE(self.config, "[out] FREQ : " + str(freq*100))
        self.serial.write(b"LR" + str(freq*100))

    def x_offset(self, x_off):
        cmd.print_verbose_WHITE(self.config, "[out] X-OFFSET : " + str(x_off))
        self.serial.write(b"XO" + x_off)

    def y_offset(self, y_off):
        cmd.print_verbose_WHITE(self.config, "[out] Y-OFFSET : " + str(y_off))
        self.serial.write(b"YO" + y_off)

    # Setpoint in LSBs
    def set_point(self, set_point):
        cmd.print_verbose_WHITE(self.config, "[out] SET_POINT : " + str(set_point))
        self.serial.write(b"SP" + struct.pack(">", set_point))

    # Sample bias in LSBs
    def sample_bias(self, sample_bias):
        cmd.print_verbose_WHITE(
            self.config, "[out] SAMPLE_BIAS : " + str(sample_bias))
        self.serial.write(b"SB" + struct.pack(">", sample_bias))

    def setKPGain(self, kp):
        cmd.print_verbose_WHITE(self.config, "[out] KP : " + str(kp))
        self.serial.write(b"KP" + kp)

    def setKIGain(self, ki):
        cmd.print_verbose_WHITE(self.config, "[out] KI : " + str(ki))
        self.serial.write(b"KI" + ki)

    def enable_scanning(self):
        cmd.print_verbose_WHITE(self.config, "[out] ENABLE SCAN")
        self.serial.write(b"EN")

    def disable_scanning(self):
        cmd.print_verbose_WHITE(self.config, "[out] DISABLE SCAN")
        self.serial.write(b"DL")

    def engage_tip(self):
        cmd.print_verbose_WHITE(self.config, "[out] ENGAGE TIP")
        self.serial.write(b"TE")

    def retract_tip(self):
        cmd.print_verbose_WHITE(self.config, "[out] RETRACT TIP")
        self.serial.write(b"TR")


    def read_until_cmd(self):
        stri = b""
        cmdlist=[b"SE"]
        while True:
            stri = self.serial.read(2)
            if stri in cmdlist:
                break
            time.sleep(1)
        cmd.print_verbose_WHITE(self.config, "[in] " + str(stri))


    def read_until_DATA(self, length=16386):
        stri = b""
        while True:
            stri += self.serial.read(4)
            cmd.print_verbose_WHITE(self.config, "[inDBG] " + str(stri) )
            if b"DATA" in stri:
                break
            time.sleep(1)
        # verify that stri is 
        cmd.print_verbose_WHITE(self.config, "[in] --- reading DATA ----" )
        stri = self.serial.read(length);
        #inte = int(stri)
        cmd.print_verbose_WHITE(self.config, "[in] DATA : " + str(inte))
        return inte
