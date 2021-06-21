import sys
from subprocess import *
import multiprocessing
import threading
import time
import shutil
import os

from fuzz_dicom.template import *

NUM_CPUS = multiprocessing.cpu_count()
corups_dir = "./corpus/intersting/"

def mutate_rad(dcm):
    try:
        rad = Popen(['radamsa','-n','1','-'],stdin=PIPE,stdout=PIPE)
    except CalledProcessError as rad_ret:
        print("[+] Failed to run radamsa and mutate ",rad_ret)
    
    dcm = rad.communicate(dcm)[0]

    return dcm

def handle_crash(dcm):
    fileName = corups_dir + str(int(time.time()))
    shutil.move("currentInp", fileName)
    print("[+] Crash input written to {}".format(fileName))

def fuzz(cpu,exec):
    #keep running it 
    dcm = open("./corpus/I_000000.dcm","rb").read()
    while True:
        #dcm = mutate_rad(dcm)
        dcm = mut(dcm)
        f = open("currentInp","wb")
        f.write(dcm)
        f.close()
        exec = exec + 1
        print("[+] Exec ",exec)
        try:
            rad = run(['./target/dcmdump', 'currentInp'],stdin=PIPE,stderr=PIPE,stdout=PIPE)
            #diff = run(['diff', "currentInp","./corpus/I_000000.dcm"],capture_output=True)
            #print(diff.stdout)
            if rad.returncode < 0:
                print("[+] Crash detected with {}".format(signal.Signals(abs(rad.returncode)).name))
                handle_crash(dcm)
        except Exception as e:
            print(str(e))
            pass
        except KeyboardInterrupt:
            print("[+] Keyboard Interrupt")
            os._exit(1)
            

                

if __name__ == "__main__":
    
    #multithread depending on the number of cpu's
    #for cpu in range(0, NUM_CPUS):
        #threading.Timer(0.0, fuzz,args=[cpu]).start()
    
    exec = 0
    while(True):
        fuzz(1,exec)