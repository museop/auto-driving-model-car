import sys
import os
import ctypes


JS_BUTTON_EVENT, JS_AXIS_EVENT = 1, 2
JS_BUTTON_PRESSED, JS_BUTTON_RELEASED = 0, 1


lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libJoystick.so")
lib = ctypes.cdll.LoadLibrary(lib_path)


class LogitechGamepadF710:
    def __init__(self, device="/dev/input/js0"):
        print('init LogitechGamepadF710')
        lib.new_joystick.restype = ctypes.c_void_p

        lib.read_event.argtypes = [ctypes.c_void_p]
        lib.read_event.restype = ctypes.c_int

        lib.get_axis_count.argtypes = [ctypes.c_void_p]
        lib.get_axis_count.restype = ctypes.c_int

        lib.get_button_count.argtypes = [ctypes.c_void_p]
        lib.get_button_count.restype = ctypes.c_int

        lib.get_axis_state.argtypes = [ctypes.c_void_p]
        lib.get_axis_state.restype = ctypes.c_int

        lib.get_event_type.argtypes = [ctypes.c_void_p]
        lib.get_event_type.restype = ctypes.c_int

        lib.get_event_number.argtypes = [ctypes.c_void_p]
        lib.get_event_number.restype = ctypes.c_int

        lib.get_event_value.argtypes = [ctypes.c_void_p]
        lib.get_event_value.restype = ctypes.c_int

        lib.get_axis_value_x.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.get_axis_value_x.restype = ctypes.c_int

        lib.get_axis_value_y.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.get_axis_value_y.restype = ctypes.c_int

        self._device = device
        self.obj = lib.new_joystick(device);

    def read_event(self):
        return lib.read_event(self.obj)

    def get_axis_count(self):
        return lib.get_axis_count(self.obj)

    def get_button_count(self):
        return lib.get_button_count(self.obj)

    def get_axis_state(self):
        return lib.get_axis_state(self.obj)

    def get_event_type(self):
        return lib.get_event_type(self.obj)

    def get_button_event(self):
        if lib.get_event_value(self.obj):
            event = JS_BUTTON_PRESSED
        else:
            event = JS_BUTTON_RELEASED
        return (lib.get_event_number(self.obj), event)

    def get_axis_value(self, axis):
        return (lib.get_axis_value_x(self.obj, axis), lib.get_axis_value_y(self.obj, axis))
    
    def __del__(self):
        print('delete LogitechGamepadF710')
                

