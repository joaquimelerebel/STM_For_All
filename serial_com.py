#!/bin/env python3 

import serial as serialLib

class Serial_COM : 
	def init(self):
		#DEBUG verify the output of the shell command
		subprocess = subprocess.Popen("ls /dev/tty.* | grep usb", shell=True, stdout=subprocess.PIPE)
		subprocess_return = subprocess.stdout.read()

		self.serial = serialLib.Serial(subprocess_return);

		self.serial.baudrate = 115200;
		
		print("using : %s" % serial.name );

	
	def serial_init() :
		self.serial.write("SE");

	def serial_disable() :
		self.serial.write("SD");

	# Scan size in LSBs
	def scan_size( scan_size ) : 
		self.serial.write("SS" + scan_size );
	
	# Image pixels
	def img_pixel( image_pix ) : 
		self.serial.write("IP" + image_pix );
	
	# Line rate in Hz
	def line_rate( freq ) : 
		self.serial.write("IP" + image_pix );

	def x_offset( x_off ) : 
		self.serial.write("XO" + x_off );

	def y_offset( y_off ) : 
		self.serial.write("YO" + y_off );
	
	# Setpoint in LSBs
	def set_point( set_point ) : 
		self.serial.write("SP" + set_point );

	#Sample bias in LSBs
	def sample_bias( sample_bias ) : 
		self.serial.write("SB" + sample_bias );
	
	def PID_KPGain( kp ) : 
		self.serial.write("KP" + kp );

	def PID_KIGain( ki ) : 
		self.serial.write("KI" + ki );
	
	def enable_scanning() :
		self.serial.write("EN");

	def disable_scanning() :
		self.serial.write("DL");

	def engage_tip() :
		self.serial.write("TE");

	def retract_tip() :
		self.serial.write("TR");

	def read_until_DATA() :
		stri = "";
		while True : 
			stri = str(self.serial.read(4));
			if stri == "DATA" :
				break;
			time.sleep(1);
		#verify that stri is byte
		stri = self.serial.read(2);
		inte = int( stri );
		return inte;