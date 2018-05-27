import os
import cv2
import numpy as np 


RED_MIN = np.array([-10, 100, 100])
RED_MAX = np.array([10, 255, 255])

YELLOW_MIN = np.array([15, 100, 100])
YELLOW_MAX = np.array([40, 255, 255])

GREEN_MIN = np.array([50, 100, 50])
GREEN_MAX = np.array([80, 255, 255])

QUEUE_SIZE = 30

UNKNOWN, RED, YELLOW, GREEN = 0, 1, 2, 3
COLORS_NAME = ["unknown", "red", "yellow", "green"]
COLORS = [(0, 0, 0), (0, 0, 255), (0, 255, 255), (0, 255, 0)]

DEFAULT_HAAR_PATH = os.path.join(os.path.dirname(__file__), "traffic_light.xml")


def argmax(a_list):
    len_list = len(a_list)
    max_value = 0
    argmax_i = 0
    for i in range(len_list):
        if a_list[i] > max_value:
            max_value = a_list[i]
            argmax_i = i
    return argmax_i


class TrafficLightDetector(object):
    def __init__(self, cascade_classifier=DEFAULT_HAAR_PATH):
        self.traffic_cascade = cv2.CascadeClassifier(cascade_classifier)
        self.lights_in_queue = [QUEUE_SIZE, 0, 0, 0] # unknown, red, green, blue
        self.queue = []
        for i in range(QUEUE_SIZE):
            self.queue.append(UNKNOWN)
    
    def detect(self, image):
        """
        Detect a traffic light from the image(BGR image).
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        traffic_light = self.traffic_cascade.detectMultiScale(gray)

        detections = []
        for (x_pos, y_pos, width, height) in traffic_light:
            mid_x1 = x_pos + int(width / 6)
            mid_x2 = x_pos + int(width * 5 / 6)
            mid_y1 = y_pos + int(height / 3)
            mid_y2 = y_pos + int(height * 2 / 3)
            color_id = self.classify_light(image[mid_y1:mid_y2, mid_x1:mid_x2])
            cv2.putText(image, COLORS_NAME[color_id], (x_pos-5, y_pos-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[color_id], 2)
            cv2.rectangle(image, (x_pos, y_pos), (x_pos+width, y_pos+height), COLORS[color_id], 2)
            detections.append((x_pos, y_pos, width, height, COLORS_NAME[color_id]))

        return detections

    def determine_the_status(self, image):
        """
        Determine the status of the traffic lights from the image(BGR image).
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        traffic_light = self.traffic_cascade.detectMultiScale(gray)

        cnt = [0, 0, 0, 0]
        for (x_pos, y_pos, width, height) in traffic_light:
            mid_x1 = x_pos + int(width / 6)
            mid_x2 = x_pos + int(width * 5 / 6)
            mid_y1 = y_pos + int(height / 3)
            mid_y2 = y_pos + int(height * 2 / 3)
            color_id = self.classify_light(image[mid_y1:mid_y2, mid_x1:mid_x2])
            #cv2.putText(image, COLORS_NAME[color_id], (x_pos-5, y_pos-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[color_id], 2)
            #cv2.rectangle(image, (x_pos, y_pos), (x_pos+width, y_pos+height), COLORS[color_id], 2)
            cnt[color_id] += 1

        traffic_color = argmax(cnt)
        self.queue.append(traffic_color)
        self.lights_in_queue[traffic_color] += 1
        self.lights_in_queue[self.queue.pop(0)] -= 1

        if self.lights_in_queue[RED] >= 1:
            return COLORS_NAME[RED]
        if self.lights_in_queue[YELLOW] >= 3:
            return COLORS_NAME[YELLOW]
        if self.lights_in_queue[GREEN] >= 5:
            return COLORS_NAME[GREEN]
        return COLORS_NAME[UNKNOWN]

    def classify_light(self, image):
        #cv2.imshow('test', image)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, RED_MIN, RED_MAX)
        red_cnt = cv2.countNonZero(mask)

        mask = cv2.inRange(hsv, YELLOW_MIN, YELLOW_MAX)
        yellow_cnt = cv2.countNonZero(mask)

        mask = cv2.inRange(hsv, GREEN_MIN, GREEN_MAX)
        green_cnt = cv2.countNonZero(mask)

        if red_cnt > yellow_cnt and red_cnt > green_cnt:
            return RED
        if yellow_cnt > red_cnt and yellow_cnt > green_cnt:
            return YELLOW
        if green_cnt > red_cnt and green_cnt > yellow_cnt:
            return GREEN
        return UNKNOWN
