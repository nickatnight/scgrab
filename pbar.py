import sys
import threading
import time


class ProgressBar(threading.Thread):
    def run(self):
        global stop
        print 'Downloading... ',
        sys.stdout.flush()
        i = 0

        while not stop:
            if (i%4) == 0:
                sys.stdout.write('\b/')
            elif (i%4) == 1:
                sys.stdout.write('\b-')
            elif (i%4) == 2:
                sys.stdout.write('\b\\')
            elif (i%4) == 3:
                sys.stdout.write('\b|')

            sys.stdout.flush()
            time.sleep(0.25)
            i+=1

stop = False
