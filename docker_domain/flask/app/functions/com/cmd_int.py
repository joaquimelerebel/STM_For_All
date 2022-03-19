from __future__ import print_function
import sys
import time


#print in stderr in red
def eprint_RED(filepath, string, isWithTs=True):
    log(filepath, string);
    if(isWithTs) : 
         string = f"[{time.time()}] " + string
    sys.stderr.write(u"\u001b[31m" + string + u"\u001b[0m"+ f"\n")

#print in stderr in green
def eprint_GREEN(filepath, string, isWithTs=True):
    log(filepath, string);
    sys.stderr.write(u"\u001b[32m" + string + u"\u001b[0m" + f"\n")


#print in stdout in red
def print_RED(filepath, string, isWithTs=True):
    log(filepath, string) 
    if(isWithTs) : 
         string = f"[{time.time()}] " + string
    sys.stdout.write(u"\u001b[31m" + string + u"\u001b[0m"+ f"\n")

#print in stdout in green
def print_GREEN(string):
    sys.stdout.write(u"\u001b[32m" + string + u"\u001b[0m"+ f"\n")

#print in stdout in white
def print_verbose_WHITE(filepath, string, isWithTs=True ):
    log(filepath, string) 
    if(isWithTs) : 
         string = f"[{time.time()}] " + string
    sys.stdout.write(string)

# print the logs in a file 
def log(filepath, string): 
    txt = f"[{time.time()}] {string}" + "\n";
    with open(filepath, "a") as f : 
        f.write(string);