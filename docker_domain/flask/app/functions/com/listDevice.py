import cmd_int as cmd
import serial.tools.list_ports
import re
import subprocess

def get_device_list( systemConfig ) : 
    cmd.print_RED( systemConfig.logFilePath, "getting device list")
    usbDic = get_usb_list(systemConfig);

    ports = serial.tools.list_ports.comports()
    devices={"PORT":[], "DESC":[], "HWID":[], "NAME":[]}
    for port, desc, hwid in sorted(ports):
        devices["PORT"].append(port);
        devices["DESC"].append(desc);
        devices["HWID"].append(hwid);

        pid=hwid[hwid.find("PID=") + len("PID="):].split()[0];
        hasDone=False;
        for d in usbDic :
            print(d["id"])
            if d["id"] == pid.lower().encode("utf-8"):
                devices["NAME"].append(d["tag"])
                hasDone = True;
                break;
        if not hasDone :
            devices["NAME"].append("");

    cmd.print_WHITE( systemConfig.logFilePath, str(devices))
    return devices;
            


# code from MikeiLL : https://stackoverflow.com/questions/8110310/simple-way-to-query-connected-usb-devices-info-in-python
def get_usb_list(systemConfig) :
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
