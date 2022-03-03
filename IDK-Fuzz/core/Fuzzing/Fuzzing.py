import subprocess
import time
import json
import os 
import ctypes
from base64 import b64decode
from core.Utils.utils import rabConnect
import sys

class PosixSpawn():
        def __init__(self):
                self.libc = ctypes.cdll.LoadLibrary("libc.so.6")
                self._posix_spawn = self.libc.posix_spawn
                self._posix_spawn.restype = ctypes.c_int
                self._posix_spawn.argtypes = (
                        ctypes.POINTER(ctypes.c_int),
                        ctypes.c_char_p, ctypes.c_void_p, ctypes.c_void_p,
                        ctypes.POINTER(ctypes.c_char_p),
                        ctypes.POINTER(ctypes.c_char_p)
                )
                # dirty hack: hardcoded struct sizes
                self.attrs = self.libc.malloc(336)
                self.actions = self.libc.malloc(80)
                self.devnull = open("/dev/null","wb")
                self.env = [x+"="+os.environ[x] for x in os.environ] + [ 0 ]

        def execute(self, exe, args):
                pid = ctypes.c_int()
                args = [exe] + args + [ 0 ]
                argv = (ctypes.c_char_p * 5) (*args)
                env = (ctypes.c_char_p * ( len(self.env) ))(*self.env)
                self.libc.posix_spawnattr_init(self.attrs)
                self.libc.posix_spawnattr_setflags(self.attrs, 0x40)
                self.libc.posix_spawn_file_actions_init(self.actions)
                self.libc.posix_spawn_file_actions_adddup2(self.actions, self.devnull.fileno(), 1)
                self._posix_spawn(ctypes.byref(pid), ctypes.c_char_p(exe),
                        self.actions, self.attrs,
                        ctypes.cast(argv, ctypes.POINTER(ctypes.c_char_p)),
                        ctypes.cast(env, ctypes.POINTER(ctypes.c_char_p)))
                status = ctypes.c_int()
                self.libc.waitpid(pid.value, ctypes.byref(status), 0)

class Fuzzer():
    def __init__(self) -> None:
        self.channel = rabConnect()
        self.ps = PosixSpawn()

    def run_posix(self,message):
        # Assuming the struct of the message as following
        # message = {exe : <executable_name>; input : <input>}
        exe = message['exe']
        inp = message['input']
        self.ps.execute(exe,inp)

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
        self.run_subprocess_stdin(blob)


    def start_exploit_consumer(self):
        # Connect to the result queue - consumer
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue="task-queue", on_message_callback=self.blob_consumer)

        self.channel.start_consuming()


    

