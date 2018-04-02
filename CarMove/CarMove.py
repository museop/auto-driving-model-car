import ctypes

lib = ctypes.cdll.LoadLibrary('./libcarMove.so')

class CarMove(object):
    def __init__(self):
        lib.CarMove_new.restype = ctypes.c_void_p

        lib.CarMove_setSpeed.argtypes = [ctypes.c_void_p, ctypes.c_double]
        lib.CarMove_setSpeed.restype = ctypes.c_void_p

        lib.CarMove_setDegree.argtypes = [ctypes.c_void_p, ctypes.c_double]
        lib.CarMove_setDegree.restype = ctypes.c_void_p

        lib.CarMove_getSpeed.argtypes = [ctypes.c_void_p]
        lib.CarMove_getSpeed.restype = ctypes.c_double

        lib.CarMove_getDegree.argtypes = [ctypes.c_void_p]
        lib.CarMove_getDegree.restype = ctypes.c_double

        lib.CarMove_moveFront.argtypes = [ctypes.c_void_p, ctypes.c_double]
        lib.CarMove_moveFront.restype = ctypes.c_void_p

        lib.CarMove_moveBack.argtypes = [ctypes.c_void_p, ctypes.c_double]
        lib.CarMove_moveBack.restype = ctypes.c_void_p

        lib.CarMove_turnLeft.argtypes = [ctypes.c_void_p, ctypes.c_double]
        lib.CarMove_turnLeft.restype = ctypes.c_void_p

        lib.CarMove_turnRight.argtypes = [ctypes.c_void_p, ctypes.c_double]
        lib.CarMove_turnRight.restype = ctypes.c_void_p

        lib.CarMove_stop.argtypes = [ctypes.c_void_p]
        lib.CarMove_stop.restype = ctypes.c_void_p

        lib.CarMove_quickBrake.argtypes = [ctypes.c_void_p]
        lib.CarMove_quickBrake.restype = ctypes.c_void_p

        self.obj = lib.CarMove_new();

    def setSpeed(self, speed):
        lib.CarMove_setSpeed(self.obj, speed)
    
    def setDegree(self, degree):
        lib.CarMove_setDegree(self.obj, degree)

    def getDegree(self):
        return lib.CarMove_getDegree(self.obj)

    def getSpeed(self):
        return lib.CarMove_getSpeed(self.obj)

    def moveFront(self, speed):
        lib.CarMove_moveFront(self.obj, speed)

    def moveBack(self, speed):
        lib.CarMove_moveBack(self.obj, speed)

    def turnLeft(self, degree):
        lib.CarMove_turnLeft(self.obj, degree)

    def turnRight(self, degree):
        lib.CarMove_turnRight(self.obj, degree)

    def stop(self):
        lib.CarMove_stop(self.obj)

    def quickBrake(self):
        lib.CarMove_quickBrake(self.obj)

        
