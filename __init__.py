#!/usr/bin/env python3

import time, ctypes, struct

SIZEOF_SEM_T = 32

class SEMAPHORE:
    def __init__(self, _sem=None, libpath="/lib/x86_64-linux-gnu/libpthread.so.0"):
        pthreadlib = ctypes.cdll.LoadLibrary(libpath)
        if _sem is None:
            self._sem = ctypes.create_string_buffer(SIZEOF_SEM_T)
        else:
            self._sem = _sem
        self._sem_init = pthreadlib.sem_init
        self._sem_init.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint]
        self._sem_init.restype = ctypes.c_int
        self._sem_destroy = pthreadlib.sem_destroy
        self._sem_destroy.argtypes = [ctypes.c_void_p]
        self._sem_destroy.restype = ctypes.c_int
        self._sem_getvalue = pthreadlib.sem_getvalue
        self._sem_getvalue.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self._sem_getvalue.restype = ctypes.c_int
        self._sem_post = pthreadlib.sem_post
        self._sem_post.argtypes = [ctypes.c_void_p]
        self._sem_post.restype = ctypes.c_int
        self._sem_wait = pthreadlib.sem_wait
        self._sem_wait.argtypes = [ctypes.c_void_p]
        self._sem_wait.restype = ctypes.c_int
        self._sem_trywait = pthreadlib.sem_trywait
        self._sem_trywait.argtypes = [ctypes.c_void_p]
        self._sem_trywait.restype = ctypes.c_int
        self._sem_timedwait = pthreadlib.sem_timedwait
        self._sem_timedwait.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self._sem_timedwait.restype = ctypes.c_int

    def sem_init(self, pshared, value):
        return self._sem_init(self._sem, pshared, value)

    def sem_destroy(self):
        return self._sem_destroy(self._sem)

    def sem_getvalue(self):
        buf = ctypes.create_string_buffer(ctypes.sizeof(ctypes.c_int))
        self._sem_getvalue(self._sem, buf)
        return struct.unpack("@I", bytes(buf))[0]

    def sem_post(self):
        return self._sem_post(self._sem)

    def sem_wait(self):
        return self._sem_wait(self._sem)

    def sem_trywait(self):
        return self._sem_trywait(self._sem)

    def sem_timedwait(self, sec, isabs=False):
        if not isabs:
            abs_now = time.clock_gettime(time.CLOCK_REALTIME)
            sec += abs_now
        tv_sec, tv_nsec = int(sec), int((sec - int(sec)) * 1e9)
        print(tv_sec, tv_nsec)
        buf = struct.pack("@2l", tv_sec, tv_nsec)
        return self._sem_timedwait(self._sem, buf)

if __name__ == "__main__":
    sem = SEMAPHORE()
    sem.sem_init(0, 0)
    print(sem.sem_getvalue())
    sem.sem_timedwait(1.5)
    print("end1")
    sem.sem_timedwait(time.clock_gettime(time.CLOCK_REALTIME) + 1.5, True)
    print("end2")

