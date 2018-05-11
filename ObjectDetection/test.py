import numpy as np
import cv2

cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)320,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

RED_MIN = np.array([-10, 100, 100])
RED_MAX = np.array([10, 255, 255])

YELLOW_MIN = np.array([15, 100, 100])
YELLOW_MAX = np.array([40, 255, 255])

GREEN_MIN = np.array([50, 100, 50])
GREEN_MAX = np.array([120, 255, 255])

while cv2.waitKey(25) != ord('q'):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, RED_MIN, RED_MAX)
    red_cnt = cv2.countNonZero(mask)
    cv2.imshow('red', cv2.bitwise_and(frame, frame, mask=mask))

    mask = cv2.inRange(hsv, YELLOW_MIN, YELLOW_MAX)
    yellow_cnt = cv2.countNonZero(mask)
    cv2.imshow('yello', cv2.bitwise_and(frame, frame, mask=mask))

    mask = cv2.inRange(hsv, GREEN_MIN, GREEN_MAX)
    green_cnt = cv2.countNonZero(mask)
    cv2.imshow('green', cv2.bitwise_and(frame, frame, mask=mask))

    #  print([red_cnt, blue_cnt, green_cnt])

