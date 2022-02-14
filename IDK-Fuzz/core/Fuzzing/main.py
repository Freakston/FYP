#!/usr/bin/python3
import subprocess
import os, sys
import time
from damutator import *

SEED_INPUT = "aaaaaabcd"

def run_once(cmd,inp=""):
    try: 
        op = subprocess.run([f"{cmd}"], check=True,universal_newlines = True, stdout = subprocess.PIPE)

    except subprocess.CalledProcessError as op:
        print(op)
        print(f"Process unexpected exit {op.returncode}")
        f = open(f"crashes/crash_{abs(op.returncode)}_{time.time()}","w")
        f.write(inp)
        f.close()
        exit()

def main():
    if len(sys.argv) != 2:
        print("python3 main.py <cmd>")
    
    print("Running Fuzzer")
    
    input_val = SEED_INPUT

    start = time.time()
    iter = 0

    while(True):

        print("\nMutating Seed")
        input_val = byteMutate(input_val,1)

        f = open("input_file","w")
        f.write(input_val)
        f.close()

        run_once(sys.argv[1],input_val)
        iter += 1

        if (iter & 0xffffff):
            elapsed = time.time()
            print(f"[*] fcps : {iter/(elapsed-start)}\titer : {iter}")

if __name__ == "__main__":
    main()