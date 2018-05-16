import sys
import ctypes
import os
from car_control import CarControl


RADIAN_MIN, RADIAN_MID, RADIAN_MAX = -0.3491, 0., 0.3491
PWM_MIN, PWM_MAX = 235., 379.

lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libcarMove.so')
lib = ctypes.cdll.LoadLibrary(lib_path)

def convert_radian_to_pwm(radian):
    return (radian + 0.3491) * 144. / 0.6982 + 235.  # (radian - radian min) * (pwm max - pwm min) / (radian max - radian min) + pwm min


class RCCarControl(CarControl):
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

    def move_front(self, pwm):
        lib.CarMove_moveFront(self.obj, pwm)

    def move_back(self, pwm):
        lib.CarMove_moveBack(self.obj, pwm)

    def steer_wheel(self, radian):
        pwm = convert_radian_to_pwm(radian)
        if radian >= 0:
            lib.CarMove_turnRight(self.obj, pwm)
        else:
            lib.CarMove_turnLeft(self.obj, pwm)

    def stop(self):
        lib.CarMove_stop(self.obj)



