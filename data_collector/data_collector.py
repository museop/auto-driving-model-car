import threading
import sys
import os
import time
sys.path.insert(0, os.path.abspath('..'))
from camera.jetson_tx2_camera import LI_IMX377_MIPI_M12
from command_processor.logitech_gamepad_f710 import LogitechGamepadF710
from command_processor.logitech_gamepad_f710 import JS_BUTTON_EVENT, JS_AXIS_EVENT, JS_BUTTON_PRESSED
from vehicle_control.rc_car_control import RCCarControl


EXIT_PROGRAM = 0
RECORD_ON = 1
RECORD_OFF = 2
CAR_SPEED_UP = 4
CAR_SPEED_DOWN = 5

MOVE_CONTROL = 0
STEERING_CONTROL = 1

SEC_WRITE_INTERVAL = 0.02


def convert_axis_value_to_radian(axis_value):
    # (axis value - axis min) * (radian max - radian min) / (axis max - axis min) + radian min
    # This function is dependent to steering angle range of car
    return (axis_value + 32767) * 0.6982 / 65534 - 0.3491 


class DataWriter(threading.Thread):
    def __init__(self, data_dir='data'):
        threading.Thread.__init__(self)
        self._data_dir = data_dir
        self._play = True
        self._record = False
        self._current_steering_angle = 0

    @property
    def current_steering_angle(self):
        return self._current_steering_angle

    @current_steering_angle.setter
    def current_steering_angle(self, angle):
        self._current_steering_angle = angle 

    def record_on(self):
        self._record = True

    def record_off(self):
        self._record = False

    def run(self):
        camera = LI_IMX377_MIPI_M12()
        data_file = open(self._data_dir + '/data.txt', 'a')
        while self._play:
            if self._record:
                frame = camera.capture_frame()
                frame = camera.calibrate(frame)
                filename = str(time.time()) + '.jpg'
                data_file.write(filename + ' %f\n' % self.current_steering_angle)
                camera.save_frame(self._data_dir, filename, frame)
                print(str(time.time()) + ": " + str(self.current_steering_angle))
            time.sleep(SEC_WRITE_INTERVAL)
        data_file.close()
    
    def stop(self):
        self._play = False


class DataCollector:
    def __init__(self):
        self.car = RCCarControl()
        self.data_writer = DataWriter()
        self.max_speed = 10
        self.min_speed = 0
        self.current_speed = 5

    def collect_data(self):
        js= LogitechGamepadF710()
        self.data_writer.start()
        
        while js.read_event() == 0:
            event_type = js.get_event_type()
            if event_type == JS_BUTTON_EVENT:
                btn_number, btn_state = js.get_button_event()
                if btn_number == EXIT_PROGRAM:
                    print('End..')
                    break
                if btn_state == JS_BUTTON_PRESSED:
                    self.process_button_event(btn_number)
            elif event_type == JS_AXIS_EVENT:
                axis = js.get_axis_state()
                x, y = js.get_axis_value(axis)
                self.process_axis_event(axis, x, y)
        self.data_writer.stop()
    
    def process_button_event(self, btn_number):
        if btn_number == RECORD_ON:
            self.data_writer.record_on()
            print("Begin saving")
        elif btn_number == RECORD_OFF:
            self.data_writer.record_off()
            print("End saving")
        elif btn_number == CAR_SPEED_UP:
            self.current_speed = min(self.current_speed+1, self.max_speed)
            print("current speed: " + str(self.current_speed))
        elif btn_number == CAR_SPEED_DOWN:
            self.current_speed = max(self.current_speed-1, self.min_speed)
            print("current speed: " + str(self.current_speed))

    def process_axis_event(self, axis, x, y):
        if axis == STEERING_CONTROL:
            steering_radian = convert_axis_value_to_radian(x)
            self.car.steer_wheel(steering_radian)
            self.data_writer.current_steering_angle = steering_radian
        elif axis == MOVE_CONTROL:
            if y < 0:
		pwm = 325+self.current_speed
                self.car.move_front(pwm)
            elif y > 0:
		pwm = 289-self.current_speed
                self.car.move_back(pwm)
            else:
                self.car.move_front(307)


if __name__ == '__main__':
    print("Collect data")
    data_collector = DataCollector()
    data_collector.collect_data()

        
