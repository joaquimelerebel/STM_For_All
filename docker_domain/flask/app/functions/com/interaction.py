import numpy as np
from threading import Thread

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
        if devicePath == "" :
            raise RuntimeException("no path to the device")
        tm.timeout( systemConfig.timeOutComTime, ping_eff,
                    (systemConfig, devicePath),
                    "pong did not come in time")
        return True
    
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

def read_scan( systemConfig, 
                scan_config, 
                matrix, 
                com_ser, 
                mustRead):
    try : 
        increasing = True;
        while(mustRead) :
            # should go in timout thread
            output = com_ser.read_until_trigger();
            line, zAvg, eAvg = com_ser.format_LineDATA(output, int(scan_config.scan_size));
            matrix[line,:] = zAvg[:];
            increasing = not increasing;
        com_ser.disable_scanning();
    
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
        if systemConfig.devicePath == None :
            raise( RuntimeException("system config with no device path") )
        self.com_ser = Serial_COM( systemConfig, systemConfig.devicePath ); 
        self.systemConfig = systemConfig;
        self.scan_config = scan_config;
        self.matrix = np.zeros((int(scan_config.scan_size), int(scan_config.scan_size)), dtype=int);
        self.matrix_1 = 0;
        self.reading_thread = 0;
        self.mustRead = True;

    def hasUpdated(self) :
        return not np.array_equal(self.matrix, self.matrix_1)

    def getMatrix(self) :
        self.matrix_1 = self.matrix;
        return self.matrix_1.copy()

    def start_scan(self):
        #TODO seperate in other functions 
        self.com_ser.serial_init();
        self.com_ser.enable_scanning();
        # end of TODO
        args=(  self.systemConfig, 
                self.scan_config, 
                self.matrix, 
                self.com_ser, 
                self.mustRead);
        self.reading_thread = Thread(target=read_scan, args=args)
        self.reading_thread.start()

    def stop_scan(self):
        #TODO
        self.mustRead = False;

    def stop(self):
        #TODO
        self.mustRead = False;
        self.reading_thread.join()
        self.com_ser.disable_scanning();
        self.com_ser.serial_disable();

    
    def simpleInteraction(self, config ):
        self.com_ser.serial_init();
        self.com_ser.enable_scanning();
        s = self.com_ser.read_until_trigger();
        self.com_ser.disable_scanning();
        self.com_ser.serial_disable();
        line, zAvg, eAvg = self.com_ser.format_DATA(s, config.width)
        for n in zAvg :
            print(hex(n))
