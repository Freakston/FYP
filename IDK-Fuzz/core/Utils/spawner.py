import ctypes
import os


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
                self.devnull = open("/dev/null", "wb")
                self.env = [x+"="+os.environ[x] for x in os.environ] + [0]
        
        def execute(self, exe, args):
                pid = ctypes.c_int()
                args = [exe] + args + [0 ]
                argv = (ctypes.c_char_p * 5)(*args)
                env = (ctypes.c_char_p * (len(self.env) ))(*self.env)
                self.libc.posix_spawnattr_init(self.attrs)
                self.libc.posix_spawnattr_setflags(self.attrs, 0x40)
                self.libc.posix_spawn_file_actions_init(self.actions)
                self.libc.posix_spawn_file_actions_adddup2(
                        self.actions, self.devnull.fileno(), 1)
                self._posix_spawn(ctypes.byref(pid), ctypes.c_char_p(exe),
                                  self.actions, self.attrs,
                                  ctypes.cast(argv, ctypes.POINTER(ctypes.c_char_p)),
                                  ctypes.cast(env, ctypes.POINTER(ctypes.c_char_p)))
                status = ctypes.c_int()
                self.libc.waitpid(pid.value, ctypes.byref(status), 0)
