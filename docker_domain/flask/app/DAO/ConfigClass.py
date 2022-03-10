class Config :
    def __init__(self, logFilePath="coucou.txt", TOcom=1, isDebug=True):
        self.logFilePath = logFilePath;
        self.timeOutComTime = TOcom
        self.debug = isDebug
