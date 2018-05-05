import ctypes

lib = ctypes.cdll.LoadLibrary('/home/nvidia/Workspace/SelfDrivingModelCar/Joystick/libJoystick.so')

class Joystick(object):
    def __init__(self, device):
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
            event = "pressed"
        else:
            event = "released"
        return (lib.get_event_number(self.obj), event)

    def get_axis_value(self, axis):
        return (lib.get_axis_value_x(self.obj, axis), lib.get_axis_value_y(self.obj, axis))

if __name__ == '__main__':
    js = Joystick("/dev/input/js0") 

    while js.read_event() == 0:
        event_type = js.get_event_type()
        if event_type == 1: # button
            print("Button %d %s" % js.get_button_event())
        elif event_type == 2: # axis
            axis = js.get_axis_state()
            x, y = js.get_axis_value(axis)
            print("Axis %d (%6d, %6d)" % (axis, x, y))



