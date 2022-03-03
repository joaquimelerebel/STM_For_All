#!/bin/env python3

import serial as serialLib
import subprocess
import cmd_int as cmd

class Serial_COM :
    def __init__(self, config):
        self.config = config
        # DEBUG verify the output of the shell command
        cmd.print_verbose_WHITE(config, "[process] Looking for device")
        try:
            self.serial = serialLib.Serial(config.device, 115200)
            cmd.print_GREEN(f"using : {config.device}" )
        except Exception as e:
            cmd.eprint_RED("software did not recognise the serial connection")
            exit()



    def serial_init(self):
        cmd.print_verbose_WHITE(self.config, "[out] SERIAL ENABLED")
        self.serial.write(b"SE")

    def serial_disable(self):
        cmd.print_verbose_WHITE(self.config, "[out] SERIAL DISABLED")
        self.serial.write(b"SD")

    # Scan size in LSBs
    def scan_size(self, scan_size):
        cmd.print_verbose_WHITE(config, "[out] SCAN-SIZE : " + str(scan_size))
        self.serial.write("SS" + scan_size)

    # Image pixels
    def img_pixel(self, image_pix):
        cmd.print_verbose_WHITE(
            config, "[out] IMAGE-PIXEL : " + str(image_pix))
        self.serial.write(b"IP" + image_pix)

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

    def read_until_code(self):
        stri = "";
        cmd=["SE"];
        while True:
            stri = str(self.serial.read(2))
            if stri in cmd :
                break
            time.sleep(1)
        # verify that stri is byte
        inte = int(stri)
        cmd.print_verbose_WHITE(config, "[in] DATA : " + str(inte))

    def read_until_DATA(self, length=16386):
        stri = ""
        while True:
            stri = str(self.serial.read(4))
            if stri == "DATA":
                break
            time.sleep(1)
        # verify that stri is byte
        stri = self.serial.read(length)
        inte = int(stri)
        cmd.print_verbose_WHITE(config, "[in] DATA : " + str(inte))
        return inte
