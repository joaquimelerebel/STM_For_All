from __future__ import print_function
import sys
import time


#print in stderr in red
def eprint_RED(filepath, *args, **kwargs):
    log(filepath, args, kwargs) 
    sys.stderr.write(u"\u001b[31m")
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.write(u"\u001b[0m")

#print in stderr in green
def eprint_GREEN(*args, **kwargs):
    sys.stderr.write(u"\u001b[32m")
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.write(u"\u001b[0m")


#print in stdout in red
def print_RED(filepath, *args, **kwargs):
    log(filepath, args, kwargs) 
    sys.stdout.write(u"\u001b[31m")
    print(*args, **kwargs)
    sys.stdout.write(u"\u001b[0m")

#print in stdout in green
def print_GREEN(*args, **kwargs):
    sys.stdout.write(u"\u001b[32m")
    print(*args, **kwargs)
    sys.stdout.write(u"\u001b[0m")

#print in stdout in white
def print_verbose_WHITE(filepath, isWithTs, *args, **kwargs):
    log(filepath, args, kwargs) 
    if(isWithTs) : 
        sys.stdout.write( f"[{time.time()}] " )
    print(*args, **kwargs)

# print the logs in a file 
def log(filepath, *args, **kwargs): 
    txt = f"[{time.time()}] {args[0]}";
    with open(filepath, "a") as f : 
        f.write(txt, **kwargs)
