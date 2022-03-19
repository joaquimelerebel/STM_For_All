from __future__ import print_function
import sys
import time


#print in stderr in red
def eprint_RED(config, string, isWithTs=True):
    log(config, string);
    if(isWithTs) : 
         string = f"[{time.time()}] " + string

    config.stdout_mutex.acquire()
    sys.stderr.write(u"\u001b[31m" + string + u"\u001b[0m"+ f"\n")
    config.stdout_mutex.release()

#print in stderr in green
def eprint_GREEN(config, string, isWithTs=True):
    log(config, string);

    config.stdout_mutex.acquire()
    sys.stderr.write(u"\u001b[32m" + string + u"\u001b[0m" + f"\n")
    config.stdout_mutex.release()


#print in stdout in red
def print_RED(config, string, isWithTs=True):
    log(config, string) 
    if(isWithTs) : 
         string = f"[{time.time()}] " + string
    
    config.stdout_mutex.acquire()
    sys.stdout.write(u"\u001b[31m" + string + u"\u001b[0m"+ f"\n")
    config.stdout_mutex.release()

#print in stdout in green
def print_GREEN(config, string):
    config.stdout_mutex.acquire()
    sys.stdout.write(u"\u001b[32m" + string + u"\u001b[0m"+ f"\n")
    config.stdout_mutex.release()

#print in stdout in white
def print_verbose_WHITE(config, string, isWithTs=True ):    
    log(config, string) 
    if(isWithTs) : 
         string = f"[{time.time()}] " + string
    
    config.stdout_mutex.acquire()
    sys.stdout.write(string)
    config.stdout_mutex.release()

# print the logs in a file 
def log(config, string): 
    txt = f"[{time.time()}] {string}" + "\n";
    
    # use of the globally defined mutex
    config.logfile_mutex.acquire()
    with open(config.logFilePath, "a") as f : 
        f.write(string);
    config.logfile_mutex.release()