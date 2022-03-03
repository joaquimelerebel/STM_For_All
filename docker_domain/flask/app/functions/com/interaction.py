from dan_serial_com import Serial_COM
import cmd_int as cmd
import timout

def ping( systemConfig, devicePath ):
    try :
        with timeout( systemConfig.timeOutComTime ) :
            import time
            if devicePath != "":
                com_ser = Serial_COM( devicePath );
                
                cmd.log( config.logFilePath, "[COM] PING")
                com_ser.serial_init();
                com_ser.serial_disable();

            else :
                raise(RuntimeError("device input name empty"))
    except OSError as ex:
        cmd.log( systemConfig.logFilePath, f"[ERROR COM] (not right device) -> {ex}")
        cmd.eprint_RED(f"[ERROR COM] (not right device) {ex}")
    except TimeoutError as ex:
        cmd.log( systemConfig.logFilePath, f"[ERROR COM] [TIMEOUT] (device didn't respond in time) {ex}")
        cmd.eprint_RED(f"[ERROR COM] [TIMEOUT] (device didn't respond in time) {ex}")
    except Exception as ex :
        cmd.log( systemConfig.logFilePath, f"[ERROR COM] {ex}")
        cmd.eprint_RED(f"[ERROR COM] {ex}")

def scan( systemConfig, scan_config ):
    try :
        com_ser = Serial_COM( scan_config.devicePath );
        
        with timeout( systemConfig.timeOutComTime ) :
            import time
            com_ser.serial_disable();

    except OSError as ex:
        cmd.log( systemConfig.logFilePath, f"[ERROR COM] (not right device) -> {ex}")
        cmd.eprint_RED(f"[ERROR COM] (not right device) {ex}")
    except TimeoutError as ex:
        cmd.log( systemConfig.logFilePath, f"[ERROR COM] [TIMEOUT] (device didn't respond in time) {ex}")
        cmd.eprint_RED(f"[ERROR COM] [TIMEOUT] (device didn't respond in time) {ex}")
    except Exception as ex :
        cmd.log( systemConfig.logFilePath, f"[ERROR COM] {ex}")
        cmd.eprint_RED(f"[ERROR COM] {ex}")

def simpleInteraction( config ):
    com_ser = Serial_COM( config );
    com_ser.serial_init();
    com_ser.enable_scanning();
    s = com_ser.read_until_DATA();
    com_ser.disable_scanning();
    com_ser.serial_disable();
    line, zAvg, eAvg = com_ser.format_DATA(s, config.width)
    for n in zAvg :
        print(hex(n))
