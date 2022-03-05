import subprocess
import time
import json
import os 
import ctypes
from base64 import b64decode
from core.Utils.utils import rabConnect
import sys
from posix_spawn import *

class Stats():
    def __init__(self):
        self.cases = 0
        self.fcps = 0
        self.crashes = 0

class Fuzzer():
    def __init__(self) -> None:
        self.start = time.time()
        self.channel = rabConnect()
        self.stats = Stats()

    def run_posix(self,message):
        
        cmd = message['exe'].encode()
        inp = message['input'].encode()
        c2pread, c2pwrite = os.pipe()
        # Tell posix_spawn to replace the child's stdout with the write end of the pipe.
        file_actions = FileActions()
        file_actions.add_dup2(c2pwrite, 1)
        # Close the parent's end of the pipe in the child.
        file_actions.add_close(c2pread)
        # Execute the child process.  posix_spawnp resolves the path.
        pid = posix_spawnp(cmd, [cmd] + [inp], file_actions=file_actions)
        # Close the child's end of the socket in the parent.
        os.close(c2pwrite)
        # Replace FD with a file object.
        f = os.fdopen(c2pread, "r")
        # And get the output.
        f.read()  # Returns "Hello world!\n"
        # Clean up the child process.
        self.stats.cases += 1
        return os.waitpid(pid, 0)  # Returns (pid, <returncode>)


    def run_subprocess(self, message):
        cmd = f"tests/{message['exe']}"
        inp = message['input']
        try:
            inp = b64decode(inp).decode()
        except Exception as e:
            pass
            return
        try: 
            op = subprocess.Popen([cmd, inp], stdin=subprocess.PIPE, stdout=sys.stdout)
        
        except subprocess.CalledProcessError as op:
            print(f"Process unexpected exit {op.returncode}")
            f = open(f"crashes/crash_{abs(op.returncode)}_{time.time()}","w")
            f.write(inp)
            f.close()
            exit()

    def run_subprocess_stdin(self, message):
        cmd = f"src/tests/{message['exe']}"
        inp = message['input']
        inp = b64decode(inp)
        try:
            op = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=sys.stdout)
            op.stdin.write(inp)
            op_out = op.communicate()[0]
            op.stdin.close()
            print(op_out)

        except subprocess.CalledProcessError as op:
            print(f"Process unexpected exit {op.returncode}")
            f = open(f"crashes/crash_{abs(op.returncode)}_{time.time()}", "w")
            f.write(inp)
            f.close()
            exit()

    def blob_consumer(self,ch, method, properties, message):
        try:
            blob = json.loads(message.decode("utf-8"))
        except Exception as e:
            print(f"[Client error] failed trying to decode the message {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        #blob = b64decode(decoded_message)
        # self.run_subprocess_stdin(blob)
        
        # Send a message back to stat-queue every 10 seconds? or 2000 iterations?
        # whichever tradeoff causes less perf diff.
        # the server should for at a predefined sync time fetch messages from stat-queue
        # and update the onboard stats.
        
        if (self.stats.cases%400 == 0):
            elapsed = time.time() - self.start
            print("[*] fc/s ",float(self.stats.cases)/elapsed)
            
        self.run_posix(blob)


    def start_exploit_consumer(self):
        # Connect to the result queue - consumer
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue="task-queue", on_message_callback=self.blob_consumer)

        self.channel.start_consuming()


    

