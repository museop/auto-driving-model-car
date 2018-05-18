import os
import sys
import time


if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath('..'))
    from vehicle_control.rc_car_control import RCCarControl, RADIAN_MID, RADIAN_MIN, RADIAN_MAX

    print("Test Car move..")
    car = RCCarControl()

    print("move front!")
    car.steer_wheel(RADIAN_MID)
    car.move_front(330)
    time.sleep(2)

    print("turn right!")
    car.steer_wheel(RADIAN_MAX)
    time.sleep(2)

    print("turn left!")
    car.steer_wheel(RADIAN_MIN)
    time.sleep(2)

    print("stop!")
    car.steer_wheel(RADIAN_MID)
    car.stop()
