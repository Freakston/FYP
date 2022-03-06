from core.Fuzzing.Fuzzing import Fuzzer
import threading

def worker():
    f = Fuzzer()
    f.start_exploit_consumer()

worker()