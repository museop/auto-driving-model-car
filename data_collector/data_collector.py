import threading
import sys
import os
import time
sys.path.insert(0, os.path.abspath('..'))
from camera.jetson_tx2_camera import JetsonTX2Camera
from user_input_device.logitech_gamepad_f710 import LogitechGamepadF710
from user_input_device.user_input_device import UserEventType
from car_control.rc_car_control import RCCarControl



SEC_WRITE_INTERVAL = 1


class DataWriter(threading.Thread):
    def __init__(self, data_dir='data'):
        threading.Thread.__init__(self)
        self._data_dir = data_dir
        self._play = True
        self._save = False
        self._current_steering_angle = 0

    @property
    def current_steering_angle(self):
        return self._current_steering_angle

    @current_steering_angle.setter
    def current_steering_angle(self, angle):
        self._current_steering_angle = angle 


    def save_on(self):
        print("Begin saving")
        self._save = True

    def save_off(self):
        print("End saving")
        self._save = False

    def run(self):
        camera = JetsonTX2Camera()
        data_file = open(self._data_dir + '/data.txt', 'a')
        while self._play:
            if self._save:
                frame = camera.capture_frame()
                frame = camera.calibrate(frame)
                filename = str(time.time()) + '.jpg'
                data_file.write(filename + ' %f\n' % self.current_steering_angle)
                camera.save_frame(self._data_dir, filename, frame)
                print(str(time.time()) + ": " + str(self.current_steering_angle))
            time.sleep(SEC_WRITE_INTERVAL)
        data_file.close()
        print('Exit DataWriter')
    
    def stop(self):
        self._play = False


class DataCollector:

    def collect_data(self):
        car = RCCarControl()
        user_input_dev = LogitechGamepadF710()
        data_writer = DataWriter()
        data_writer.start()

        max_speed = 10
        min_speed = 0
        current_speed = 5
        
        while user_input_dev.is_available():
            user_event, value = user_input_dev.read_user_event()

            if user_event == UserEventType.CHANGE_STEERING_ANGLE:
                car.steer_wheel(value)
                data_writer.current_steering_angle = value
            elif user_event == UserEventType.MOVE_FRONT:
                car.move_front(325 + current_speed)
            elif user_event == UserEventType.MOVE_BACK:
                car.move_back(289 - current_speed)
            elif user_event == UserEventType.BRAKE:
                car.move_front(307)
            elif user_event == UserEventType.MODE_ON:
                data_writer.save_on()
            elif user_event == UserEventType.MODE_OFF:
                data_writer.save_off()
            elif user_event == UserEventType.SPEED_UP:
                current_speed = min(current_speed + 1, max_speed)
                print("current speed: " + str(current_speed))
            elif user_event == UserEventType.SPEED_DOWN:
                current_speed = max(current_speed - 1, min_speed)
                print("current speed: " + str(current_speed))
            elif user_event == UserEventType.EXIT_PROGRAM:
                car.steer_wheel(0)
                car.move_front(307)
                break

        data_writer.stop()
        print('Exit DataCollector')


if __name__ == '__main__':
    print("Collect data")
    data_collector = DataCollector()
    data_collector.collect_data()

        
