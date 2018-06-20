import os
import sys
import enum
import time
from logitech_gamepad_f710 import LogitechGamepadF710
from logitech_gamepad_f710 import JS_BUTTON_EVENT, JS_AXIS_EVENT, JS_BUTTON_PRESSED
#  sys.path.insert(0, os.path.abspath('..'))
from auto_driving_manager.auto_driving_manager import AutoDrivingManager


EXIT_PROGRAM = 0
AUTO_DRIVING_ON = 1
AUTO_DRIVING_OFF = 2
CAR_SPEED_UP = 4
CAR_SPEED_DOWN = 5

MOVE_CONTROL = 0
STEERING_CONTROL = 1


def convert_axis_value_to_radian(axis_value):
    # (axis value - axis min) * (radian max - radian min) / (axis max - axis min) + radian min
    # This function is dependent to steering angle range of car
    return (axis_value + 32767) * 0.6982 / 65534 - 0.3491 


class CommandProcessor(object):
    def __init__(self):
        super(CommandProcessor, self).__init__()
        print('init CommandProcessor')
        self.js = LogitechGamepadF710()
        self.adm = AutoDrivingManager()
        self.auto_mode = False
    
    def run(self):
        while self.js.read_event() == 0:
            event_type = self.js.get_event_type()
            if event_type == JS_BUTTON_EVENT:
                btn_number, btn_state = self.js.get_button_event()
                if btn_number == EXIT_PROGRAM:
                    self.adm.clear()
                    break
                if btn_state == JS_BUTTON_PRESSED:
                    self.process_button_event(btn_number)
            elif event_type == JS_AXIS_EVENT:
                axis = self.js.get_axis_state()
                x, y = self.js.get_axis_value(axis)
                self.process_axis_event(axis, x, y)
            if self.auto_mode == True:
                time.sleep(0.2)

    def process_button_event(self, btn_number):
        if btn_number == AUTO_DRIVING_ON:
            self.adm.auto_driving_mode(True)
            self.auto_mode = True
        elif btn_number == AUTO_DRIVING_OFF:
            self.adm.auto_driving_mode(False)
            self.auto_mode = False
        elif btn_number == CAR_SPEED_UP:
            self.adm.speed_up(1)
        elif btn_number == CAR_SPEED_DOWN:
            self.adm.speed_down(1)

    def process_axis_event(self, axis, x, y):
        if axis == STEERING_CONTROL:
            steering_radian = convert_axis_value_to_radian(x)
            self.adm.steer_wheel(steering_radian)
        elif axis == MOVE_CONTROL:
            if y < 0:
                self.adm.move_front()
            elif y > 0:
                self.adm.move_back()
            else:
                self.adm.brake()
                
    def __del__(self):
        print('delete CommandProcessor')
        
