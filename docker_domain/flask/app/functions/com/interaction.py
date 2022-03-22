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
        cmd.log( systemConfig, "[COM] PING")
        if devicePath == "" :
            raise RuntimeException("no path to the device")
        tm.timeout( systemConfig.timeOutComTime, ping_eff,
                    (systemConfig, devicePath),
                    "pong did not come in time")
        return True
    
    except OSError as ex:
        cmd.eprint_RED(systemConfig, f"[ERROR COM] (not right device) {ex}")
        if systemConfig.debug :
            raise ex;
    except TimeoutError as ex:
        cmd.eprint_RED(systemConfig, f"[ERROR COM] [TIMEOUT] (device didn't respond in time) {ex}")
        if systemConfig.debug :
            raise ex;
    except Exception as ex :
        cmd.eprint_RED(systemConfig, f"[ERROR COM] {ex}")
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
            cmd.eprint_RED(systemConfig, f"[DBG] new loop from read")
            output = com_ser.read_until_trigger();
            line, zAvg, eAvg = com_ser.format_LineDATA(output, int(scan_config.scan_size));
            cmd.eprint_RED(systemConfig, f"[DBG] line nb : {line}");
            matrix[line,:] = zAvg[:];
            increasing = not increasing;
        com_ser.disable_scanning();
    
    except OSError as ex:
        cmd.eprint_RED(systemConfig, f"[ERROR COM] (not right device) {ex}")
        if systemConfig.debug :
            raise ex;
    except TimeoutError as ex:
        cmd.eprint_RED(systemConfig, f"[ERROR COM] [TIMEOUT] (device didn't respond in time) {ex}")
        if systemConfig.debug :
            raise ex;
    except Exception as ex :
        cmd.eprint_RED(systemConfig, f"[ERROR COM] {ex}")
        if systemConfig.debug :
            raise ex;

def scanSetup(systemConfig, scan_config, com_ser):
    try :

        # setup 
        com_ser.img_pixel( int(scan_config.img_pixel) );
        com_ser.line_rate( int(scan_config.line_rate) );
        com_ser.x_offset( int(scan_config.offset.x) );
        com_ser.y_offset( int(scan_config.offset.y) );
        com_ser.set_point( int(scan_config.set_point) );
        com_ser.sample_bias( int(scan_config.sample_bias) );
        com_ser.setKIGain( int(scan_config.PID.KI) );
        com_ser.setKPGain( int(scan_config.PID.KP) );

    except OSError as ex:
        cmd.eprint_RED(systemConfig, f"[ERROR COM] (not right device) {ex}")
        if systemConfig.debug :
            raise ex;
    except TimeoutError as ex:
        cmd.eprint_RED(systemConfig, f"[ERROR COM] [TIMEOUT] (device didn't respond in time) {ex}")
        if systemConfig.debug :
            raise ex;
    except Exception as ex :
        cmd.eprint_RED(systemConfig, f"[ERROR COM] {ex}")
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
        return not (self.matrix == self.matrix_1).all()

    def getMatrix(self) :
        self.matrix_1 = self.matrix.copy();
        return self.matrix_1.copy()

    def start_scan(self):
        self.com_ser.serial_init();

        scanSetup(self.systemConfig, self.scan_config, self.com_ser);
        self.com_ser.engage_tip();

        args=(  self.systemConfig, 
                self.scan_config, 
                self.matrix, 
                self.com_ser, 
                self.mustRead);
        self.com_ser.enable_scanning();
        self.reading_thread = Thread(target=read_scan, args=args)
        self.reading_thread.start()

    def stop_scan(self):
        #TODO
        self.mustRead = False;

    def stop(self):
        #TODO
        self.mustRead = False;
        if reading_thread != 0 :
            self.reading_thread.join()

        self.com_ser.disable_scanning();
        self.com_ser.retract_tip();
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
