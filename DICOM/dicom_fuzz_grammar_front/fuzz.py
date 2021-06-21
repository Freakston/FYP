import sys
from subprocess import *
import multiprocessing
import threading
import time

NUM_CPUS = multiprocessing.cpu_count()
corups_dir = "./corpus/intersting/"

def mutate_rad(dcm):
    try:
        rad = Popen(['radamsa','-n','1','-'],stdin=PIPE,stdout=PIPE)
    except CalledProcessError as rad_ret:
        print("[+] Failed to run radamsa and mutate ",rad_ret)
    
    dcm = rad.communicate(dcm)[0]

    return dcm

def fuzz(cpu):
    #keep running it 
    dcm = open("./corpus/I_000000.dcm","rb").read()
    while True:
        print("Execution on cpu: ",cpu)
        dcm = mutate_rad(dcm)
        try:
            run(['./target/dcmdump', dcm],stdin=PIPE,stderr=PIPE,stdout=PIPE, capture_output=True)
            if rad.returncode < 0:
                print("[+] Crash detected with {}".format(signal.Signals(abs(rad.returncode)).name)
                file_name = corups_dir+str(int(time.time()))
                f = open(file_name, 'wb')
                f.write(dcm)
                f.close()
                print("[+] Crash input written to {}".format(file_name))
        except Exception as e:
            print(str(e))
            #pass to make sure we restart the thread
            pass

if __name__ == "__main__":
    #multithread depending on the number of cpu's
    for cpu in range(0, NUM_CPUS):
        threading.Timer(0.0, fuzz,args=[cpu]).start()