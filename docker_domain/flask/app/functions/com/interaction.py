from dan_serial_com import Serial_COM
import cmd_int as cmd
import timeout as tm

def ping( systemConfig, devicePath ):
    try :
        with tm.timeout( systemConfig.timeOutComTime ) :
            import time
            if devicePath != "":
                com_ser = Serial_COM( systemConfig, devicePath );
                
                cmd.log( systemConfig.logFilePath, "[COM] PING")
                com_ser.serial_init();
                com_ser.serial_disable();

            else :
                raise(RuntimeError("device input name empty"))
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

def scan( systemConfig, scan_config ):
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


def simpleInteraction( config ):
    com_ser = Serial_COM( config );
    com_ser.serial_init();
    com_ser.enable_scanning();
    s = com_ser.read_until_trigger();
    com_ser.disable_scanning();
    com_ser.serial_disable();
    line, zAvg, eAvg = com_ser.format_DATA(s, config.width)
    for n in zAvg :
        print(hex(n))
