from __future__ import print_function
import sys


#print in stderr in red
def eprint_RED(*args, **kwargs):
    sys.stderr.write(u"\u001b[31m")
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.write(u"\u001b[0m")

#print in stderr in green


def eprint_GREEN(*args, **kwargs):
    sys.stderr.write(u"\u001b[32m")
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.write(u"\u001b[0m")


#print in stdout in red
def print_RED(*args, **kwargs):
    sys.stdout.write(u"\u001b[31m")
    print(*args, **kwargs)
    sys.stdout.write(u"\u001b[0m")

#print in stdout in green


def print_GREEN(*args, **kwargs):
    sys.stdout.write(u"\u001b[32m")
    print(*args, **kwargs)
    sys.stdout.write(u"\u001b[0m")

#print in stdout in green


def print_verbose_WHITE(config, *args, **kwargs):
    if(config.verbose):
        print(*args, **kwargs)
