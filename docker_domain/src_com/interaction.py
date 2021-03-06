from dan_serial_com import Serial_COM

def test( config ):
    if config.test_type == "SIMPLE" : 
        simpleInteraction(config)


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
