import autoit
import time

def sendkey(keys,stoke=0.1,times=1):
    i=0
    while i<times:
        autoit.send(keys)
        time.sleep(stoke)
        i += 1

