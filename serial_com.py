#!/bin/env python 

from serial import Serial
import serial as serialLib
import subprocess
import cmd_int as cmd

class Serial_COM : 
	def __init__(self):
		#DEBUG verify the output of the shell command
		subp = subprocess.Popen("ls /dev/tty* | grep usb", shell=True, stdout=subprocess.PIPE)
		subprocess_return = subp.stdout.read();
		try:
			self.serial = serialLib.Serial(subprocess_return, 115200);
		except Exception as e:
			cmd.eprint_RED("software did not recognise the serial connection");
			exit();
		
		print("using : %s" % serial.name );

	
	def serial_init(self) :
		self.serial.write("SE");

	def serial_disable(self) :
		self.serial.write("SD");

	# Scan size in LSBs
	def scan_size(self, scan_size ) : 
		print( scan_size );
		self.serial.write("SS" + scan_size );
	
	# Image pixels
	def img_pixel( self, image_pix ) : 
		self.serial.write("IP" + image_pix );
	
	# Line rate in Hz
	def line_rate( self, freq ) : 
		self.serial.write("IP" + image_pix );

	def x_offset( self, x_off ) : 
		self.serial.write("XO" + x_off );

	def y_offset( self, y_off ) : 
		self.serial.write("YO" + y_off );
	
	# Setpoint in LSBs
	def set_point( self, set_point ) : 
		self.serial.write("SP" + set_point );

	#Sample bias in LSBs
	def sample_bias( self, sample_bias ) : 
		self.serial.write("SB" + sample_bias );
	
	def PID_KPGain( self, kp ) : 
		self.serial.write("KP" + kp );

	def PID_KIGain( self, ki ) : 
		self.serial.write("KI" + ki );
	
	def enable_scanning(self) :
		self.serial.write("EN");

	def disable_scanning(self) :
		self.serial.write("DL");

	def engage_tip(self) :
		self.serial.write("TE");

	def retract_tip(self) :
		self.serial.write("TR");

	def read_until_DATA(self) :
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