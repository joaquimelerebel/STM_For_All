class Config :
    def __init__(self, logFilePath="coucou.txt", TOcom=1, isDebug=True):
        self.logFilePath = logFilePath;
        self.timeOutComTime = TOcom
        self.debug = isDebug
        self.scanner = 0;
        self.devicePath = 0;

    def newScanner(self, scanner):
        if not self.scanner == 0 :
            self.scanner.stop_scan()
            self.scanner.stop()
        self.scanner = scanner

    def setDevicePath(self, devPath):
        self.devicePath = devPath;