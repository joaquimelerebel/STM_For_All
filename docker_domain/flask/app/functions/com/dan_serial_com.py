#!/bin/env python3

import serial as serialLib
import subprocess
import cmd_int as cmd

# inspiration of Dan Berard serial communication protocol 
# used to communicate with a teesee through serial communication

class Serial_COM:
    def __init__(self, path_to_device): 
        try:
            self.serial = serialLib.Serial(subprocess_return, 115200)
        except Exception as e :
            raise RuntimeError("could not connect to : {path_to_device}");

        serial_init();

    def serial_init(self):
        cmd.print_verbose_WHITE(config, "[out] SERIAL ENABLED")
        self.serial.write(b"SE")

    def serial_disable(self):
        cmd.print_verbose_WHITE(config, "[out] SERIAL DISABLED")
        self.serial.write(b"SD")

    # Scan size in LSBs
    def scan_size(self, scan_size):
        cmd.print_verbose_WHITE(config, "[out] SCAN-SIZE : " + str(scan_size))
        self.serial.write(b"SS" + scan_size)

    # Image pixels
    def img_pixel(self, image_pix):
        cmd.print_verbose_WHITE(
            config, "[out] IMAGE-PIXEL : " + str(image_pix))
        self.serial.write(b"IP" + image_pix)

    # Line rate in Hz
    def line_rate(self, freq):
        cmd.print_verbose_WHITE(config, "[out] FREQ : " + str(freq*100))
        self.serial.write(b"LR" + str(freq*100))

    def x_offset(self, x_off):
        cmd.print_verbose_WHITE(config, "[out] X-OFFSET : " + str(x_off))
        self.serial.write(b"XO" + x_off)

    def y_offset(self, y_off):
        cmd.print_verbose_WHITE(config, "[out] Y-OFFSET : " + str(y_off))
        self.serial.write(b"YO" + y_off)

    # Setpoint in LSBs
    def set_point(self, set_point):
        cmd.print_verbose_WHITE(config, "[out] SET_POINT : " + str(set_point))
        self.serial.write(b"SP" + struct.pack(">", set_point))

    # Sample bias in LSBs
    def sample_bias(self, sample_bias):
        cmd.print_verbose_WHITE(
            config, "[out] SAMPLE_BIAS : " + str(sample_bias))
        self.serial.write(b"SB" + struct.pack(">", sample_bias))

    def setKPGain(self, kp):
        cmd.print_verbose_WHITE(config, "[out] KP : " + str(kp))
        self.serial.write(b"KP" + kp)

    def setKIGain(self, ki):
        cmd.print_verbose_WHITE(config, "[out] KI : " + str(ki))
        self.serial.write(b"KI" + ki)

    def enable_scanning(self):
        cmd.print_verbose_WHITE(config, "[out] ENABLE SCAN")
        self.serial.write(b"EN")

    def disable_scanning(self):
        cmd.print_verbose_WHITE(config, "[out] DISABLE SCAN")
        self.serial.write(b"DL")

    def engage_tip(self):
        cmd.print_verbose_WHITE(config, "[out] ENGAGE TIP")
        self.serial.write(b"TE")

    def retract_tip(self):
        cmd.print_verbose_WHITE(config, "[out] RETRACT TIP")
        self.serial.write(b"TR")

    def read_until_DATA(self):
        stri = ""
        while True:
            stri = str(self.serial.read(4))
            if stri == "DATA":
                break
            time.sleep(1)
        # verify that stri is 
        stri = self.serial.read(3);
        inte = int(stri)
        cmd.print_verbose_WHITE(config, "[in] DATA : " + str(inte))
        return inte
