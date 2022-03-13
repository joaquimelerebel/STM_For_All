# code from Emil
# https://stackoverflow.com/questions/492519/timeout-on-a-function-call

import threading
import trace
import time
import sys

#class from https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
class thread_with_trace(threading.Thread):
  def __init__(self, *args, **keywords):
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False
 
  def start(self):
    self.__run_backup = self.run
    self.run = self.__run     
    threading.Thread.start(self)
 
  def __run(self):
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup
 
  def globaltrace(self, frame, event, arg):
    if event == 'call':
      return self.localtrace
    else:
      return None
 
  def localtrace(self, frame, event, arg):
    if self.killed:
      if event == 'line':
        raise SystemExit()
    return self.localtrace
 
  def kill(self):
    self.killed = True
 
def timeout(time, fn, args, err):
    t = thread_with_trace(target=fn, args=args)
    t.start()

    # Wait for time seconds or until process finishes
    t.join(time)

    # If thread is still active
    if t.is_alive():
        t.kill()
        raise TimeoutError(err)

