import cv2
import time
import numpy as np
import threading
from Joystick.Joystick import Joystick
from CarMove.CarMove import CarMove
from LaneKeepingAssist.steering_model import SteeringModel
from LaneKeepingAssist.utility import steering_angle2pwm_value, range_map

NEUTRAL_VALUE = 307
MOVE_FRONT_SPEED = 328
MOVE_BACK_SPEED = 284

js = None
car = None
steering_model = None
self_driving_mode = False

def steer(steering_value):
    if steering_value >= 307.0:
        car.turnRight(steering_value)
    else:
        car.turnLeft(steering_value)

def self_driving():
    steering_model.load_model_from('LaneKeepingAssist/model.h5')
    cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)320, height=(int)160,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
    while True:
        if self_driving_mode:
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            steering_radian = steering_model.predict(frame)
            steering_value = steering_angle2pwm_value(steering_radian)
            steer(steering_value)
        time.sleep(0.01)
    cap.release()

if __name__ == '__main__':
    js = Joystick("/dev/input/js0")
    car = CarMove()
    steering_model = SteeringModel()

    t1 = threading.Thread(target=self_driving) 
    t1.daemon = True
    t1.start()

    while js.read_event() == 0:
        event_type = js.get_event_type()
        # button event
        if event_type == 1:
            btn, btype = js.get_button_event()
            if btn == 0:
                print('Exit..')
                break
            elif btn == 3 and btype == "pressed":
                if self_driving_mode:
                    self_driving_mode = False
                    car.moveFront(NEUTRAL_VALUE)
                else:
                    self_driving_mode = True
                    car.moveFront(MOVE_FRONT_SPEED)
                print("auto driving: " + str(self_driving_mode))
        # axis event
        elif event_type == 2 and self_driving_mode == False:
            axis = js.get_axis_state()
            if axis == 0:
                x, y = js.get_axis_value(axis)
                if y < 0:
                    print("move front")
                    car.moveFront(MOVE_FRONT_SPEED)
                elif y > 0:
                    print("move back")
                    car.moveBack(MOVE_BACK_SPEED)
                else:
                    print("stop")
                    car.moveFront(NEUTRAL_VALUE)
            elif axis == 1:
                x, y = js.get_axis_value(axis)
                pwm = range_map(x, -32767, 32767, 235, 379)
                if pwm >= NEUTRAL_VALUE:
                    car.turnRight(pwm)
                else:
                    car.turnLeft(pwm)
    car.turnRight(NEUTRAL_VALUE)
    car.stop()
