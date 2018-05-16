import sys
import os
import ctypes
from user_input_device import UserInputDevice
from user_input_device import UserEventType


JS_BUTTON_EVENT, JS_AXIS_EVENT = 1, 2
JS_BUTTON_PRESSED, JS_BUTTON_RELEASED = 0, 1

USER_EVENT_TYPES_OF_BTN_EVENT = [
    UserEventType.EXIT_PROGRAM,
    UserEventType.MODE_ON,
    UserEventType.MODE_OFF,
    UserEventType.DEFAULT,
    UserEventType.SPEED_DOWN,
    UserEventType.SPEED_UP,
]

lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libJoystick.so")
lib = ctypes.cdll.LoadLibrary(lib_path)


def convert_axis_value_to_radian(axis_value):
    # (axis value - axis min) * (radian max - radian min) / (axis max - axis min) + radian min
    # This function is dependent to steering angle range of car
    return (axis_value + 32767) * 0.6982 / 65534 - 0.3491 


class LogitechGamepadF710(UserInputDevice):
    def __init__(self, device="/dev/input/js0"):
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

    def device_name(self):
        return self._device

    def is_available(self):
        if self.read_event() == 0:
            return True
        else:
            return False

    def read_user_event(self):
        event_type = UserEventType.DEFAULT
        value = 0
        js_event_type = self.get_event_type()
        if js_event_type == JS_BUTTON_EVENT:
            btn_number, btn_state = self.get_button_event()
            if btn_number < 6 and btn_state == JS_BUTTON_PRESSED:
                event_type = USER_EVENT_TYPES_OF_BTN_EVENT[btn_number]
        elif js_event_type == JS_AXIS_EVENT:
            axis = self.get_axis_state()
            if axis == 0:
                x, y = self.get_axis_value(axis)
                if y < 0:
                    event_type = UserEventType.MOVE_FRONT
                elif y > 0:
                    event_type = UserEventType.MOVE_BACK
                else:
                    event_type = UserEventType.BRAKE
            elif axis == 1:
                x, y = self.get_axis_value(axis)
                event_type = UserEventType.CHANGE_STEERING_ANGLE
                value = convert_axis_value_to_radian(x)
        return event_type, value
                

if __name__ == '__main__':
    js = LogitechGamepadF710()
    while js.read_event() == 0:
        event_type = js.get_event_type()
        if event_type == JS_BUTTON_EVENT:
            btn_number, btn_state = js.get_button_event()
            print("Button %d %s" % (btn_number, btn_state))
            if btn_number == 0: # button X
                print("Exit")
                break
        elif event_type == JS_AXIS_EVENT:
            axis = js.get_axis_state()
            x, y = js.get_axis_value(axis)
            print("Axis %d (%6d, %6d)" % (axis, x, y))



