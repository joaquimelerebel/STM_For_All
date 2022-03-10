import functions.com.cmd_int as cmd
import serial.tools.list_ports
import re
import subprocess

def get_device_list( systemConfig ) : 
    cmd.print_RED( systemConfig.logFilePath, "getting device list")
    usbDic = get_usb_list();
    ports = serial.tools.list_ports.comports();
    #---DEBUG---
    ports = [("USB1", "desc1PID=123 this is the USB device 1", "hwid1"), ("USB2", "desc2PID=123 this is the USB device 2", "hwid2"), ("USB3", "desc3PID=123 this is the USB device 3", "hwid3"), ("USB4", "desc4PID=123 this is the USB device 4", "hwid4") ];
    devices=[]
    for port, desc, hwid in sorted(ports):
        pid=hwid[hwid.find("PID=") + len("PID="):].split()[0];
        hasDone=False;
        for d in usbDic :
            if d["id"] == pid.lower().encode("utf-8"):
                name = d["tag"];
                hasDone = True;
                break;
        if not hasDone :
            name="";

        devices.append((port, desc, hwid, name));
        
    cmd.print_verbose_WHITE( systemConfig.logFilePath, f"devices found : {devices}")
    return devices;
            


# code from MikeiLL : https://stackoverflow.com/questions/8110310/simple-way-to-query-connected-usb-devices-info-in-python
def get_usb_list() :
    device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb")
    devices = []
    for i in df.split(b'\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                devices.append(dinfo)
    return devices
