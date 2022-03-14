import numpy as np
import threading

from functions.com.dan_serial_com import Serial_COM
import functions.com.cmd_int as cmd
import functions.com.timeout as tm


def ping_eff( systemConfig, devicePath ) :
    com_ser = Serial_COM( systemConfig, devicePath ); 
    com_ser.serial_init();
    com_ser.serial_disable();

def ping( systemConfig, devicePath ):
    try :
        cmd.log( systemConfig.logFilePath, "[COM] PING")
        tm.timeout( systemConfig.timeOutComTime, ping_eff,
                    (systemConfig, devicePath),
                    "pong did not come in time")
        if devicePath == "" :
            raise RuntimeException("no path to the device")
    except OSError as ex:
        cmd.eprint_RED(systemConfig.logFilePath, f"[ERROR COM] (not right device) {ex}")
        if systemConfig.debug :
            raise ex;
    except TimeoutError as ex:
        cmd.eprint_RED(systemConfig.logFilePath, f"[ERROR COM] [TIMEOUT] (device didn't respond in time) {ex}")
        if systemConfig.debug :
            raise ex;
    except Exception as ex :
        cmd.eprint_RED(systemConfig.logFilePath, f"[ERROR COM] {ex}")
        if systemConfig.debug :
            raise ex;

def read_scan( systemConfig, scan_config, matrix, com_ser, mustRead ):
    try : 
        increasing = True;
        while(self.mustRead) :
            # should go in timout thread
            output = self.com_ser.read_until_trigger();
            line, zAvg, eAvg = self.com_ser.format_DATA(s, config.width);
            matrix[line,:] = zAvg[:];
            increasing = not increasing;
    
    except OSError as ex:
        cmd.eprint_RED(systemConfig.logFilePath, f"[ERROR COM] (not right device) {ex}")
        if systemConfig.debug :
            raise ex;
    except TimeoutError as ex:
        cmd.eprint_RED(systemConfig.logFilePath, f"[ERROR COM] [TIMEOUT] (device didn't respond in time) {ex}")
        if systemConfig.debug :
            raise ex;
    except Exception as ex :
        cmd.eprint_RED(systemConfig.logFilePath, f"[ERROR COM] {ex}")
        if systemConfig.debug :
            raise ex;

def scan(systemConfig, scan_config, matrix, com_ser):
    try :
        com_ser = Serial_COM( systemConfig, scan_config.devicePath );
         
        with tm.timeout( systemConfig.timeOutComTime ) :
            import time
            com_ser.serial_init();
        
        # setup 
        com_ser.scan_size(scan_config.scan_size);
        com_ser.img_pixel(scan_config.image_pix);
        com_ser.line_rate(scan_confgi.freq);
        
        with tm.timeout( systemConfig.timeOutComTime ) :
            import time
            pixelPerLine = com_ser.getPixelPerLine();
        #intitiation of scanning
        com_ser.engage_tip();
        com_ser.enable_scanning();
        
        #scanning
        while(True) :
            raw_data = com_ser.read_until_trigger(); 
            lineCount, zAvg, eAvg = com_ser.format_LineDATA( raw_data, pixelPerLine );
            if lineCount == scan_config.image_pix :
                break;

        com_ser.disable_scanning();
        com_ser.serial_disable();

    except OSError as ex:
        cmd.eprint_RED(systemConfig.logFilePath, f"[ERROR COM] (not right device) {ex}")
        if systemConfig.debug :
            raise ex;
    except TimeoutError as ex:
        cmd.eprint_RED(systemConfig.logFilePath, f"[ERROR COM] [TIMEOUT] (device didn't respond in time) {ex}")
        if systemConfig.debug :
            raise ex;
    except Exception as ex :
        cmd.eprint_RED(systemConfig.logFilePath, f"[ERROR COM] {ex}")
        if systemConfig.debug :
            raise ex;




class Scanner:
    def __init__(self, systemConfig, scan_config) :
        self.com_ser = Serial_COM( systemConfig, devicePath ); 
        self.systemConfig = systemConfig;
        self.scan_config = scan_config;
        self.matrix = np.zeros((scan_config.width, scan_config.height), dtype=int);
        self.thread = 0;
        self.mustRead = True;

    def getMatrix(self) :
        return self.matrix.copy()

    def start_scan(self):
        args=(self.systemConfig, self.scan_config, self.matrix, self.com_ser, self.mustRead);
        self.thread = Thread(target=launch_scan, args=args)
        self.thread.start()
        

    def stop_scan(self):
        #TODO
        self.mustRead = False;
        pass;

    
    def simpleInteraction(self, config ):
        self.com_ser.serial_init();
        self.com_ser.enable_scanning();
        s = self.com_ser.read_until_trigger();
        self.com_ser.disable_scanning();
        self.com_ser.serial_disable();
        line, zAvg, eAvg = self.com_ser.format_DATA(s, config.width)
        for n in zAvg :
            print(hex(n))
