from posix_spawn import *
import os
import time
import threading



def run_posix():
    cmd = b"" # Add the binary location here
    inp = b'inp'

    c2pread, c2pwrite = os.pipe()
    file_actions = FileActions()
    file_actions.add_dup2(c2pwrite, 1)
    
    file_actions.add_close(c2pread)
    pid = posix_spawnp(cmd, [cmd] + [inp], file_actions=file_actions)
    os.close(c2pwrite)

    f = os.fdopen(c2pread, "r")
    print(f.read())  # Returns "Hello world!\n"

    return os.waitpid(pid, 0)

start = time.time()
count = 0

def worker(id):
    global start,count
    
    while(1):
        run_posix()
        count+=1
        if count%1000 == 0:
            cps = float(count)/(time.time() - start)
            print("fcps = ",cps)

print(f"Got return value as {run_posix()}")
'''
threads = []
for i in range(16):
    threads.append(threading.Thread(target=worker, args=(i,)))

for thread in threads:
    thread.start()

while threading.active_count() > 0:
    time.sleep(0.1)
'''
