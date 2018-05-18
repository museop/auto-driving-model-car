import os
import sys
import threading
import time
from auto_driving import IAutoDriving
sys.path.insert(0, os.path.abspath('..'))
from camera.jetson_tx2_camera import LI_IMX377_MIPI_M12
from vehicle_control.rc_car_control import RCCarControl
from lane_keeping_assist.lane_keeping import LaneKeeping
from lane_keeping_assist.utils import range_map
from traffic_signal_detector.traffic_signal_detector import TrafficSignalDetector


EPS = 0.00001
MAX_SPEED = 10
MIN_SPEED = 0
MIN_FRONT_PWM = 325
MAX_BACK_PWM = 289
MID_PWM = 307
MIN_RADIAN = -0.3491

lock = threading.Lock()
car = RCCarControl()
car_speed = 1

class AutoDriver(threading.Thread):
    def __init__(self):
        super(AutoDriver, self).__init__()
        print('init AutoDriver')
        self.play = True
        self.authority_to_drive = False

    def grant_authority_to_drive(self):
        self.authority_to_drive = True

    def take_away_authority_to_drive(self):
        self.authority_to_drive = False

    def run(self):
        lane_keeping_assist = LaneKeeping()
        lane_keeping_assist.setup_frame_color_space("bgr")
        traffic_signal_detector = TrafficSignalDetector()
        
        front_camera = LI_IMX377_MIPI_M12()
            
        while self.play:
            if self.authority_to_drive:
                front_frame = front_camera.capture_frame()
                #  front_frame = front_camera.calibrate(front_frame)
                steering_angle = lane_keeping_assist.predict_angle(front_frame)
                steering_angle = steering_angle / 2
                adjusted_speed = range_map(-abs(steering_angle), MIN_RADIAN, 0.0, 0.0, car_speed+EPS)
                front_frame = front_camera.calibrate(front_frame)
                can_go = traffic_signal_detector.can_go_forward(front_frame)
                lock.acquire()
                car.steer_wheel(steering_angle)
                if can_go:
                    car.move_front(MIN_FRONT_PWM + adjusted_speed)
                else:
                    car.move_front(MID_PWM)
                lock.release()
            else:
                time.sleep(0.5)
        
    def stop(self):
        self.play = False
    
    def __del__(self):
        print('delete AutoDriver')

class AutoDrivingManager(IAutoDriving):
    def __init__(self):
        super(AutoDrivingManager, self).__init__()
        print('init AutoDrivingManager')
        self.authority_to_drive = True
        self.auto_driver = AutoDriver()
        self.auto_driver.start()
        
    def auto_driving_mode(self, mode):
        if self.authority_to_drive:
            if mode == True:
                self.auto_driver.grant_authority_to_drive()
                time.sleep(0.5)
                lock.acquire()
                car.move_front(MIN_FRONT_PWM + car_speed)
                lock.release()
            else:
                self.auto_driver.take_away_authority_to_drive()
                time.sleep(0.5)
                lock.acquire()
                car.move_front(MID_PWM)
                lock.release()
        print("auto_driving_mode: " + str(mode))

    def speed_up(self, value):
        if self.authority_to_drive:
            global car_speed
            car_speed = min(car_speed + 1, MAX_SPEED)
            print("speed_up: " + str(car_speed))

    def speed_down(self, value):
        if self.authority_to_drive:
            global car_speed
            car_speed = max(car_speed - 1, MIN_SPEED)
            print("speed_down: " + str(car_speed))

    def steer_wheel(self, steering_radian):
        if self.authority_to_drive:
            lock.acquire()
            car.steer_wheel(steering_radian) 
            lock.release()

    def move_front(self):
        if self.authority_to_drive:
            lock.acquire()
            car.move_front(MIN_FRONT_PWM + car_speed)
            lock.release()
            print("move_front")

    def move_back(self):
        if self.authority_to_drive:
            lock.acquire()
            car.move_back(MAX_BACK_PWM - car_speed)
            lock.release()
            print("move_back")
        
    def brake(self):
        if self.authority_to_drive:
            lock.acquire()
            car.move_front(MID_PWM)
            lock.release()
            print("brake")
    
    def clear(self):
        self.auto_driver.stop()

    def __del__(self):
        self.auto_driver.stop()
        print('delete AutoDrivingManager')

