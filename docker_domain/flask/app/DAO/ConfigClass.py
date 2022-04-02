import threading

class Config :
    
    connected=[];
    room=[];

    def __init__(self, logFilePath="coucou.txt", TOcom=1, isDebug=True):
        self.logFilePath = logFilePath;
        self.timeOutComTime = TOcom
        self.debug = isDebug
        self.scanner = 0;
        self.devicePath = 0;
        # mutex creation 
        self.logfile_mutex = threading.Lock()
        self.stdout_mutex = threading.Lock()


    def newScanner(self, scanner):
        if not self.scanner == 0 :
            self.scanner.stop_scan()
            self.scanner.stop()
        self.scanner = scanner

    def setDevicePath(self, devPath):
        self.devicePath = devPath;