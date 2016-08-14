__author__ = "Abhishek"
import subprocess, signal, os

def signal_handler(signall, frame):
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    print out
    for line in out.splitlines():
        if 'new_databricks_visualization.py' in line:
            pid = int(line.split(None, 1)[0])
            print "pid,",pid
            os.kill(pid, signal.SIGKILL)



if __name__ == '__main__':

    # registering handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        print "Doing some work"

#
# import signal
# import time
# import sys
#
# class GracefulKiller:
#   kill_now = False
#   def __init__(self):
#     signal.signal(signal.SIGINT, self.exit_gracefully)
#     signal.signal(signal.SIGTERM, self.exit_gracefully)
#     #signal.signal(signal.SIGKILL, self.exit_gracefully)
#
#   def exit_gracefully(self,signum, frame):
#     self.kill_now = True
#
# if __name__ == '__main__':
#   killer = GracefulKiller()
#   while True:
#     time.sleep(1)
#     print("doing something in a loop ...")
#     if killer.kill_now:
#         print "hey"
#         p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
#         out, err = p.communicate()
#         for line in out.splitlines():
#             #if 'killpgm.py' in line:
#             if 'new_databricks_visulaization.py' in line:
#                 pid = int(line.split(None, 1)[0])
#                 os.kill(pid, signal.SIGKILL)
#
#       # exit(-1)
#
#
# #   print "End of the program. I was killed gracefully :)"